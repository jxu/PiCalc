PyPi
====

Several algorithms for arbitrary precision calculation of pi. Plus, how could I pass up that name? 
Based on Nick Craig-Wood's python implementations, but with my own non-fixed-point and gmpy2 changes. 

To do: Improve documentation in code

Formulas
--------
Details in the code.

**Machin** 

Uses the formula `pi/4 = 4*arctan(1/5) - arctan(1/239)`. Features gmpy2's hardware level algorithm and an accelerated formula by Euler for arctan. 

**Chudnovsky**

Uses a very fast rapidly convergent algorithm that can be seen here: http://en.wikipedia.org/wiki/Chudnovsky_algorithm



Benchmarks
----------

**Machin**

gmpy2: 100,000 digits in  2.5 seconds

Decimal arctan: 10,000 digits in 0.5 seconds, 100,000 digits in 47.4 seconds


