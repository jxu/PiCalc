PyPi
====

Several algorithms for arbitrary precision calculation of pi. Plus, how could I pass up that name? 
Based on Nick Craig-Wood's python implementations, but with my own gmpy2 changes. Older versions have non-fixed point math. Included a cheesy timing program so I don't rewrite the code multiple times to try to get performance. 

To do: 

- Improve documentation in code

- Multi-threading: a possibility?

Formulas
--------
Details in the code.

**Machin** 

Uses the formula `pi/4 = 4*arctan(1/5) - arctan(1/239)`. Features gmpy2's hardware level algorithm and an accelerated formula by Euler for arctan. 

**Chudnovsky**

Uses a very fast rapidly convergent algorithm that can be seen here: http://en.wikipedia.org/wiki/Chudnovsky_algorithm. Includes a regular implementation with gmpy2 and a binary-splitting method with gmpy2.  



Benchmarks
----------

**Machin**

gmpy2 arctan: 	10,000 digits in 0.06 s,	100,000 digits in 1.8 s, 	1,000,000 digits in 31.2 s

Decimal arctan:	10,000 digits in 0.4 s,		100,000 digits in 38.9 s

Euler arctan:	10,000 digits in 0.3 s,		100,000 digits in 34.4 s


**Chudnovsky**

Regular:		10,000 digits in 0.01 s,	100,000 digits in 0.8 s,	1,000,000 digits in 81.1 s	

Bs:				10,000 digits in 0.005 s,	100,000 digits in 0.1 s,	1,000,000 digits in 2.3 s,		10,000,000 digits in 57.4 s

Speed Optimizations 
-------------------

- Replaced `gmpy2.log2` with `math.log2`

- Replaced gmpy2 integer square root multiplied by `scale**2` with mpfr square root
    - 33% less time



