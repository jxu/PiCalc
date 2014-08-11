# Pi generation program
# Based on an article on craig-wood.com with some gmpy2 changes
from decimal import *
import gmpy2, time, math
from gmpy2 import mpz, mpfr

def machin_gmpy2(digits):
    # Precision + 20 bits for safety
    gmpy2.get_context().precision = int(math.log2(10) * digits) + 20
        
    one_5th = mpfr("1") / 5
    one_239th = mpfr("1") / 239
        
    pi_fourths = 4*gmpy2.atan(one_5th) - gmpy2.atan(one_239th)
    pi = 4*pi_fourths
        
    return pi


def machin(digits):
    getcontext().prec = digits + 10     # 10 digit safety
    scale = 10**(digits + 10)           # fixed point
        
    def atan(x):
        # Calculate arctan(1/x)
        # 2 divisions per loop
        current_value = 0
        divisor = 1
        x_squared = x * x
        current_term = scale // x    

        while True:
            # Thanks to Raymond Hettinger for solving issues
            current_value += current_term // divisor
            
            divisor += 2
            # 1/((x^(n+2)) 
            current_term //= -x_squared

            if current_term == 0:
                break
        return Decimal(current_value) / scale
    
    pi_fourths = 4 * atan(5) - atan(239)
    return pi_fourths * 4
    

def machin_euler(digits):
    getcontext().prec = digits + 10     
    scale = 10**(digits + 10) 
    
    def accelerated_atan(x):
        # Calculate arctan(1/x) using Euler's formula 
        # Combines 2 terms, 1 division and 2 multiplications per loop
        x_squared_plus_1 = x * x + 1
        current_term = (scale * x) // x_squared_plus_1
        two_loop_count = 2
        divisor = x_squared_plus_1

        current_value = current_term    # For coefficient 1/1
        
        while True:        
            divisor = (two_loop_count + 1) * x_squared_plus_1
            current_term *= two_loop_count 
            current_term //= divisor
            
            if current_term == 0:
                break
            current_value += current_term
            
            two_loop_count += 2
            
        return Decimal(current_value) / scale 
            
    pi_fourths = 4 * accelerated_atan(5) - accelerated_atan(239)
        
    return pi_fourths * 4


def chudnovsky(digits):
    # 20 safety digits because lots of calculations (only about 3 are needed)
    scale = 10**(mpz(digits+20))  

    gmpy2.get_context().precision = int(math.log2(10) * (digits + 20)) 
    
    k = mpz(1)
    a_k = scale
    a_sum = scale
    b_sum = mpz(0)
    C = mpz(640320)
    C_cubed_over_24 = C**3 // 24
    
    while True:
        a_k *= -(6*k-5) * (2*k-1) * (6*k-1)
        a_k //= k**3 * C_cubed_over_24
        a_sum += a_k
        b_sum += k * a_k
        k += 1
        if a_k == 0:
            break
    
    total_sum = mpfr(13591409 * a_sum + 545140134 * b_sum)
    pi = (426880 * gmpy2.sqrt(mpfr(10005))) / total_sum
 
    return pi*scale

                
def chudnovsky_bs(digits):
    gmpy2.get_context().precision = int(math.log2(10) * (digits + 20))
     
    # Use binary splitting
    digits += 20
    C = mpz(640320)
    C_cubed_over_24 = C**3 // 24
    def bs(a, b):
        # a(a) = +/- (13591409 + 545140134a)
        # p(a) = (6a-5)(2a-1)(6a-1)
        # b(a) = 1
        # q(a) = a^3 * C_cubed_over_24
        
        if b - a == 1:
            # Directly compute
            if a == 0:
                Pab = Qab = mpz(1)
            else:
                Pab = (6*a-5) * (2*a-1) * (6*a-1)
                Qab = a**3 * C_cubed_over_24
            Tab = Pab * (13591409 + 545140134*a)
            if a & 1:
                Tab *= -1 
        
        else:
            m = (a+b) // 2  # Midpoint
            # Recursively divide and conquer
            Pam, Qam, Tam = bs(a, m)
            Pmb, Qmb, Tmb = bs(m, b)
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
            
        return Pab, Qab, Tab

    digits_per_term = math.log10(C_cubed_over_24/72) 

    N = int(digits/digits_per_term + 1)
    P, Q, T = bs(mpz(0), mpz(N))
    Q, T = mpfr(Q), mpfr(T)

    return (Q * 426880 * gmpy2.sqrt(mpfr(10005))) / T


def gauss_legendre(digits):
    gmpy2.get_context().precision = int(math.log2(10) * (digits + 5))
    
    iterations = int(math.log2(digits)) 
    
    # Direct translation of algorithm
    a = mpfr(1)
    b = 1 / gmpy2.sqrt(mpfr(2))
    t = mpfr(1)/4
    x = mpfr(1)


    for i in range(iterations):
        y = a
        a = (a + b) / 2
        b = gmpy2.sqrt(b * y)
        t = t - x * (y-a)**2
        x = 2 * x
        
    pi = ((a+b)**2) / (4*t)
    return pi

def borwein(digits):
    gmpy2.get_context().precision = int(math.log2(10) * (digits + 10))
    
    sqrt_2 = gmpy2.sqrt(mpfr(2))
    a_n = sqrt_2
    b_n = mpz(0)
    p_n = 2 + sqrt_2
    
    while True:
        sqrt_a_n = gmpy2.sqrt(a_n)
        a_n1 = (sqrt_a_n + 1/sqrt_a_n) / 2
        b_n1 = (1 + b_n) * sqrt_a_n / (a_n + b_n)
        p_n1 = (1 + a_n1) * p_n * b_n1 / (1 + b_n1)
        
        if p_n1 == p_n:
            break
        
        a_n = a_n1
        b_n = b_n1
        p_n = p_n1
        
    return p_n
     
def main():
    start_time = time.time()               
             
    print(borwein(100))
    
    print("%s seconds" % (time.time() - start_time))
    
main()

