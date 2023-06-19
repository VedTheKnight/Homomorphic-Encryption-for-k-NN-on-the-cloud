import socket
import threading

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected. ")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}]{msg}")

def start():
    server.listen()
    print(f"[LISTENING]Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        """
        the code waits on this line for a new connection to the server and when one occurs it will store the
        address of the connection and a socket object which allows us to send information back to that connection
        """
        thread = threading.Thread(target = handle_client,args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # excluding the original start() thread which is running always

if __name__ == '__main__':

    HEADER = 64 #to store the number of bits of the incoming message
    PORT = 5050
    SERVER = socket.gethostname()
    ADDR = (SERVER,PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #creates the server socket
    server.bind(ADDR)

    print("[STARTING]server is starting...")
    start()



