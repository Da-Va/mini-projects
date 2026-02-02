#include "class.hpp"


template class A<int>;

void B::foo() {
    Eigen::MatrixXd M(10,10); 
    M.setRandom();
    Eigen::FullPivLU<Eigen::MatrixXd> decomp_lu(M);
    Eigen::JacobiSVD<Eigen::MatrixXd> decomp_svd(M);
    std::cout << decomp_lu.cols() << '\n';
    std::cout << decomp_svd.cols() << '\n';
} 
