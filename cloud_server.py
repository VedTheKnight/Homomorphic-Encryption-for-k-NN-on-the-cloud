import socket
import json

#function to identify whether n is a prime: returns 1 if n is prime and 0 if it is not prime
def isPrime(n):
    for i in range(2,n):
        if(n%i==0):
            return 0
    return 1

#function to compute the next prime given a prime n
def nextPrime(n):
    n += 1
    while(not isPrime(n)):
        if(not isPrime(n)):
            n += 1
    return n

#function to factorize n and return an array consisting of each prime factor
def factorize(n):
    factors = []
    for i in range(2,n+1):
            while(n>0 and isPrime(i) and n%i==0):
                factors.append(i)
                n = n/i
            i = nextPrime(i)
    return factors

if __name__ == '__main__':

    PORT2 = 65433 #port for the cloud server
    SERVER = socket.gethostname()
    ADDR2 = (SERVER,PORT2)
    FORMAT = 'utf-8'

    cloudServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the cloud server socket
    cloudServer.bind(ADDR2)
    cloudServer.listen()
    print(f"[CLOUD SERVER]Cloud Server is listening on {ADDR2}")

    while True:
        conn, addr = cloudServer.accept()
        print(f"[CLOUD SERVER]{addr} connected. ")

        connected = True
        while connected:

            data = json.loads(conn.recv(2048).decode(FORMAT)) #data obtained and converted into a dictionary
            print("[CLOUD SERVER]Data Received")

            integer = data[data["key"]] #extracts the modified integer from the data

            print("[CLOUD SERVER]Running operations on data")
            data[data["key"]] = factorize(integer)

            print("[CLOUD SERVER]Sending Data")
            conn.sendall(json.dumps(data).encode(FORMAT)) #sends the dictionary with the modified number replaced by the array of its factorization

            connected = False

        print(f"[CLOUD SERVER]{addr} has disconnected.")
