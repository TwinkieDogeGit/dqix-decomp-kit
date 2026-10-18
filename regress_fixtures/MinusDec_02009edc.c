#include <globaldefs.h>

typedef struct decimal {
    char sgn;
    char unused;
    short exp;
    struct {
        unsigned char length;
        unsigned char text[32];
        unsigned char unused;
    } sig;
} decimal;

// USA: func_02009edc
ARM void func_02009edc(decimal* z, const decimal* x, const decimal* y) {
    int zlen, dexp;
    unsigned char *ib, *i, *ie;
    const unsigned char *jb, *j, *jn;

    *z = *x;

    if (y->sig.text[0] == 0)
        return;

    zlen = z->sig.length;
    if (zlen < y->sig.length)
        zlen = y->sig.length;

    dexp = z->exp - y->exp;
    zlen += dexp;

    if (zlen > 32)
        zlen = 32;

    while (z->sig.length < zlen)
        z->sig.text[z->sig.length++] = 0;

    ib = z->sig.text;
    i = ib + zlen;

    if (y->sig.length + dexp < zlen)
        i = ib + (y->sig.length + dexp);

    jb = y->sig.text;
    j = jb + (i - ib - dexp);
    jn = j;

    while (i > ib && j > jb) {
        --i;
        --j;
        if (*i < *j) {
            unsigned char* k = i - 1;
            while (*k == 0)
                --k;
            while (k != i) {
                --*k;
                ++k;
                *k += 10;
            }
        }
        *i -= *j;
    }

    if (jn - jb < y->sig.length) {
        int roundDown = 0;
        if (*jn < 5)
            roundDown = 1;
        else if (*jn == 5) {
            const unsigned char* je = y->sig.text + y->sig.length;

            for (j = jn + 1; j < je; ++j)
                if (*j != 0)
                    goto done;

            i = ib + (jn - jb) + dexp - 1;

            if (*i & 1)
                roundDown = 1;
        }
        if (roundDown) {
            if (*i < 1) {
                unsigned char* k = i - 1;
                while (*k == 0)
                    --k;
                while (k != i) {
                    --*k;
                    ++k;
                    *k += 10;
                }
            }
            *i -= 1;
        }
    }

done:
    for (i = ib; *i == 0; ++i) {
    }

    if (i > ib) {
        unsigned char dl = (unsigned char)(i - ib);
        z->exp -= dl;
        ie = ib + z->sig.length;
        for (; i < ie; ++i, ++ib)
            *ib = *i;
        z->sig.length -= dl;
    }

    ib = z->sig.text;
    for (i = ib + z->sig.length; i > ib;) {
        --i;
        if (*i != 0)
            break;
    }
    z->sig.length = (unsigned char)(i - ib + 1);
}
