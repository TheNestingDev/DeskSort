import socket
from network import SocketManager, ServerMode, get_local_ip
class Client:
    def __init__(self, server:SocketManager) -> None:
        self.server = server

    def run(self):
        self.server.send("hi from client")
        print(self.server.receive(1024))

def main():
    server_ip = input("Enter server IP address: ")
    host = get_local_ip() if server_ip == "" else server_ip
    port = 12345
    with SocketManager(host=host, port=port, mode=ServerMode.CLIENT) as server:
        client = Client(server)
        client.run()

if __name__ == "__main__":
    main()
