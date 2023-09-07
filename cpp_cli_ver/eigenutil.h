#include <vector>
#include <tuple>
#include <Eigen/Dense>

#ifndef EIGENUTIL_H
#define EIGENUTIL_H

class EigenUtil{

    public:
        static std::vector<std::tuple<float, Eigen::VectorXd>> get_eigenvals_vecs(Eigen::MatrixXd matrix_in);

};

#endif
