"""
Author: Noé Backert
Date: 2024-10-27
Brief: Main file, to test the RSA encryption and decryption
"""

from tools import ModularInteger
from tools import Toolbox
from tools import RSA

if __name__=="__main__":
    p, q =61879, 40939
    N=p*q
    phi_N=(p-1)*(q-1)
    e=Toolbox.e_selection(phi_N)
    #e=52079935

    d=ModularInteger(e, phi_N).mult_inverse().n
    print(f"d={d}")
    print(f"e*d mod phi(N)={ModularInteger(e, phi_N)*d}")

    print(f"p={p}, q={q}, N={N}, phi(N)={phi_N}, e={e}, d={d}")
    test = 2
    test_exp = 16
    print(f"{test}^{test_exp} mod {N} = {ModularInteger(test, N).square_and_multiply(test_exp)}")


    rsa = RSA(p, q)
    message = 1234    
    encrypted_message = rsa.encryption(message)
    print(f"Encrypted message: {encrypted_message}")
    decrypted_message = rsa.decryption(encrypted_message)
    print(f"Decrypted message: {decrypted_message}")

    message = "Hello, World!"
    