"""
Author: Noé Backert
Date: 2024-10-27
Brief: RSA file, to test the RSA encryption and decryption
"""
import sys
import os
from tools import ModularInteger
from tools import Toolbox
from tools import RSA


if __name__=="__main__":
    if len(sys.argv) >=2:
        label=sys.argv[1]
        if "-h" in sys.argv or "--help" in sys.argv:
            print("Usage: python rsa.py [generate|encode|decode] [message]")
            print("Options:")
            print("  -h, --help            Show this help message and exit")
            print("  -p P                  Prime number p")
            print("  -q Q                  Prime number q")
            print("  -e E                  Public exponent e")
            print("  -f                    Use the file rsa_keys.txt to get the parameters")
            print("  gen, generate         Generate the keys and save them in rsa_keys.txt")
            print("  enc/encode [msg]      Encrypt the message (default parameters: p=61879, q=40939, e=52079935)")
            print("  dec/decode [msg]      Decrypt the message (default parameters: p=61879, q=40939, e=52079935)")
            exit(0)
        if "-p" in sys.argv and "-q" in sys.argv:
            #To be able to choose the parameters p and q
            p = int(sys.argv[sys.argv.index("-p")+1])
            if Toolbox.is_prime(p)==False:
                print("p must be a prime number")
                exit(1)
            q = int(sys.argv[sys.argv.index("-q")+1])
            if Toolbox.is_prime(q)==False:
                print("q must be a prime number")
                exit(1)
            if "-e" in sys.argv:
                e = int(sys.argv[sys.argv.index("-e")+1])
            else:
                phi_N=(p-1)*(q-1)
                e = Toolbox.e_selection(phi_N)
                
        elif "-f" in sys.argv and os.path.exists("rsa_keys.txt"):
            # To use the parameters from the file rsa_keys.txt
            with open("rsa_keys.txt", "r") as file:
                lines = file.readlines()
                p = int(lines[0].split('=')[1])
                q = int(lines[1].split('=')[1])
                e = int(lines[2].split('=')[1])
        else:
            # If nothing mentioned, use my saved parameters for RSA project
            p,q=61879,40939
            N=p*q
            phi_N=(p-1)*(q-1)
            e=52079935

        rsa=RSA(p, q, e, 0)
        if label=="generate" or label=="gen":
            p, q = Toolbox.get_rsa_parameters()
            print(f"p={p}, q={q}")
            rsa = RSA(p, q)
            print(f"e={rsa.e}, d={rsa.d}, N={rsa.N}, phi(N)={rsa.phi_N}")
            with open("rsa_keys.txt", "w") as file:
                file.write(f"p={p}\nq={q}\ne={rsa.e}")
            print("Keys saved in rsa_keys.txt")

        elif label=="encode" or label=="enc" or label=="encrypt":
            if len(sys.argv) < 3:
                print("Please provide a message to encrypt")
                exit(1)
            print(f"Encrypting using p={p}, q={q}, e={e}")
            encrypted_str=rsa.encryption_str(sys.argv[2])
            print(f"Encrypted list: {encrypted_str}")

        elif label=="decode" or "dec" or "decrypt":
            if len(sys.argv) < 3:
                print("Please provide a message to decrypt")
                exit
            print('Decrypting...')
            list_encrypted_str=sys.argv[2].replace('[','').replace(']','').replace(' ','')
            list_encrypted_int=[int(i) for i in list_encrypted_str.split(',')]
            decrypted_str=rsa.decryption_str(list_encrypted_int)
            print(f"Decrypted message: {decrypted_str}")
    