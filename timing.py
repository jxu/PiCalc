# Timing module

import gmpy2, time, math

digits = 100000

scale = 10**digits  # Decimal precision
gmpy2.get_context().precision = int(math.log2(10) * digits) # Binary precision

def start_timer():
    global start_time   # Lazy coding
    start_time = time.time()
    
def print_timer():
    print("%s s" % (time.time() - start_time))
    
# Integer and floating point division
def division_test():
    start_timer()
    for i in range(1000):
        x = scale // 3
    print_timer()
    
    start_timer()
    for i in range(1000):
        x = gmpy2.mpfr(1) / 3
    print_timer()
    
    start_timer()
    for i in range(1000):
        x = gmpy2.mpfr(1) / gmpy2.mpfr(3)
    print_timer()


# Integer and floating point square root
def squareroot_test():
    start_timer()
    for i in range(100):
        x = gmpy2.isqrt(3 * scale**2)
    print_timer()
    
    start_timer()
    for i in range(100):
        x = gmpy2.sqrt(gmpy2.mpfr(3))
    print_timer()
  
  
squareroot_test()
    





