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
    p,q = None, None
    if len(sys.argv) >=2:
        label=sys.argv[1]
        if "-h" in sys.argv or "--help" in sys.argv:
            print("\n\nUsage: python rsa.py [generate|encode|decode] [message]")
            print("  gen, generate              Generate the keys and save them in rsa_keys.txt")
            print("  enc, encode [msg]          Encrypt the message (default parameters: p=61879, q=40939, e=52079935)")
            print("  dec, decode [msg]          Decrypt the message (default parameters: p=61879, q=40939, e=52079935)")
            print("  sign [msg]                 Sign the message (default parameters: p=61879, q=40939, e=52079935)")
            print("  verify [signature] [msg]   Verify the signature (default parameters: p=61879, q=40939, e=52079935)")
            print("\nOptions:")
            print("  -h, --help            Show this help message and exit")
            print("  -e E                  Public exponent e")
            print("  -N N                  Modulus N")
            print("  -f                    Use the file rsa_keys.txt to get the parameters")
            exit(0)
        
        if "-N" in sys.argv and "-e" in sys.argv:
            N = int(sys.argv[sys.argv.index("-N")+1])
            e = int(sys.argv[sys.argv.index("-e")+1])
            rsa = RSA(None, None, e, N)

        elif "-f" in sys.argv and os.path.exists("rsa_keys.txt"):
            # To use the parameters from the file rsa_keys.txt
            with open("rsa_keys.txt", "r") as file:
                lines = file.readlines()
                p = int(lines[0].split('=')[1])
                q = int(lines[1].split('=')[1])
                e = int(lines[2].split('=')[1])
                rsa = RSA(p, q, e)
        else:
            # If nothing mentioned, use my saved parameters for RSA project
            p,q=61879,40939
            N=p*q
            phi_N=(p-1)*(q-1)
            e=52079935
            rsa = RSA(p, q, e)

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
            if "-N" in sys.argv:
                N = int(sys.argv[sys.argv.index("-N")+1])
            if "-e" in sys.argv:
                e = int(sys.argv[sys.argv.index("-e")+1])
            print(f"Encrypting using p={p}, q={q}, N={N}, e={e}")

            encrypted_str=rsa.encryption_str(sys.argv[2])
            print(f"Encrypted list: {encrypted_str}")

        elif label=="decode" or label=="dec" or label=="decrypt":
            if len(sys.argv) < 3:
                print("Please provide a message to decrypt")
                exit
            if p is None or q is None:
                print("Please provide p and q to decrypt")
                exit(1)
            print('Decrypting...')
            decrypted_str=rsa.decryption_str(sys.argv[2])
            print(f"Decrypted message: {decrypted_str}")
        
        elif label=="sign":
            if len(sys.argv) < 3:
                print("Please provide a message to sign")
                exit(1)
            print(f"Signing the message using d={rsa.d}...")
            signature = rsa.sign_str(sys.argv[2])
            print(f"Signature: {signature}")
    
        elif label=="verify":
            if len(sys.argv) < 4:
                print("Please provide a signature and the message to verify")
                exit(1)
            print(f"Verifying the signature using e={rsa.e}...")
            message = rsa.verify_str(sys.argv[2], sys.argv[3])
            print(f"Message: {message}")