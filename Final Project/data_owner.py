import random
import socket
import json
import numpy as np
import math
import sage

#common parameters for the simulation
d=50
m = 10000

#socket information
PORT1 = 65432 #port for the data owner
SERVER = socket.gethostname() #gets the ip-address of the device
ADDR1 = (SERVER,PORT1)

# initializing positive security parameters
c = random.randint(1,10)
e = random.randint(1,10)
n = d+c+e+1
D = [[]]

#Helper Function to get a permutation function
def getPerm(n):

    perm = [i for i in range(n)]

    for i in range(n):

        j = random.randint(0, n - 1)
        while(j==i):
            j = random.randint(0,n-1)

        temp = perm[i]
        perm[i] = perm[j]
        perm[j] = temp

    return perm

#Helper Function to generate invertible matrix M
def generateInvertibleMatrix(n):

    # Generate a random matrix of size n x n with very small values this will limit size of A_q
    matrix = np.random.randint(10,size = (n,n))
    #matrix = np.random.rand(n,n) / 10000000000000

    # Check if the matrix is invertible
    while np.linalg.matrix_rank(matrix) < n:
        #matrix = np.random.rand(n,n) / 10000000000000
        matrix = np.random.randint(10, size=(n, n))

    print(f"Matrix M : {matrix}")
    return matrix

#Obtains the dataset from database.txt
def getD():
    D = []
    f = open("database.txt", "r")
    for x in f:
        row = [int(num) for num in x.strip().split()]
        D.append(row)

    return D

#generates the private key of the Data Owner
def KeyGen():

    # generating a random invertible matrix of dimension nxn
    M = generateInvertibleMatrix(n)

    #generating random vectors as a part of our private key
    S = [random.random()*1000 for _ in range(d+1)]
    t = [random.random()*1000 for _ in range(c)]

    #generating a permutation function perm of n numbers
    perm = getPerm(n)

    return [S,t,perm,M]

#encrypts single data point
def computeEncryptedDatapoint(D,i,Key,v):
    p = D[i]

    mag_p = 0
    for i in p:
        mag_p += i*i
    mag_p = math.sqrt(mag_p)

    S = Key[0]
    t = Key[1]
    perm = Key[2]
    M = Key[3]

    p_intermediate = []
    p_encrypted = [0 for i in range(n)]

    #calculating p_intermediate which is p_encrypted before permutation and multiplication by M_inv
    for i in range(d):
        p_intermediate.append(S[i] - 2*p[i])

    p_intermediate.append(S[d]+mag_p*mag_p)

    for i in t:
        p_intermediate.append(i)

    for i in v:
        p_intermediate.append(i)

    #permutation
    c = 0

    for element in p_intermediate:
        p_encrypted[perm[c]] = element
        c+=1

    p_encrypted = np.array(p_encrypted)
    p_encrypted = p_encrypted.reshape(1,-1)

    M = np.array(M)
    M = M.reshape(n,n)

    M_inv = np.linalg.inv(M)

    p_encrypted = np.matmul(p_encrypted,M_inv)

    return p_encrypted

#encrypts the whole database
def encryptData(D,Key):

    D_encrypted = [[]]
    for i in range(m):
        v = [random.random() * 1000 for _ in range(e)]

        p_enc_i = computeEncryptedDatapoint(D, i, Key, v)

        D_encrypted.append(p_enc_i)

    return D_encrypted

#Receive Encrypt and Send encrypted query to and from Query User with modifications. ONE TIME FUNCTION NEED TO INC. RE-USABILITY
def queryRES(Key):
    dataOwner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates the data owner socket
    dataOwner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # a useful line in debugging to prevent OSError: [Errno 98] Address already in use
    dataOwner.bind(ADDR1)
    dataOwner.listen()
    print(f"[DATA OWNER]Data Owner is listening on {ADDR1}")

    # creating this loop allows the data owner to interact with multiple clients in sequential order
    while True:
        conn, addr = dataOwner.accept()  # starts a connection between client and data owner
        print(f"[DATA OWNER]{addr} connected. ")

        connected = True
        while connected:
            message= json.loads(conn.recv(32768).decode())  # message obtained and converted to a list
            public_key = message[0]
            query_encrypted = message[1]
            print("[Data Owner]Obtained message and deconstructed it successfully")

            #computations
            A_q = queryEncrypt(query_encrypted,Key,public_key)

            print(f"[Data Owner]Successfully computed A_q")

            for i in range(n):
                print(f"A_q {i} {A_q[i]} ")

            '''
            A_q.append(-1) #the terminating character
            for i in range(n):
                print(f"A_q {i} {A_q[i]} ")

            for i in range(len(A_q)):
                message = [A_q[i]] # to prevent overflow
                conn.sendall(json.dumps(message).encode())  # converts the list back into binary format and sends it back to client as data
            '''

            conn.sendall(json.dumps(A_q).encode())

            print("[Data Owner]Sent the encrypted query back to the query user")
            connected = False

        print(f"[DATA OWNER]{addr} has disconnected.")
        break

#Paillier Encryption Function
def encrypt(public_key, plaintext):

    n = public_key[0]
    g = public_key[1]

    # random number in {1,2,3,...,n-1}
    r = randint(1, n - 1)

    if (plaintext >= int(n)):
        raise ValueError("Invalid Message! Please try again with a smaller message.")
    else:
        ciphertext = int(mod(power_mod(g, int(plaintext), int(n ** 2)) * power_mod(r, int(n), int(n ** 2)), int(n ** 2)))

        return ciphertext

#Query Modification
def queryEncrypt(query_encrypted,Key,public_key):
    #checks if the query is valid
    if(len(query_encrypted)!=d):
        return False

    #get necessary parameters
    perm = Key[2]
    #create inverse permutation list
    inverse_perm = [0 for i in perm]
    for i in range(len(perm)):
        inverse_perm[perm[i]] = i

    M = Key[3]
    c = len(Key[1])
    R_q = [int(random.random()*10) for i in range(c)] #c-dimensional random vector between one and ten
    beta_q = random.random()/10000000000000  # random small positive number
    A_q = [0 for i in range(n)]


    #compute n-dimensional encrypted vector A_q
    for i in range(n):
        A_q[i] = encrypt(public_key,0)

        for j in range(n):
            t = inverse_perm[j]
            if t < d:
                phi = beta_q*M[i][j] # [0,1]*[0,10]/10000
                A_q[i] = int(A_q[i]*pow(query_encrypted[t],phi))
            elif t == d:
                phi = beta_q * M[i][j] # [0,1]*[0,10]/10000
                A_q[i] = int(A_q[i] * encrypt(public_key,phi))
            elif t < d+c+1:
                w = t-d-1
                phi = beta_q * M[i][j] * R_q[w] #[0,1]*[0,10]*[0,10]/10000
                A_q[i] = int(A_q[i] * encrypt(public_key, phi))


    return A_q

#Obtain the database
D = getD()
print("[Data Owner]Obtained the database")

#Generate the private Key
Key = KeyGen()
print("[Data Owner]Generated its private key")

#Encrypt the data using the private Key
D_encrypted = encryptData(D,Key)
print("[Data Owner]Encrypted its data using the private key")

#Obtain the encrypted query from the Query User, perform necessary modification and send it back to the Query User - Receive Encrypt and Send
queryRES(Key)

