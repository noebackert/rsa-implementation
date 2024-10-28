"""
Author: Noé Backert
Date: 2024-10-27
Brief: A class to add useful functions for the project.
"""
import random

class Toolbox:
    @staticmethod
    def is_prime(n: int) -> bool:
        """Return True if n is a prime number and return False otherwise"""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1): # only need to check up to the square root of n as it can't have factors larger than that
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Return the greatest common divisor of a and b"""
        while b > 0:
            a, b = b, a % b
        return a
    
    @staticmethod
    def generate_16bits_parameters_prime()->int:
        """Generate a prime number of 16 bits"""
        while True:
            n = random.randint(3, 2**16)
            if Toolbox.is_prime(n):
                return n
        
    @staticmethod
    def get_rsa_parameters()->tuple[int, int]:
        """Generate the parameters required for RSA encryption"""
        p = Toolbox.generate_16bits_parameters_prime()
        q = Toolbox.generate_16bits_parameters_prime()
        while p == q:
            q = Toolbox.generate_16bits_parameters_prime() # make sure p and q are different for security reasons
        return p, q

    @staticmethod
    def e_selection(phi_N:int)->int:
        """Select an integer e that is a relative prime number with phi_N and smaller than phi_N"""
        while True:
            e = random.randint(2, phi_N)
            if Toolbox.gcd(e, phi_N) == 1:
                return e
