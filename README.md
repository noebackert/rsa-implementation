# RSA Implementation for course INSE6110-Concordia

## How to run ?

    ./.venv/Scripts/activate

    python ./rsa.py -h

## How to use it ?

**Usage:**

    python rsa.py [generate|encode|decode] [message] (options)
>
    gen, generate               # Generate the keys and save them in rsa_keys.txt

    enc, encode [msg]           # Encrypt the message 
                                (default parameters: p=61879, q=40939, e=52079935)

    dec, decode [msg]           # Decrypt the message 
                                (default parameters: p=61879, q=40939, e=52079935)

    sign [msg]                  # Sign a message
                                (default parameters: p=61879, q=40939, e=52079935)

    verify [signature] [msg]    # Verify someone's signature
Options:

    -h, --help            # Show this help message and exit
    -N N                  # Choose the mod N
    -e E                  # Choose a public exponent e
    -f                    # Use the parameters stored in the file rsa_keys.txt

# Example to share a secret :

```py
python rsa.py gen
```
Then share the public key e,N

```py
python rsa.py enc <message> -e <e> -N <N>
python rsa.py dec <message> -f 
```

# Warning

The use of python3.10 or higher is required because of the use of type annotations inside the functions. (List[int])