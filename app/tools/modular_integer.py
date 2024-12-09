"""
Author: Noé Backert
Date: 2024-10-27
Brief: A class to manage modular arithmetic and number theory in a simpler way.
"""
from tools.toolbox import Toolbox

class ModularInteger:
    """A class to manage modular arithmetic and number theory for course INSE6110@Concordia."""
    def __init__(self, n: int, mod: int) -> None:
        try:
            if not isinstance(n, int) or not isinstance(mod, int):
                raise TypeError("n and mod must be integers")
            if mod <= 0:
                raise ValueError("mod must be a positive integer")
            self.n = n % mod
            self.mod = mod
        except Exception as e:
            print(e)       
            print("ModularInteger object not created")
            exit(1)
    
    def __add__(self, other: 'ModularInteger') -> 'ModularInteger':
        return ModularInteger((self.n + other.n) % self.mod, self.mod)
    
    def __sub__(self, other: 'ModularInteger') -> 'ModularInteger':
        return ModularInteger((self.n - other.n) % self.mod, self.mod)
    
    def __mul__(self, other) -> 'ModularInteger':
        if isinstance(other, ModularInteger):
            return ModularInteger((self.n * other.n) % self.mod, self.mod)
        elif isinstance(other, int):
            return ModularInteger((self.n * other) % self.mod, self.mod)
        else:
            raise TypeError("Unsupported type for multiplication")

    def __str__(self) -> str:
        return f"{self.n} mod {self.mod}"
    
    def mult_inverse_naive(self) -> 'ModularInteger':
        """Return the multiplicative inverse of self if it exists, None otherwise
        naive version (first I tried, but very long for 16 bits integers)"""
        if Toolbox.gcd(self.n, self.mod) != 1:
            return None
        else:
            for i in range(1, self.mod):
                if (self.n * i) % self.mod == 1:
                    return ModularInteger(i, self.mod)
    
    def mult_inverse(self) -> 'ModularInteger':
        """Return the multiplicative inverse of self if it exists using the extended euclidian algorithm, None otherwise"""
        if Toolbox.gcd(self.n, self.mod) != 1:
            return None
        else:
            x,y,d,r,s,t=1,0,self.n,0,1,self.mod
            while t>0:
                q = d//t
                u = x-q*r
                v = y-q*s
                w = d-q*t
                x,y,d,r,s,t=r,s,t,u,v,w
            return ModularInteger(x, self.mod)
    
    def square_and_multiply(self,exp: int)-> 'ModularInteger':
        """Define power function using square and multiply algorithm
        parameters:
        - exp: the exponent to which the number is raised"""
        bin_exp = bin(exp)[2:] # bin returns a string starting with '0b'
        N = ModularInteger(self.n, self.mod)
        for i in range(1,len(bin_exp)):
            if bin_exp[i]=='0':
                N = N*N 
            else:
                N=N*N*self.n
        return N
    
