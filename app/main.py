"""
Author: Noé Backert
Date: 2024-10-27
Brief: Main file, to test the RSA encryption and decryption
"""
import sys
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


    message = "Hello World!"
    encrypted_str = rsa.encryption_str(message)
    print(f"Encrypted message: {encrypted_str}")

    decrypted_str = rsa.decryption_str(encrypted_str)
    print(f"Decrypted message: {decrypted_str}")

    if len(sys.argv) >=2:
        label=sys.argv[1]
        print(label)
        if label=="encode" or label=="enc":
            if len(sys.argv) < 3:
                print("Please provide a message to encrypt")
                exit(1)
            encrypted_str=rsa.encryption_str(sys.argv[2])
            print(f"Encrypted list: {encrypted_str}")

        elif label=="decode" or "dec":
            print('decoding...')
            if len(sys.argv) < 3:
                print("Please provide a message to decrypt")
                exit
            list_encrypted_str=sys.argv[2].replace('[','').replace(']','').replace(' ','')
            list_encrypted_int=[int(i) for i in list_encrypted_str.split(',')]
            decrypted_str=rsa.decryption_str(list_encrypted_int)
            print(f"Decrypted message: {decrypted_str}")