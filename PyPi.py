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
        zero = Decimal(10)**-(digits+10)
        
        def atan(x):
            # Calculate arctan(1/x)
            x = Decimal(x)
            current_value = Decimal(0)
            divisor = 1
            x_squared = x * x
            current_term = 1 / x    
                
            while True:
                # Thanks to Raymond Hettinger for solving issues
                current_value += current_term / divisor
                
                divisor += 2
                # 1/((x^(n+2)) 
                current_term /= -x_squared
   
                if abs(current_term) <= zero:
                    break
            
            return current_value
        
        def accelerated_atan(x):
            x = Decimal(x)
            x_squared_plus_1 = x * x + 1
            current_term = x / x_squared_plus_1
            two_loop_count = Decimal(2)
            divisor = x_squared_plus_1

            
            current_value = current_term    # For coefficient 1/1
            while True:     
                
                divisor = (two_loop_count + 1) * x_squared_plus_1
                current_term *= two_loop_count / divisor
                if abs(current_term) <= zero:
                    break
                current_value += current_term
                
                two_loop_count += 2
                
            return current_value 
            
        if use_accelerated_atan:
            pi_fourths = 4*accelerated_atan(5) - accelerated_atan(239)
        else:
            pi_fourths = 4*atan(5) - atan(239)
        pi = 4*pi_fourths
        
        print(pi)
                
                
                
start_time = time.time()               
                
machin(digits=1000, use_accelerated_atan=True)
# Credit: rogeriopvl
print("%s seconds" % (time.time() - start_time))