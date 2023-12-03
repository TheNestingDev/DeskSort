import socket
import sys
from network import SocketManager
from dataclasses import dataclass

@dataclass
class Client:
    connection:socket.socket
    address:int

class Server:
    def __init__(self, server:SocketManager) -> None:
        self.server = server
        self.active = True

    def handle_client(self, client:Client) -> int:
        print(f"Server connected to: {client.address}")
        while True:
            data = client.connection.recv(1024)
            if not data:
                return 100
            print(f"{client.address}: {data}")

    def run(self):
        while self.active:
            print("server waiting for connection...")

            # wait for connection
            try:
                connection, address = self.server.socket.accept()
            except KeyboardInterrupt:
                print("Manually stopped Server by user")
                self.active = False
                break

            # handle connection
            client = Client(connection, address)
            with client.connection:
                status = self.handle_client(client)
            print(f"Client got disconnected: {status}")

class Worker:
    pass

def main():
    with SocketManager() as server_con:
        server = Server(server_con)
        server.run()

if __name__ == "__main__":
    main()
