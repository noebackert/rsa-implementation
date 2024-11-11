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
        if p is not None and q is not None:
            self.p = p
            self.q = q
            self.N = p * q
            self.phi_N = (p - 1) * (q - 1)
            if e is not None:
                if Toolbox.gcd(e, (p-1)*(q-1)) != 1:
                    raise ValueError("The public exponent e must be coprime with (p-1)*(q-1)")
            else:
                # Choose a random public exponent e
                e = Toolbox.e_selection((p-1)*(q-1))
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

    def to_int_list(self, message:str)->list[int]:
        """Convert a string to a list of integers"""
        separated_str=[message[i:i+3] for i in range(0, len(message), 3)]
        separated_str_hex=[hex(int.from_bytes(i.encode())) for i in separated_str]
        separated_str_int=[int(i, 16) for i in separated_str_hex] 
        return separated_str_int

    def encryption_str(self, message:str)->str:
        """Encrypt the message using the public key (e,N)
        and return the encrypted message as a string"""
        separated_str_int=self.to_int_list(message)        
        encrypted_str=str([int(self.encryption(i)) for i in separated_str_int])
        return encrypted_str
    
    def decryption_str(self, encrypted_message:str)->str:
        """Decrypt the encrypted message using the private key (d,N)
        and return the decrypted message as a string"""
        # format the encrypted message
        list_encrypted_str=encrypted_message.replace('[','').replace(']','').replace(' ','').split(',')
        list_encrypted_int=[int(i) for i in list_encrypted_str]
        try:
            decrypted_str=[bytes.fromhex(hex(self.decryption(i))[2:]).decode() for i in list_encrypted_int]
        except ValueError:
            raise ValueError("The decryption key must not be valid")
        return "".join(decrypted_str)
    

    def sign_str(self, message:str)->str:
        """Sign the message using the private key (d,N)
        and return the signature as an integer"""
        separated_str_int=self.to_int_list(message)        
        sign=str([int(self.decryption(int(i))) for i in separated_str_int])
        return sign
    
    def verify_str(self, signature:str, message:str)->str:
        """Verify the signature using the public key (e,N)
        and return the verified message as a string, 
        the message to be verified and a boolean indicating the verification"""
        list_encrypted_str=signature.replace('[','').replace(']','').replace(' ','').split(',')
        list_encrypted_int=[int(i) for i in list_encrypted_str]
        try:
            decrypted_str=[bytes.fromhex(hex(self.encryption(i))[2:]).decode() for i in list_encrypted_int]
            complete_decrypted_str="".join(decrypted_str)
        except ValueError:
            raise ValueError("The decryption key must not be valid")
        return complete_decrypted_str, message, complete_decrypted_str==message
    