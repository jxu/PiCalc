// Pi calculations program (rewrite in C++ for speed)
// Compile with -O3 for best results

#include <boost/multiprecision/gmp.hpp>
#include <iostream>
#include <math.h>
#include <tuple>

using namespace boost::multiprecision;

namespace boost{ namespace multiprecision{

template <unsigned Digits10>
class gmp_float;

typedef number<gmp_float<0> >     mpf_float;
}}

namespace boost{ namespace multiprecision{

class gmp_int;

typedef number<gmp_int >         mpz_int;

}}

typedef std::tuple<mpz_int, mpz_int, mpz_int>   return_values;


return_values bs(const mpz_int &a, const mpz_int &b)
{
    const mpz_int C_cubed_over_24 = 10939058860032000ll; // C = 640320;

    if (b - a > 1000000)
    {
        std::cout << "Current a, b: " << a << " " << b << std::endl;
    }

    mpz_int Pab, Qab, Tab;

    if (b - a == 1)
    {
        if (a == 0)
        {
            Pab = Qab = 1;
        }
        else
        {
            Pab = (6*a-5) * (2*a-1) * (6*a-1);
            Qab = a*a*a * C_cubed_over_24;

        }
        Tab = Pab * (13591409 + 545140134*a);

        if (a & 1)
        {
            Tab *= -1;
        }
    }
    else
    {
        mpz_int m;
        m = (a+b) / 2;

        mpz_int Pam, Qam, Tam;
        std::tie(Pam, Qam, Tam) = bs(a, m);

        mpz_int Pmb, Qmb, Tmb;
        std::tie(Pmb, Qmb, Tmb) = bs(m, b);

        Pab = Pam * Pmb;
        Qab = Qam * Qmb;
        Tab = Qmb * Tam + Pam * Tmb;
    }
    // std::cout << "P Q T: " << Pab << ", " << Qab << ", " << Tab << std::endl;

    return_values return_tuple(Pab, Qab, Tab);

    return return_tuple;
};

mpf_float chudnovsky(int digits)
{
    // binary splitting

    const double digits_per_term = log10(151931373056000ll); // log(C_cubed_over_24 / 72);

    mpz_int N = mpz_int((digits + 20) / digits_per_term + 1);

    std::cout << "Iterations: " << N << std::endl;

    mpf_float::default_precision(digits + 20);
    mpz_int P, Q, T;

    std::tie(P, Q, T) = bs(0, N);

    mpf_float Q_float = mpf_float(Q);
    mpf_float T_float = mpf_float(T);

    const mpf_float float_10005 = 10005;

    return (Q_float * 426880 * sqrt(float_10005)) / T_float;
}

int main()
{
    int digits = 1000000000; // int limit is 2,147,483,647

    std::cout.precision(digits + 10);
    std::cout << std::fixed;

    mpf_float pi = chudnovsky(digits);

    // std::cout << pi << std::endl;

    return 0;
}
