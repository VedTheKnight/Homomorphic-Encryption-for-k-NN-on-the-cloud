import socket
import json


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
            factors = factor(integer)
            data[data["key"]] = []
            for p in list(factors):
                x = int(p[1])
                while(x):
                    data[data["key"]].append(int(p[0]))
                    x -= 1
                # since p and x are special non-JSON serializable types we must explicitly convert to int. p is base of a factor and x is power.


            print("[CLOUD SERVER]Sending Data")
            conn.sendall(json.dumps(data).encode(FORMAT)) #sends the dictionary with the modified number replaced by the array of its factorization

            connected = False

        print(f"[CLOUD SERVER]{addr} has disconnected.")
