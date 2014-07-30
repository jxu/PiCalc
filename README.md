PyPi
====

Several algorithms for arbitrary precision calculation of pi. Plus, how could I pass up that name? 
Based on Nick Craig-Wood's python implementations, but with my own gmpy2 changes. Older versions have non-fixed point math. Includes a cheesy timing program so I don't rewrite the code multiple times to try to get performance. 

To do: 

- Better documentation 
- Multi-threading: a possibility?

Formulas
--------
Details in the code.

**Machin:** Uses the formula `pi/4 = 4*arctan(1/5) - arctan(1/239)`. Features gmpy2's hardware level algorithm and an accelerated formula by Euler for arctan. 

**Chudnovsky:** Uses a very fast rapidly convergent algorithm that can be seen here: http://en.wikipedia.org/wiki/Chudnovsky_algorithm. Includes a regular implementation with gmpy2 and a binary-splitting method with gmpy2.  

**Gauss-Legendre:** Uses a second order convergence algorithm based on the arithmatic-geometric mean. Only `log2(n)` iterations are needed.


Benchmarks
----------

**Machin**

gmpy2 arctan: 	10,000 digits in 0.06 s,	100,000 digits in 1.8 s, 	1,000,000 digits in 31.2 s

Decimal arctan:	10,000 digits in 0.4 s,		100,000 digits in 38.9 s

Euler arctan:	10,000 digits in 0.3 s,		100,000 digits in 34.4 s


**Chudnovsky**

Regular:		10,000 digits in 0.01 s,	100,000 digits in 0.7 s,	1,000,000 digits in 79.7 s	

Bs:				10,000 digits in 0.004 s,	100,000 digits in 0.1 s,	1,000,000 digits in 1.6 s,		10,000,000 digits in 28.9 s, 	100,000,000 digits in 432.3 s

**Gauss-Legendre**

				10,000 digits in 0.01 s, 	100,000 digits in 0.4 s, 	1,000,000 digits in 5.8 s,		10,000,000 digits in 101.5 s

Speed Optimizations 
-------------------
- Replaced `gmpy2.log2` with `math.log2`
- Replaced gmpy2 integer square root multiplied by `scale**2` with mpfr square root
    - 33% less time
- Use `mpz` exponentiation for `scale`
    - 50% less time


