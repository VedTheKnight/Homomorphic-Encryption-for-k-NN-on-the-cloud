import socket

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

if __name__ == '__main__':
    HEADER = 64 #to store the number of bits of the incoming message
    PORT = 5050
    SERVER = socket.gethostname()
    ADDR = (SERVER,PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)



send("Hello World!")
send(("!DISCONNECT"))