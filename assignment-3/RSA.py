import random

class RSA:
    def __init__(self, k=0, e=65537,N=0):
        self.k = k
        self.e = e
        self.N = N
        self.p = 0
        self.q = 0

        if(self.N==0):
            # Pre generated primes
            first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                                 31, 37, 41, 43, 47, 53, 59, 61, 67,
                                 71, 73, 79, 83, 89, 97, 101, 103,
                                 107, 109, 113, 127, 131, 137, 139,
                                 149, 151, 157, 163, 167, 173, 179,
                                 181, 191, 193, 197, 199, 211, 223,
                                 227, 229, 233, 239, 241, 251, 257,
                                 263, 269, 271, 277, 281, 283, 293,
                                 307, 311, 313, 317, 331, 337, 347, 349]

            def nBitRandom(n):
                return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)

            def getLowLevelPrime(n):
                '''Generate a prime candidate divisible
                by first primes'''
                while True:
                    # Obtain a random number
                    pc = nBitRandom(n)

                    # Test divisibility by pre-generated
                    # primes
                    for divisor in first_primes_list:
                        if pc % divisor == 0 and divisor ** 2 <= pc:
                            break
                    else:
                        return pc

            def isMillerRabinPassed(mrc):
                '''Run 20 iterations of Rabin Miller Primality test'''
                maxDivisionsByTwo = 0
                ec = mrc - 1
                while ec % 2 == 0:
                    ec >>= 1
                    maxDivisionsByTwo += 1

                def trialComposite(round_tester):
                    if pow(round_tester, ec, mrc) == 1:
                        return False
                    for i in range(maxDivisionsByTwo):
                        if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                            return False
                    return True

                # Set number of trials here
                numberOfRabinTrials = 20
                for i in range(numberOfRabinTrials):
                    round_tester = random.randrange(2, mrc)
                    if trialComposite(round_tester):
                        return False
                return True

            while True:
                prime_candidate = getLowLevelPrime(self.k)
                if not isMillerRabinPassed(prime_candidate):
                    continue
                else:
                    self.p = prime_candidate
                    break

            while True:
                while True:
                    self.q = getLowLevelPrime(self.k)
                    if (self.p != self.q): break

                if not (isMillerRabinPassed(self.q) and gcd(self.e, (self.p - 1) * (self.q - 1) == 1)):
                    continue
                else:
                    break

    def get_public_key(self):
        self.N = self.p * self.q
        return (self.N,self.e)

    def encrypt(self, plaintext):
        #plaintext_int = int(plaintext.decode('utf-8'))
        plaintext_int = int.from_bytes(plaintext, 'big')
        if(plaintext_int>=self.N):
            print("Invalid message! Please try again with a different message!")
        else:
            M = power_mod(plaintext_int,self.e,self.N)
            #M_bytes = str(M).encode('utf-8')
            M_bytes = M.to_bytes((M.bit_length() + 7) // 8, 'big')
            return M_bytes

    def decrypt(self,ciphertext):
        #ciphertext_int = int(ciphertext.decode('utf-8'))
        ciphertext_int = int.from_bytes(ciphertext, 'big')
        if (ciphertext_int >= self.N):
            print("Invalid message! Please try again with a different message!")
        else:
            d = inverse_mod(self.e, (self.p-1)*(self.q-1))
            m = power_mod(ciphertext_int,d, self.N)
            #m_bytes = str(m).encode('utf-8')
            m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
            return m_bytes



