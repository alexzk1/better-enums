// This file was generated automatically.

// Hello, World!
//
// Download enum.h, then compile this program:

#include <iostream>
#include "enum.h"

BETTER_ENUM(Word, int, Hello, World)


#if defined(BUILD_MONOLITHIC)
#define main    better_enum_1_hello_example_main
#endif

extern "C"
int main(void)
{
    std::cout << (+Word::Hello)._to_string() << ", "
              << (+Word::World)._to_string() << "!"
              << std::endl;

    return 0;
}

// Run it, and you should see the output "Hello, World!"
//
// Congratulations, you have just created your first Better Enum!
