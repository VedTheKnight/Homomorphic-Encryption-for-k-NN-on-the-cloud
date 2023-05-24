import random
import json
#this version works for small messages - error in prime generation not k-bit
#issue in encryption -- very slow for large values!
class Paillier:

    def __init__(self,k = 1024):
        self.k = k
        #useful function
        def L(x,n):
            return (x-1)//n #note this is floor division in order to avoid overflow error

        while(True):
            #two distinct primes such that gcd(pq,(p-1)(q-1)) = 1
            self.p = int(random_prime(2**self.k))
            while(True):
                self.q = int(random_prime(2**self.k))
                if(self.p==self.q or gcd(self.p*self.q,(self.p-1)*(self.q-1)) != 1):continue
                else:break
            #computes n=pq
            self.n = self.p*self.q
            #computes lambda = lcm(p-1,q-1) ---> private key
            self.l = lcm(self.p-1,self.q-1)
            #computes g=random number in {1,2,3,..n^2-1}
            self.g = randint(1,self.n**2-1)
            #computes mu - modular multiplicative inverse
            if(gcd(L(int(power_mod(self.g,self.l,self.n**2)),self.n),self.n)==1):
                self.mu = inverse_mod(int(L(int(power_mod(self.g,self.l,self.n**2)),self.n)),self.n)
                break
            else:
                continue

        #random number in {1,2,3,...,n-1}
        self.r = randint(1,self.n-1)


    def get_public_key(self):
        return self.n,self.g

    def encrypt(self,plaintext):
        plaintext_int = int.from_bytes(plaintext, 'big')

        if(plaintext_int >= int(self.n)):
            raise ValueError("Invalid Message! Please try again with a smaller message.")
        else:
            #ciphertext_int = int(mod(int(plaintext_tuple[2]**plaintext_int)*int(self.r**plaintext_tuple[1]),plaintext_tuple[1]**2))#integer
            ciphertext_int = int(mod(power_mod(self.g, plaintext_int, self.n ** 2) * power_mod(self.r,self.n,self.n ** 2),self.n ** 2))
            ciphertext_bytes = ciphertext_int.to_bytes((ciphertext_int.bit_length() + 7) // 8, 'big')
            return ciphertext_bytes

    def decrypt(self,ciphertext):
        ciphertext_int = int.from_bytes(ciphertext, 'big')

        # useful function
        def L(x, n):
            return (x - 1) // n #note this is floor division in order to avoid overflow error

        if(ciphertext_int>=self.n**2):
            raise ValueError("Invalid Message! Please try again with a smaller message.")

        else:
            pm = power_mod(int(ciphertext_int),self.l,self.n*self.n)
            L_val = L(pm,self.n)
            plaintext_int = int(mod(int(L_val)*self.mu,self.n))
            plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
            return plaintext_bytes


