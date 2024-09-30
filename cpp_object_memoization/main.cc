#include <iostream>
#include <memory>
#include <unordered_map>
#include <map>

template<typename T>
struct Memoizer{

    template<typename... Args>
    static std::shared_ptr<T> create(Args... args)
    {
        static std::map<std::tuple<Args...>, std::shared_ptr<T>> mem;

        std::tuple<Args...> key = {args...};
        
        if(mem.count(key) == 0) {
            mem[key] = std::make_shared<T>(args...);
        }

        return mem[key];
    }
};



struct A {
    A(int a, int b) {};
};

int main()
{
    
    auto a1 = Memoizer<A>::create(1,1);
    auto a2 = Memoizer<A>::create(1,2);
    auto a1_alt = Memoizer<A>::create(1,1);

    std::cout << a1 << '\n';
    std::cout << a2 << '\n';
    std::cout << a1_alt << '\n';

}