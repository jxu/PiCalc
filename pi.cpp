// Pi calculations program (rewrite in C++ and gmp for speed)
// Compile with -O3
#include "gmpxx.h"
#include <iostream>
#include <math.h>

// Deal with this later
void *__gxx_personality_v0;
void *_Unwind_Resume;

const int EXTRA_DIGITS = 50; // Margin

void bs(const mpz_class &a, const mpz_class &b, mpz_class &Pab, mpz_class &Qab, mpz_class &Tab)
{
    const mpz_class C_cubed_over_24("10939058860032000"); // C = 640320;

    if (b - a == 1)
    {
        if (a == 0)
        {
            Pab = Qab = 1;
        }
        else
        {
            Pab = (6*a-5) * (2*a-1) * (6*a-1);
            mpz_class a_cubed;
            mpz_pow_ui(a_cubed.get_mpz_t(), a.get_mpz_t(), 3);
            Qab = a_cubed * C_cubed_over_24;
        }
        Tab = Pab * (13591409 + 545140134*a);

        if (mpz_odd_p(a.get_mpz_t()))
        {
            Tab *= -1;
        }
    }
    else
    {
        // Binary splitting
        mpz_class m = (a+b) / 2;

        mpz_class Pam, Qam, Tam;
        bs(a, m, Pam, Qam, Tam);

        mpz_class Pmb, Qmb, Tmb;
        bs(m, b, Pmb, Qmb, Tmb);

        Pab = Pam * Pmb;
        Qab = Qam * Qmb;
        Tab = Qmb * Tam + Pam * Tmb;
    }
    // std::cout << "P Q T: " << Pab << ", " << Qab << ", " << Tab << std::endl;
};

mpf_class chudnovsky(int digits)
{
    int bin_digits = int(digits * log2(10));
    const double digits_per_term = log10(151931373056000ll); // log(C_cubed_over_24 / 72);

    mpz_class N = int((bin_digits + EXTRA_DIGITS) / digits_per_term + 1);

    std::cout << "Binary splitting max: " << N << std::endl;

    int precision = bin_digits + EXTRA_DIGITS;
    std::cout << "Precision: " << precision << std::endl;
    mpf_set_default_prec(precision);

    mpz_class P, Q, T;
    bs(0, N, P, Q, T);

    mpf_class Q_float(Q);
    mpf_class T_float(T);

    mpf_class sqrt_10005;
    mpf_sqrt_ui(sqrt_10005.get_mpf_t(), 10005);
    //std::cout << sqrt_10005 << std::endl; // Correct precision

    mpf_class pi = (Q_float * 426880 * sqrt_10005) / T_float;
    return pi;
}

int main()
{
    const int digits = 1000000;

    std::cout.precision(digits + 10);
    //std::cout << std::fixed;

    mpf_class pi = chudnovsky(digits);
    //std::cout << pi << std::endl;

    return 0;
}
