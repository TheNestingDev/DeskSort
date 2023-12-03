import socket

class SocketManager:
    def __init__(self, host='127.0.0.1', port=12345, mode='server'):
        self.host = host
        self.port = port
        self.mode = mode
        self.socket = None

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.mode == 'server':
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print(f"Server started on {self.host}:{self.port}")
        elif self.mode == 'client':
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
        print("Socket closed.")
        return False
