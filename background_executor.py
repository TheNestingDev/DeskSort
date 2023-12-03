from network import SocketManager, get_local_ip
from dataclasses import dataclass
import socket

STATUS_SUCCESS = 200
STATUS_CLIENT_DISCONNECTED = 201
STATUS_ERROR = 300

@dataclass
class Client:
    connection: socket.socket
    address: tuple  # (IP, Port)

class Server:
    def __init__(self, server: SocketManager) -> None:
        self.server = server
        self.active = True

    def handle_client(self, client: Client) -> int:
        print(f"Server connected to: {client.address}")
        while True:
            try:
                data = client.connection.recv(1024)
                if not data:
                    return STATUS_CLIENT_DISCONNECTED
                print(f"{client.address}: {data}")
                .send(f"Hey server response: {data}")
            except Exception as e:
                print(f"Error handling client {client.address}: {e}")
                return STATUS_ERROR

    def handle_connection(self):
        try:
            connection, address = self.server.socket.accept()
            client = Client(connection, address)
            with client.connection:
                status = self.handle_client(client)
            print(f"Client got disconnected: {status}")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"An error occurred during connection: {e}")

    def run(self):
        while self.active:
            print("Server waiting for connection...")
            self.handle_connection()

        # Server shutdown logic here if needed
        print("Server shutdown.")

class Worker:
    pass

def main():
    host = get_local_ip()
    port = 12345
    with SocketManager(host=host, port=port) as server_con:
        server = Server(server_con)
        server.run()

if __name__ == "__main__":
    main()
