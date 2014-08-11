PyPi
====

Several algorithms for arbitrary precision calculation of pi. Plus, how could I pass up that name? 
Based on Nick Craig-Wood's python implementations, but with my own gmpy2 changes. Includes a timing program to verify certain functions. I threw in some C++ code to see if gcc could do anything for speed. Any more speed increases would have to be done without Python. 

To do: 
- Better documentation 
- Multi-threading: a possibility?

Algorithms
----------
Details in the code.

**Machin:** Uses the formula `pi/4 = 4*arctan(1/5) - arctan(1/239)`. Features gmpy2's hardware level algorithm and an accelerated formula by Euler for arctan. 

**Chudnovsky:** Uses a very fast [rapidly convergent algorithm](http://en.wikipedia.org/wiki/Chudnovsky_algorithm). Includes a regular implementation with gmpy2 and a binary-splitting method with gmpy2.  

**Gauss-Legendre:** Uses a [second order convergence algorithm](https://en.wikipedia.org/wiki/Gauss-Legendre_algorithm) based on the arithmatic-geometric mean. Only `log2(n)` iterations are needed.

**Borwein:** Just for fun, PyPi includes [Borwein's 1984 algorithm](https://en.wikipedia.org/wiki/Borwein's_algorithm#Quartic_convergence_.281984.29) with quartic convergence. Not as fast as Gauss-Legendre though, probably because of the 4 divisions per iteration. 

Benchmarks
----------
Python

    Digits >>>          10,000        100,000        1,000,000    10,000,000    100,000,000
    ---------------------------------------------------------------------------------------
    Machin gmpy2        0.06 s        1.7 s          30.5 s       542.9 s       -
    Machin Taylor       0.4 s         38.9 s         -            -             -
    Machin Euler        0.3 s         34.4 s         -            -             -
    Chudnovksy regular  0.01 s        0.7 s          79.7 s       -             -
    Chudnovsky BS       0.004 s       0.1 s          1.6 s        28.9 s        432.3 s
    Gauss-Legendre      0.01 s        0.4 s          5.8 s        101.5 s       -
    Borwein             0.05 s        1.4 s          22.6 s       327.8 s       -
	
C++

    Digits >>>          10,000        100,000        1,000,000    10,000,000    100,000,000
    ---------------------------------------------------------------------------------------
    Chudnovsky BS       0.03 s        0.1 s          1.5 s        21.6 s        331.1 s
    	

	


Speed Optimizations (Python)
----------------------------
- Replaced `gmpy2.log2` with `math.log2`
- Replaced gmpy2 integer square root multiplied by `scale**2` with mpfr square root
    - 33% less time
- Use `mpz` exponentiation for `scale`
    - 50% less time


