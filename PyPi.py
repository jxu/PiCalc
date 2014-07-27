# Pi generation program
from decimal import *
import gmpy2, time, math
from gmpy2 import mpz, mpfr

def machin(digits, use_gmpy2=False, use_accelerated_atan=True):
    
    if use_gmpy2:
        
        bits_precision = int(gmpy2.log2(10) * digits)
        # Precision + 20 bits for safety
        gmpy2.get_context().precision = bits_precision + 20
        
        # Automatic type conversion (int to mpfr in division)
        one_5th = mpfr("1") / 5
        one_239th = mpfr("1") / 239
        
        pi_fourths = 4*gmpy2.atan(one_5th) - gmpy2.atan(one_239th)
        pi = 4*pi_fourths
        
        return pi
        
    else:   
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
        
        def accelerated_atan(x):
            # Calculate arctan(1/x) using Euler's formula 
            # Combines 2 terms, 1 division and 2 multiplications per loop
            x_squared_plus_1 = x * x + 1
            current_term = scale * x // x_squared_plus_1
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
            
        if use_accelerated_atan:
            pi_fourths = 4 * accelerated_atan(5) - accelerated_atan(239)
        else:
            pi_fourths = 4 * atan(5) - atan(239)
        pi = 4 * pi_fourths
        
        return pi
                
                
                
def chudnovsky(digits, use_bs=True):
    # 20 safety digits because lots of calculations
    scale = mpz(10**(digits+20))    

    bits_precision = int(gmpy2.log2(10) * digits)

    # gmpy2 precision ~ 20 digits
    gmpy2.get_context().precision = bits_precision + 67
    
    if not use_bs:
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
        
        total_sum = 13591409 * a_sum + 545140134 * b_sum
        pi = (426880 * gmpy2.isqrt(10005 * scale**2) * scale) // total_sum
 

        return gmpy2.div(mpfr(pi), scale)
    
    else:
        # Use binary splitting
        digits += 20
        C = mpz(640320)
        C_cubed_over_24 = C**3 // 24
        def bs(a, b):
            # Shamelessly stolen from craig-wood.com
            # Like this entire program
            
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

        print("hi")
        digits_per_term = math.log10(C_cubed_over_24/72) 
        print("bye")

        N = int(digits/digits_per_term + 1)
        P, Q, T = bs(mpz(0), mpz(N))
        scale = mpz(10**digits)
        z = (Q*426880*gmpy2.isqrt(10005 * scale**2)) // T
        
        return mpfr(z) / scale
        


start_time = time.time()               
                
chudnovsky(digits=10000000)
# Credit: rogeriopvl
print("%s seconds" % (time.time() - start_time))

