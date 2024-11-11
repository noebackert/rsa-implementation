"""
Author: Noé Backert
Date: 2024-10-27
Brief: A class representing the RSA.
"""

from tools.modular_integer import ModularInteger
from tools.toolbox import Toolbox

class RSA:
    """A class to manage RSA key generation, encryption and decryption algorithms."""
    def __init__(self, p:int = None, q:int = None, e:int = None, N:int = None):
        """
        Initialize the RSA object with either:
        - p, q, and e to calculate d, N, and Phi(N),
        - or N and e for encryption-only mode.
        """
        if p is not None and q is not None and e is not None:
            self.p = p
            self.q = q
            self.N = p * q
            self.phi_N = (p - 1) * (q - 1)
            self.e = e
            self.d = ModularInteger(self.e, self.phi_N).mult_inverse().n

        elif N is not None and e is not None:
            self.N = N
            self.e = e
            self.d = None
            self.p = None
            self.q = None
            self.phi_N = None

        else:
            raise ValueError("Invalid parameters. Provide either (p, q, e) or (N, e).")

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
    