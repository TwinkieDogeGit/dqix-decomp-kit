#include <globaldefs.h>
#include "System/Interrupts.h"

#if defined(jpn)
#define data_0211127c data_02110f1c
#endif

struct DMAOrTimerResponse
{
    DMACompletionCallback callback;
    unsigned int stayEnabledAfter;
    int userdata;
};

extern DMAOrTimerResponse data_0211127c[8];

inline DMACompletionCallback& CallbackByIndex(int n, int base = 0)
{
    return *(DMACompletionCallback*)((unsigned int)&data_0211127c[base].callback + n * sizeof(DMAOrTimerResponse));
}

inline unsigned int& ShouldStayEnabledByIndex(int n, int base = 0)
{
    return *(unsigned int*)((unsigned int)&data_0211127c[base].stayEnabledAfter + n * sizeof(DMAOrTimerResponse));
}

inline int& CallbackUserdataByIndex(int n, int base = 0)
{
    return *(int*)((unsigned int)&data_0211127c[base].userdata + n * sizeof(DMAOrTimerResponse));
}

// USA: func_020c6c48
ARM void SetTimerOverflowCallback(int timer, DMACompletionCallback callback, int userdata)
{
    CallbackByIndex(timer, 4) = callback;
    CallbackUserdataByIndex(timer, 4) = userdata;
    EnableSpecificInterrupts(IRQ_MASK_TIMER_N_OVERFLOW(timer));
    ShouldStayEnabledByIndex(timer, 4) = true;
}
