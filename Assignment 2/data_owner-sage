import socket
import json
import random

if __name__ == '__main__':

    PORT1 = 65432 #port for the data owner
    SERVER = socket.gethostname() #gets the ip-address of the device
    ADDR1 = (SERVER,PORT1)
    FORMAT = 'utf-8'

    dataOwner = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates the data owner socket
    dataOwner.bind(ADDR1)
    dataOwner.listen()
    print(f"[DATA OWNER]Data Owner is listening on {ADDR1}")

    #creating this loop allows the data owner to interact with multiple clients in sequential order
    while True:
        conn, addr = dataOwner.accept() #starts a connection between client and data owner
        print(f"[DATA OWNER]{addr} connected. ")

        connected = True
        while connected:
            query = json.loads(conn.recv(2048).decode(FORMAT))  # query obtained and converted to a dictionary

            # generates a random number between 1 and 10000 and multiplies the query integer by it
            random_number = random.randint(1, 10000)
            query[query["key"]] *= random_number

            conn.sendall(json.dumps(query).encode(FORMAT))#converts the dictionary back into binary format and sends it back to client as data
            connected = False

        print(f"[DATA OWNER]{addr} has disconnected.")


