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
        if e*d % self.phi_N != 1 and e != 0 and d != 0:
            raise ValueError("e*d mod phi(N) must be equal to 1")
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


    def encryption_str(self, message:str)->str:
        """Encrypt the message using the public key (e,N)
        and return the encrypted message as a string"""
        separated_str=[message[i:i+3] for i in range(0, len(message), 3)]
        separated_str_hex=[hex(int.from_bytes(i.encode())) for i in separated_str]        
        encrypted_str=[int(self.encryption(int(i, 16))) for i in separated_str_hex]
        return encrypted_str
    
    def decryption_str(self, encrypted_message:list[int])->str:
        """Decrypt the encrypted message using the private key (d,N)
        and return the decrypted message as a string"""
        try:
            decrypted_str=[bytes.fromhex(hex(self.decryption(i))[2:]).decode() for i in encrypted_message]
        except ValueError:
            raise ValueError("The decryption key must not be valid")
        return "".join(decrypted_str)