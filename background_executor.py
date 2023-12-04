import network
import socket


class Server:
    def __init__(self, server_conn: network.SocketManager) -> None:
        self.server_conn = server_conn
        self.server_conn.init_sever()
        self.status: network.ConnectionStatus = network.ConnectionStatus.CONNECTED

    def handle_client_logic(self, client: network.Client):
        data = client.connection.recv(1024)
        if not data:
            client.status = network.ConnectionStatus.CLIENT_DISCONNECTED
            return

        print(f"{client.address}: {data}")
        client.connection.send(f"Response to {client.address}: {data}".encode())

    def handle_client(self, client: network.Client) -> int:
        print(f"[Server] connection started with: {client.address}")

        while client.status == network.ConnectionStatus.CONNECTED:
            try:
                self.handle_client_logic(client)
            except Exception as e:
                print(f"[Server] Error handling client {client.address}: {e}")
                return network.StatusCodes.ERROR

    def handle_connection(self):
        try:
            connection, address = self.server_conn.socket.accept()
            client = network.Client(connection, address, network.ConnectionStatus.CONNECTED)
            with client.connection:
                exit_status = self.handle_client(client)
            print(f"[Server] Client got disconnected: {exit_status}")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"[Server] An error occurred during connection: {e}")

    def run(self):
        while self.status == network.ConnectionStatus.CONNECTED:
            print("[Server] waiting for new connection...")
            self.handle_connection()

        print("[Server] shutdown.")

class Worker:
    pass

def main():
    host = network.get_local_ip()
    port = 12345
    with network.SocketManager(host=host, port=port) as server_conn:
        server = Server(server_conn)
        server.run()

if __name__ == "__main__":
    main()
