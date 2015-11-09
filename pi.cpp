// Pi calculations program (rewrite in C++ and gmp for speed)
// Compile with -O3
#include "gmpxx.h"
#include <iostream>
#include <math.h>

// Deal with this later
void *__gxx_personality_v0;
void *_Unwind_Resume;

const int EXTRA_DIGITS = 10; // Margin

void bs(const int a, const int b, mpz_class &Pab, mpz_class &Qab, mpz_class &Tab)
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
            Pab = 6*a-5;
            Pab *= 2*a-1;
            Pab *= 6*a-1;
            //mpz_class a_cubed;
            //mpz_pow_ui(a_cubed.get_mpz_t(), a.get_mpz_t(), 3);

            Qab = C_cubed_over_24;
            Qab *= a; Qab *= a; Qab *= a;
        }
        Tab = Pab * (13591409 + 545140134*a);

        if (a&1)
            Tab *= -1;

    }
    else
    {
        // Binary splitting
        mpz_class Pam, Qam, Tam;
        mpz_class Pmb, Qmb, Tmb;

        int m = (a+b) / 2;

        bs(a, m, Pam, Qam, Tam);
        bs(m, b, Pmb, Qmb, Tmb);

        Pab = Pam * Pmb;
        Qab = Qam * Qmb;
        Tab = Qmb * Tam + Pam * Tmb;
    }
    //std::cout << "P Q T: " << Pab << ", " << Qab << ", " << Tab << std::endl;
};

mpz_class chudnovsky(int digits)
{
    digits += EXTRA_DIGITS;

    const double digits_per_term = log10(151931373056000ll); // log(C_cubed_over_24 / 72);
    int N = int(digits / digits_per_term) + 1;

    std::cout << "Binary splitting max: " << N << std::endl;

    mpz_class P, Q, T;
    bs(0, N, P, Q, T);


    mpz_class one;
    mpz_ui_pow_ui(one.get_mpz_t(), 10, digits);
    mpz_class sqrt_10005 = one * 10005;
    mpz_sqrt(sqrt_10005.get_mpz_t(), sqrt_10005.get_mpz_t());

    mpz_class pi = (Q * 426880 * sqrt_10005) / T;

    //int bin_digits = int(digits * log2(10));
    //int precision = bin_digits + EXTRA_DIGITS;
    //std::cout << "Precision: " << precision << std::endl;
    //mpf_set_default_prec(precision);

    //mpf_class Q_float(Q);
    //mpf_class T_float(T);

    //mpf_class sqrt_10005;
    //mpf_sqrt_ui(sqrt_10005.get_mpf_t(), 10005);
    //std::cout << sqrt_10005 << std::endl; // Correct precision

    //mpf_class pi = (Q_float * 426880 * sqrt_10005) / T_float;
    return pi;
}

int main()
{
    const int digits = 10000000;

    std::cout.precision(digits + 10);
    //std::cout << std::fixed;

    mpz_class pi = chudnovsky(digits);
    //std::cout << pi << std::endl;

    return 0;
}
