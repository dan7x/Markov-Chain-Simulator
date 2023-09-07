#include <Eigen/Dense>
#include <vector>
#include <tuple>
#include <iostream>
#include "eigenutil.h"

std::vector<std::tuple<float, Eigen::VectorXd>> EigenUtil::get_eigenvals_vecs(Eigen::MatrixXd matrix_in){
    Eigen::EigenSolver<Eigen::MatrixXd> eigensolver;
    eigensolver.compute(matrix_in); // Solve

    // Get real eigenvalues and vectors (stn dist guaranteed to exist)
    Eigen::VectorXd eigen_values = eigensolver.eigenvalues().real();
    Eigen::MatrixXd eigen_vectors = eigensolver.eigenvectors().real();

    // std::cout << "val" << std::endl << eigen_values << std::endl;
    // std::cout << "vec" << std::endl << eigen_vectors << std::endl;

    // Result
    std::vector<std::tuple<float, Eigen::VectorXd>> eigen_vectors_and_values; 

    for(int i=0; i<eigen_values.size(); i++){
        std::tuple<float, Eigen::VectorXd> vec_and_val(eigen_values[i], eigen_vectors.row(i));
        eigen_vectors_and_values.push_back(vec_and_val);
    }

    // Sort result
    std::sort(eigen_vectors_and_values.begin(), eigen_vectors_and_values.end(), 
        [&](const std::tuple<float, Eigen::VectorXd>& a, const std::tuple<float, Eigen::VectorXd>& b) -> bool{ 
            return std::get<0>(a) <= std::get<0>(b); 
    });

    // Reset original eigenvec/val to sorted order
    // int index = 0;
    // for(auto const vect : eigen_vectors_and_values){
    //     eigen_values(index) = std::get<0>(vect);
    //     eigen_vectors.row(index) = std::get<1>(vect);
    //     index++;
    // }

    return eigen_vectors_and_values;
}
