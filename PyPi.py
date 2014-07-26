# Pi generation program
from decimal import *
import gmpy2

def machin(digits, use_gmpy2=False, use_accelerated_atan=True):
    
    if use_gmpy2:
        
        bits_precision = int(gmpy2.log2(10) * digits)
        # Precision + 20 bits for safety
        gmpy2.get_context().precision = bits_precision + 20
        
        # Automatic type conversion (int to mpfr in division)
        one_fifth = gmpy2.mpfr("1") / 5
        one_239th = gmpy2.mpfr("1") / 239
        
        pi_fourths = 4*gmpy2.atan(one_fifth) - gmpy2.atan(one_239th)
        pi = 4*pi_fourths
        
        print(pi)
        
    else:   
        getcontext().prec = digits + 5     # 10 digit safety
        
        def atan(x):
            # Calculate arctan(1/x)
            x = Decimal(x)
            current_value = Decimal(0)
            divisor = 1
            x_squared = x * x
            current_term = 1 / x
            zero = Decimal(10)**-(digits+10)
            
                
            while True:
                # Thanks to Raymond Hettinger for solving issues
                current_value += current_term / divisor
                
                divisor += 2
                current_term = -current_term / x_squared

                
                if abs(current_term) < zero:
                    break
            

            return current_value
        
        def accelerated_atan(x):
            ...
            
        if use_accelerated_atan:
            pi_fourths = 4*accelerated_atan(5) - accelerated_atan(239)
        else:
            pi_fourths = 4*atan(5) - atan(239)
        pi = 4*pi_fourths
        
        print(pi)
                
                
                

machin(digits=1000000, )