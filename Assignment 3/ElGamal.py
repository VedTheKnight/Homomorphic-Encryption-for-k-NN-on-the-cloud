import random

class ElGamal:
    def __init__(self,g,p):
        self.g = g
        self.p = p
        self.r = randint(1,100)
        self.h = power_mod(self.g, self.r, self.p)

    def get_public_key(self):
        return self.p,self.g,self.h

    def encrypt(self,plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')
        if(plaintext_int >= self.p):
            raise ValueError("Invalid plaintext! Please try again with a shorter message.")
        else:
            s = power_mod(self.h, self.r, self.p)
            X = int(mod(plaintext_int * s, self.p))
            ciphertext_bytes = X.to_bytes((X.bit_length() + 7) // 8, 'big')
            return ciphertext_bytes

    def decrypt(self,ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        if (ciphertext_int >= self.p):
            raise ValueError("Invalid plaintext! Please try again with a shorter message.")
        else:
            s = power_mod(self.h,self.r,self.p)
            s_inv = inverse_mod(s,self.p)
            plaintext_int = int(mod(ciphertext_int*s_inv,self.p))
            plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
            return plaintext_bytes


