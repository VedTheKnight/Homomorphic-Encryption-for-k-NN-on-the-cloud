import random
import json

class ElGamal:
    def __init__(self,g,p):
        self.g = g
        self.p = p
        self.r = randint(1,100)
        self.h = power_mod(self.g, self.r, self.p)

    def get_public_key(self):
        return self.p,self.g,self.h

    def encrypt(self,plaintext):
        plaintext_tuple = json.loads(plaintext.decode())#tuple containing string message in index 0
        plaintext_int = int.from_bytes(plaintext_tuple[0].encode(), 'big')
        if(plaintext_int >= self.p):
            raise ValueError("Invalid plaintext! Please try again with a shorter message.")
        else:
            s = power_mod(plaintext_tuple[1][2], self.r, self.p)
            X = mod(plaintext_int * s, self.p)
            tuple = (int(self.h), int(X))
            ciphertext = json.dumps(tuple).encode()
            return ciphertext  # as binary

    def decrypt(self,ciphertext):
        ciphertext_tuple = json.loads(ciphertext.decode()) #tuple
        if (ciphertext_tuple[1] >= self.p):
            raise ValueError("Invalid plaintext! Please try again with a shorter message.")
        else:
            s = power_mod(ciphertext_tuple[0],self.r,self.p)
            s_inv = inverse_mod(s,self.p)
            plaintext_int = int(mod(ciphertext_tuple[1]*s_inv,self.p))
            plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
            return plaintext_bytes


bob = ElGamal(51,356946343358715584277268939833200898638115523809875957978296404324882635483239652693185396510297393318766806270336708224092728306993230856774545615633749902372048048265678686975662568763138587679678543730494365670031920127769412328695198054176711730984373627043994772365720336206479390798908230342619)
bob_public_key = bob.get_public_key()

alice = ElGamal(51,356946343358715584277268939833200898638115523809875957978296404324882635483239652693185396510297393318766806270336708224092728306993230856774545615633749902372048048265678686975662568763138587679678543730494365670031920127769412328695198054176711730984373627043994772365720336206479390798908230342619)
message = ("hello",bob_public_key)

plaintext = json.dumps(message).encode() #is a binary type
ciphertext = alice.encrypt(plaintext)

print(bob.decrypt(ciphertext).decode())