import random
import socket
import json
import sage
import numpy as np
import math

#common parameters for the simulation
d = 50
m = 10000

#socket information
PORT1 = 65432  # data owner port
PORT2 = 65433  # cloud server port
SERVER = socket.gethostname()
ADDR1 = (SERVER, PORT1)  # data owner
ADDR2 = (SERVER, PORT2)  # cloud server


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
            while(gcd(self.g,self.n)!=1):
                self.g = randint(1, self.n ** 2 - 1)

            #computes mu - modular multiplicative inverse
            if(gcd(L(int(power_mod(self.g,self.l,self.n**2)),self.n),self.n)==1):
                self.mu = inverse_mod(int(L(int(power_mod(self.g,self.l,self.n**2)),self.n)),self.n)
                break
            else:
                continue



    def get_public_key(self):
        return self.n,self.g

    def encrypt(self,plaintext):

        # random number in {1,2,3,...,n-1}
        self.r = randint(1, self.n - 1)

        if(plaintext >= int(self.n)):
            raise ValueError("Invalid Message! Please try again with a smaller message.")
        else:
            ciphertext = int(mod(power_mod(self.g, plaintext, self.n ** 2) * power_mod(self.r,self.n,self.n ** 2),self.n ** 2))

            return ciphertext

    def decrypt(self,ciphertext):
        # useful function
        def L(x, n):
            return (x - 1) // n #note this is floor division in order to avoid overflow error

        #deleting this line since A_q is very large and always fails this
        #testing what happens on allowing this
        if(ciphertext>=self.n**2):
            raise ValueError("Invalid Message! Please try again with a smaller message.")

        #else:
        pm = power_mod(int(ciphertext),self.l,self.n*self.n)
        L_val = L(pm,self.n)
        plaintext = int(mod(int(L_val)*self.mu,self.n))
        return plaintext

def sendAndReceiveQuerywithKey(message):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initializes the client object
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # a useful line in debugging to prevent OSError: [Errno 98] Address already in use

    # interaction with the data owner

    client.connect(ADDR1)  # establishes connection with the data owner's port
    client.sendall(json.dumps(message).encode())  # sends the query to the data owner for modification
    print("[Query User]Sent the encrypted query - E_pk(q)")

    A_q = json.loads(client.recv(32768).decode())

    print("[Query User]Received A_q")
    for i in range(len(A_q)):
        print(f"A_q {i} {A_q[i]} ")

    client.close()  # closes the connection with the data owner

    return A_q

def sendAndReceiveIndexSet(q_dash):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initializes the client object
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # a useful line in debugging to prevent OSError: [Errno 98] Address already in use

    # interaction with the cloud server
    client.connect(ADDR2)  # establishes connection with the cloud server's port
    #send_data(client, json.dumps(q_dash).encode(), 4096) #set the buffer size as 4096
    client.sendall(json.dumps(q_dash).encode())
    print("[Query User]Sent the encrypted query - q_dash")

    index_set = json.loads(client.recv(32768).decode())
    client.close()

    return index_set

def send_data(socket, data, buffer_size):
    total_sent = 0
    while total_sent < len(data):
        chunk = data[total_sent:total_sent + buffer_size]
        total_sent += socket.send(chunk)


#generate a query - This can be taken as input from user - for now we initialize it to an arbitrary placeholder value
#q = [random.randint(-10, 10) for _ in range(d)]
q = [4, -3, -2, -3, 7, 6, -6, -9, -2, 5, 5, -9, -2, -9, -10, -9, -10, 4, 7, 8, 3, 2, 8, 0, 4, -8, 8, 6, -5, 6, 9, -6, -8, 1, 2, -10, -4, -9, -10, 6, -2, 1, -4, -6, -7, 6, -4, -8, -8, 8]
#we scale our query -- an attempt
#for i in range(len(q)):
    #q[i]*= 1000

print("[Query User]Generated random query")

#Generate public key and private key of Homomorphic Crypto-system
paillier = Paillier(k=16)

public_key = paillier.get_public_key()
print(f"Public Key {public_key}")

#encrypt the query point to send to the Data Owner
q_cipher = [paillier.encrypt(x) for x in q]
print(f"[Query User]Encrypted the query : {q_cipher}")

#we want to send both the public key and the q_cipher to the data owner so that he can generate A_q
message = [public_key,q_cipher]

#Send the encrypted query point to the Data Owner
A_q = sendAndReceiveQuerywithKey(message)

#Now decrypts using the secret paillier key
q_dash = [paillier.decrypt(x) for x in A_q]
print("[Query User]Computed q_dash")

print(q_dash)

#Send q_dash to the cloud server and receive the index set after k-NN computation
index_set = sendAndReceiveIndexSet(q_dash)

print(f"Index Set : {index_set}")