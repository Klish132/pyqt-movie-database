import socket
import threading
import dbwrapper as wrapper

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_list = []


def handle_client(conn, addr):
    print(f"[NEW CONN] {addr} connected.")

    connected = True
    while connected:
        message_length_decoded = conn.recv(HEADER).decode(FORMAT)
        if message_length_decoded:
            message_length = int(message_length_decoded[1:])
            message = conn.recv(message_length).decode(FORMAT)
            action, info = message.split("|", 1)
            if action == DISCONNECT_MESSAGE:
                connected = False
            else:
                result = wrapper.message_analyzer(action, info)
                if "UPD" in result[0]:
                    msg = result[0]
                    msg_length = get_length(msg)
                    send_to_all(msg_length)
                    send_to_all(msg.encode(FORMAT))
                else:
                    for msg in result:
                        msg_length = get_length(msg)
                        conn.send(msg_length)
                        conn.send(msg.encode(FORMAT))
    remove(conn)
    conn.close()


def get_length(info):
    msg_length = len(info)
    msg_length_coded = ("H" + str(msg_length)).encode(FORMAT)
    msg_length_coded += b' ' * (HEADER - len(msg_length_coded))
    return msg_length_coded


def send_to_all(message):
    for client in client_list:
        try:
            client.send(message)
        except Exception as e:
            print(str(e))
            client.close()
            remove(client)


def remove(conn):
    if conn in client_list:
        client_list.remove(conn)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNS] {threading.activeCount() - 1}")


print("[START] Server is starting...")
start()


