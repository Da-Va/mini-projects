#include <iostream>
#include <optional>
#include <functional>
#include <type_traits>

template<typename T>
class Option {
    using StorageType = 
        std::conditional_t<
            std::is_reference<T>::value,
            std::optional<std::reference_wrapper<std::remove_reference_t<T>>>,
            std::optional<T>
        >;
    
    StorageType opt_; 

    static auto& get_(std::optional<T>& o) { return *o; }
    static auto& get_(std::optional<std::reference_wrapper<std::remove_reference_t<T>>>& o) { return o->get(); }
    
  public:    
    std::add_lvalue_reference_t<std::remove_reference_t<T>> get() {
        return get_(opt_);
    }
    std::add_lvalue_reference_t<std::remove_reference_t<T>> operator*() {
        return get_(opt_);
    }
    
    Option(std::add_lvalue_reference_t<std::remove_reference_t<T>> val) : opt_(val) { } ;
     
};
 
int main()
{
    int a = 12;
    
    
    
    Option<int&> aopt = a;
    Option<int&> aopt2 = aopt;

    std::cout << *aopt << '\n';
    *aopt2 = 20;
    std::cout << a << '\n';

}
