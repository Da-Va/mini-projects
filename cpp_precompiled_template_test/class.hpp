#include <eigen3/Eigen/Dense>

#include <iostream>

template <typename T>
class A {
public:
    void foo();
};

template<typename T>
void A<T>::foo() {
    Eigen::MatrixXd M(10,10); 
    M.setRandom();
    Eigen::FullPivLU<Eigen::MatrixXd> decomp_lu(M);
    Eigen::JacobiSVD<Eigen::MatrixXd> decomp_svd(M);
    std::cout << decomp_lu.cols() << '\n';
    std::cout << decomp_svd.cols() << '\n';
} 

class B {
public:
    void foo();    
};
// void B::foo() {
//     Eigen::MatrixXd M(10,10); 
//     M.setRandom();
//     Eigen::FullPivLU<Eigen::MatrixXd> decomp_lu(M);
//     Eigen::JacobiSVD<Eigen::MatrixXd> decomp_svd(M);
//     std::cout << decomp_lu.cols() << '\n';
//     std::cout << decomp_svd.cols() << '\n';
// } 

extern template class A<int>;