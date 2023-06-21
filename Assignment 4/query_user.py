import socket
import json

if __name__ == '__main__':

    PORT1 = 65432 #data owner port
    PORT2 = 65433 #cloud server port
    SERVER = socket.gethostname()
    ADDR1 = (SERVER,PORT1)#data owner
    ADDR2 = (SERVER,PORT2)#cloud server
    FORMAT = 'utf-8'

    with open("/tmp/data/query_data.txt", "r") as file:
        integer = int(file.readline())
    query = {"key" : "password","password" : integer} #creates the query dictionary using the integer provided by the user

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #intializes the client object

    #interaction with the data owner

    client.connect(ADDR1) #establishes connection with the data owner's port
    client.sendall(json.dumps(query).encode(FORMAT)) #sends the query to the data owner for modification

    data = json.loads(client.recv(2048).decode(FORMAT)) #obtains the modified query as data by multiplying the integer by a random number between 1 and 10000

    print(f'[QUERY USER]Modified integer:{data[data["key"]]}')

    client.close() #closes the connection with the data owner

    #interaction with the cloud server

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #re-initializes the client object for connection with the cloud server's port

    client.connect(ADDR2) #establishes connection with the cloud server's port
    client.sendall(json.dumps(data).encode(FORMAT)) #sends the data to the cloud server for prime factorization

    print("[QUERY USER]Data sent to cloud server for computation")









