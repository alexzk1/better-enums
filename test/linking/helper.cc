#include <iostream>
#include "shared.h"
#include "helper.h"

void better_enum_example_print(Channel channel)
{
    std::cout << Channel::_name() << "::" << channel._to_string() << std::endl;
    std::cout << Channel::_size() << std::endl;
}
