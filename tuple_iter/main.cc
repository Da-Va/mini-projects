#include <iostream>
#include <tuple>

#include <memory>

template<class... Args>
void foo(Args... args) {
        std::cout << sizeof...(Args) << '\n';
}

int main()
{
    foo();
    
    int* a = new int[10];

}