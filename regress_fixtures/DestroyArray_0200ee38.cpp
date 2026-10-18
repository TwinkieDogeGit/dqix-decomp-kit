#include <globaldefs.h>

typedef void (*ElementDestructor0200ee38)(void*);
extern "C" void func_0200efb8();

// USA: func_0200ee38
extern "C" ARM void func_0200ee38(unsigned char* begin, unsigned char* end,
    unsigned int stride, ElementDestructor0200ee38 destroy)
{
    try {
        if (end > begin) {
            do {
                end -= stride;
                destroy(end);
            } while (end > begin);
        }
    } catch (...) {
        func_0200efb8();
    }
}
