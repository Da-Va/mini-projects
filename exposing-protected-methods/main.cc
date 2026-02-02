#include <iostream>

class A {
    int a;
public:
    A(int a) : a(a) {}
    int get() { return a; }
};

class B : protected A {
public:
    B(int a) : A(a) {}
    A& asA() { return *this; }
};

int main()
{
    A a(1);
    B b(10);
    std::cout << a.get() << '\n';
    std::cout << b.asA().get() << '\n';

    b.asA() = a;
    std::cout << a.get() << '\n';
    std::cout << b.asA().get() << '\n';
}