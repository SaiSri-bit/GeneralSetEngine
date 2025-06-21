pi = 3.141592653589793
e = 2.718281828459045

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def sin(x, terms=10):
    result = 0
    for n in range(terms):
        term = ((-1)**n) * (x**(2*n + 1)) / factorial(2*n + 1)
        result += term
    return result

def cos(x, terms=10):
    result = 0
    for n in range(terms):
        term = ((-1)**n) * (x**(2*n)) / factorial(2*n)
        result += term
    return result

def exp(x, terms=10):
    result = 0
    for n in range(terms):
        term = (x**n) / factorial(n)
        result += term
    return result
