import os
import re
import subprocess
import sys

import gitread
import kitpaths
import regionsync

sys.path.insert(0, f"{kitpaths.KIT}/pad")
from decomment import strip

KIT, SP = kitpaths.KIT, kitpaths.SP
CLEAN = f"{SP}/clean"
MANIFEST = f"{CLEAN}/manifest.tsv"
LANDED = f"{CLEAN}/landed.tsv"
REJECTED = f"{CLEAN}/rejected.tsv"
REGIONS = ("usa", "jpn", "eur")
COUPLED = ("addrname", "remangle")
SWAP = {".cpp": ".c", ".c": ".cpp"}
USAGE = """bash landclean.sh [reviewed.txt]

With reviewed.txt (one repo path per line), only those rows land; the rest stay queued.
Lands rewritten sources of functions already on decomp-matching. $SP/clean/manifest.tsv lists
`<repo path>\\t<blob it replaces>\\t<why>`; $SP/clean/<repo path> is the rewrite. A rewrite saved under
the other source extension ($SP/clean/<stem>.c for a <stem>.cpp row, or the reverse) replaces the file
under that name and renames it in every region's delinks.txt. Under the wave lock,
from the published tip of the integration tree: drops a row whose file changed since its blob,
applies the rest, requires ninja check and sha1 in usa/jpn/eur (built at once), sets aside the rows a
red build's log names (or half the batch when it names none) until what stays builds green as one
set, commits that set, publishes, and moves every row to landed.tsv or rejected.tsv. A batch that is
red with nothing named builds the tip alone; when the tip is red too, every row stays queued.
Exit 0: landed or nothing to land. 1: refused."""


def run(cwd, *args, stdin=None):
    r = subprocess.run(list(args), cwd=cwd, input=stdin, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.returncode, r.stdout + r.stderr


def git(tree, *args):
    return run(tree, "git", *args)


def stage(tree, rels):
    return run(tree, "git", "add", "--pathspec-from-file=-", stdin="".join(f"{rel}\n" for rel in rels))


def rows():
    out = []
    try:
        for line in open(MANIFEST, encoding="utf-8"):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0]:
                out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    except OSError:
        pass
    return out


def target(rel):
    stem, ext = os.path.splitext(rel)
    other = stem + SWAP.get(ext, ext)
    return other if not os.path.isfile(f"{CLEAN}/{rel}") and os.path.isfile(f"{CLEAN}/{other}") else rel


def delinks_naming(tree, tip, rel):
    out = git(tree, "grep", "-l", "-F", f"{rel}:", tip, "--", "config")[1].split()
    return [p.split(":", 1)[1] for p in out if p.endswith("delinks.txt")]


def touched(tree, tip, entries):
    paths = []
    for rel, _, _ in entries:
        paths.append(rel)
        if target(rel) != rel:
            paths += [target(rel)] + delinks_naming(tree, tip, rel)
    return list(dict.fromkeys(paths))


def split_stale(tree, entries):
    current = gitread.blob_ids(tree, [f"HEAD:{rel}" for rel, _, _ in entries])
    fresh, stale = [], []
    for rel, base, why in entries:
        missing = not os.path.isfile(f"{CLEAN}/{target(rel)}")
        (stale if current.get(f"HEAD:{rel}") != base or missing else fresh).append((rel, base, why))
    return fresh, stale


def units(entries):
    groups, out = {}, []
    for entry in entries:
        if entry[2] in COUPLED:
            if entry[2] not in groups:
                groups[entry[2]] = []
                out.append(groups[entry[2]])
            groups[entry[2]].append(entry)
        else:
            out.append([entry])
    return out


def settle(entries, check):
    seen = {}

    def test(batch):
        key = frozenset(batch)
        if key not in seen:
            seen[key] = check(batch)
        return seen[key]

    def grow(base, parts):
        batch = base + [e for p in parts for e in p]
        if not parts:
            return base
        ok, blamed = test(batch)
        if ok:
            return batch
        if len(parts) == 1:
            return base
        named = [i for i, p in enumerate(parts) if blamed & set(p)]
        if not named or len(named) == len(parts):
            named = range(len(parts) // 2, len(parts))
        first = [p for i, p in enumerate(parts) if i not in named]
        return grow(grow(base, first), [parts[i] for i in named])

    parts = units(entries)
    if parts:
        ok, blamed = test([e for p in parts for e in p])
        if not ok and not blamed and not test([])[0]:
            return None
    return grow([], parts)


def blame(tree, part, red):
    import culprits
    tags = {}
    for rel, _, _ in part:
        try:
            with open(f"{CLEAN}/{target(rel)}", encoding="utf-8", errors="ignore") as fh:
                tags[target(rel)] = culprits.tag_of(fh.read()) or ("", "")
        except OSError:
            tags[target(rel)] = ("", "")
    named = set()
    for region, log in red.items():
        named |= {path for _, _, path, _ in culprits.name(log, tags)}
        for folder in regionsync.failed_folders(log, region):
            try:
                with open(f"{tree}/{folder}/delinks.txt", encoding="utf-8", errors="ignore") as fh:
                    named |= {src for src, _ in regionsync.BLOCK.findall(fh.read())}
            except OSError:
                pass
    return {entry for entry in part if target(entry[0]) in named}


def verdict(tree, tip, part, fresh):
    import culprits
    apply(tree, tip, part, fresh)
    results = regionsync.green(REGIONS)
    if any(not ok and culprits.transient(log) for ok, log in results.values()):
        results = regionsync.green(REGIONS)
    red = {region: log for region, (ok, log) in results.items() if not ok}
    return not red, blame(tree, part, red)


def wanted(rel):
    if rel.endswith((".c", ".cpp")):
        with open(f"{CLEAN}/{rel}", encoding="utf-8") as fh:
            return strip(fh.read()).encode("utf-8")
    with open(f"{CLEAN}/{rel}", "rb") as fh:
        return fh.read()


def apply(tree, tip, entries, fresh=()):
    part = {rel for rel, _, _ in entries}
    back = [rel for rel, _, _ in fresh if rel not in part]
    if back:
        dirty = set(git(tree, "diff", "--name-only", "-z")[1].split("\0"))
        back = [rel for rel in back if rel in dirty]
    swapped = {rel for rel, _, _ in list(fresh) + list(entries) if target(rel) != rel}
    for rel in swapped:
        if os.path.exists(f"{tree}/{target(rel)}"):
            os.remove(f"{tree}/{target(rel)}")
        back += [rel] + delinks_naming(tree, tip, rel)
    if back:
        run(tree, "git", "checkout", "-q", "--pathspec-from-file=-", "--pathspec-file-nul", tip,
            stdin="".join(f"{rel}\0" for rel in dict.fromkeys(back)))
    for rel in part:
        new = target(rel)
        data = wanted(new)
        if new != rel:
            os.remove(f"{tree}/{rel}")
            for cfg in delinks_naming(tree, tip, rel):
                with open(f"{tree}/{cfg}", encoding="utf-8", newline="") as fh:
                    text = fh.read()
                with open(f"{tree}/{cfg}", "w", encoding="utf-8", newline="") as fh:
                    fh.write(re.sub(rf"(?m)^{re.escape(rel)}:", lambda m: f"{new}:", text))
        try:
            with open(f"{tree}/{new}", "rb") as fh:
                if fh.read() == data:
                    continue
        except OSError:
            pass
        with open(f"{tree}/{new}", "wb") as fh:
            fh.write(data)


def write_rows(path, entries, mode):
    with open(path, mode, encoding="utf-8", newline="\n") as fh:
        fh.writelines(f"{rel}\t{base}\t{why}\n" for rel, base, why in entries)


def main():
    if len(sys.argv) > 2:
        sys.exit(USAGE)
    entries = rows()
    if len(sys.argv) == 2:
        reviewed = {ln.strip() for ln in open(sys.argv[1], encoding="utf-8") if ln.strip()}
        entries = [e for e in entries if e[0] in reviewed]
    if not entries:
        print("nothing to land")
        return 0
    code, out = run(KIT, sys.executable, f"{KIT}/integ_tree.py", "sync")
    if code:
        print(f"REFUSED: integ_tree.py sync: {out.strip()[-200:]}")
        return 1
    tree = out.strip().splitlines()[-1]
    os.chdir(tree)
    git(tree, "fetch", "-q", kitpaths.DECOMP_URL, kitpaths.DECOMP_BRANCH)
    tip = git(tree, "rev-parse", "FETCH_HEAD")[1].strip()
    git(tree, "checkout", "-q", "-f", "--detach", tip)
    fresh, stale = split_stale(tree, entries)
    broken = {why for _, _, why in stale if why in COUPLED}
    stale += [e for e in fresh if e[2] in broken]
    fresh = [e for e in fresh if e[2] not in broken]
    for rel, _, _ in stale:
        print(f"STALE {rel}: changed on decomp-matching since it was rewritten; rewrite it again")

    good = settle(fresh, lambda part: verdict(tree, tip, part, fresh))
    queued = fresh if good is None else []
    if good is None:
        print(f"REFUSED: decomp-matching does not build green at {tip[:8]}; {len(fresh)} row(s) stay queued")
        good = []
    red = [e for e in fresh if e not in good and e not in queued]
    for rel, _, _ in red:
        print(f"RED {rel}: a region does not build with it")
    apply(tree, tip, good, fresh)
    if good:
        stage(tree, touched(tree, tip, good))
        if git(tree, "commit", "-q", "-m", f"Clean {len(good)} matched source(s)")[0]:
            print("REFUSED: nothing to commit")
            return 1
        code, out = run(KIT, sys.executable, f"{KIT}/integ_tree.py", "publish")
        if code not in (0, 2):
            git(tree, "checkout", "-q", "-f", "--detach", tip)
            print(f"REFUSED: integ_tree.py publish: {out.strip()[-300:]}")
            return 1
        write_rows(LANDED, good, "a")
        if any(why in COUPLED for _, _, why in good):
            pooled = run(KIT, sys.executable, f"{KIT}/pad/repool.py", "--apply", "--rev", tip)[1].strip()
            print("pools: " + (pooled.splitlines() or [""])[-1])
    write_rows(REJECTED, stale + red, "a")
    done = set(entries) - set(queued)
    write_rows(MANIFEST, [e for e in rows() if e not in done], "w")
    print(f"LANDED {len(good)} of {len(entries)} at {git(tree, 'rev-parse', '--short', 'HEAD')[1].strip()}")
    return 1 if queued else 0


if __name__ == "__main__":
    sys.exit(main())
