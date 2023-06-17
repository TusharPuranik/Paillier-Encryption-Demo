# Paillier-Encryption-Demo

## Paillier Encryption Python Implementation

This project presents a Python implementation of the Paillier encryption scheme, a public-key cryptosystem known for its homomorphic properties. The Paillier encryption algorithm allows secure computation on encrypted data, enabling operations such as addition and multiplication without the need to decrypt the underlying values. This repository provides a practical demonstration of Paillier encryption by showcasing its encryption, decryption, and homomorphic properties using Python.

## Features:

- Key Generation: The project includes functionality to generate public and private keys required for Paillier encryption.
- Encryption and Decryption: It provides methods to encrypt plaintext messages using the generated public key and decrypt the encrypted ciphertext using the corresponding private key.
- Homomorphic Operations: The Paillier encryption scheme enables homomorphic addition and multiplication on encrypted data. This implementation showcases how to perform these operations on encrypted values without revealing the plaintext.
- Secure Communication: The project demonstrates how Paillier encryption can be utilized for secure communication between multiple parties, ensuring the confidentiality of the exchanged information.

## Usage:

- Generate Keys: Use the provided key generation module to generate the public and private keys required for encryption and decryption.
- Encrypt and Decrypt: Utilize the encryption and decryption modules to securely encrypt plaintext messages and decrypt the corresponding ciphertext.
- Homomorphic Operations: Explore the functionality to perform homomorphic addition and multiplication on encrypted values, preserving privacy while obtaining meaningful results.
- Secure Communication Example: Refer to the provided example code to understand how Paillier encryption can be applied to achieve secure communication between multiple parties.

## Dependencies:
The project relies on the following Python libraries:

- PyCryptodome: A library for cryptographic primitives and algorithms.
- NumPy: A fundamental package for scientific computing with Python.
- Flask: Python's lightweight web framework for building powerful, scalable, and elegant web applications.
