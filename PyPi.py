# Pi generation program
from decimal import *
import gmpy2, time

def machin(digits, use_gmpy2=False, use_accelerated_atan=True):
    
    if use_gmpy2:
        
        bits_precision = int(gmpy2.log2(10) * digits)
        # Precision + 20 bits for safety
        gmpy2.get_context().precision = bits_precision + 20
        
        # Automatic type conversion (int to mpfr in division)
        one_5th = gmpy2.mpfr("1") / 5
        one_239th = gmpy2.mpfr("1") / 239
        
        pi_fourths = 4*gmpy2.atan(one_5th) - gmpy2.atan(one_239th)
        pi = 4*pi_fourths
        
        print(pi)
        
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
                current_term = current_term // -x_squared
   
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
                current_term = current_term // divisor
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
        
        print(pi)
                
                
                
start_time = time.time()               
                
machin(digits=100000, use_accelerated_atan=True)
# Credit: rogeriopvl
print("%s seconds" % (time.time() - start_time))

