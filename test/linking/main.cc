#include "shared.h"
#include "helper.h"


#if defined(BUILD_MONOLITHIC)
#define main    better_enum_linking_test_example_main
#endif

extern "C"
int main(void)
{
    better_enum_example_print(Channel::Red);

    return 0;
}
