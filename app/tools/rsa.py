"""
Author: Noé Backert
Date: 2024-10-27
Brief: A class representing the RSA.
"""

from tools.modular_integer import ModularInteger
from tools.toolbox import Toolbox

class RSA:
    """A class to manage RSA key generation, encryption and decryption algorithms."""
    def __init__(self, p:int, q:int, e:int=0, d:int=0):
        """Initialize the RSA object with the parameters p, q, e and d, 
        if e and d are not provided, they will be generated using the generating
        functions created in the Toolbox module"""
        self.p = p
        self.q = q
        self.N = p*q
        self.phi_N = (p-1)*(q-1)
        if e == 0:
            self.e = Toolbox.e_selection(self.phi_N)
        else:
            self.e = e
        if d == 0:
            self.d = ModularInteger(self.e, self.phi_N).mult_inverse().n
        else:
            self.d = d

    def encryption(self, message:int)->int:
        """Encrypt the message using the public key (e,N)
        and return the encrypted message as an integer"""
        return ModularInteger(message, self.N).square_and_multiply(self.e).n
    
    def decryption(self, cipher:int)->int:
        """Decrypt the cipher using the private key (d,N)
        and return the decrypted message as an integer"""
        return ModularInteger(cipher, self.N).square_and_multiply(self.d).n

