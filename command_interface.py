import socket
from network import SocketManager, ServerMode, get_local_ip

class Client:
    def __init__(self, server:SocketManager) -> None:
        self.server_conn = server
        self.server_conn.init_client()

    def run(self):
        while True:
            msg = input("> ")
            if msg.lower == "exit":
                break
            self.server_conn.socket.send(msg.encode())
            print(self.server_conn.socket.recv(1024))

def main():
    server_ip = input("Enter server IP address: ")
    host = get_local_ip() if server_ip == "" else server_ip
    port = 12345
    with SocketManager(host=host, port=port, mode=ServerMode.CLIENT) as server_conn:
        client = Client(server_conn)
        client.run()

if __name__ == "__main__":
    main()
