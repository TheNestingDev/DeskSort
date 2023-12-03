import socket
from enum import Enum, auto

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

class ConnectionStatus(Enum):
    CONNECTED = auto()
    DISCONNECTED = auto()
    CONNECTION_FAILED = auto()
    NOT_INITIALIZED = auto()
    USER_DISCONNECTED = auto()
    SERVER_DISCONNECTED = auto()

class ServerMode(Enum):
    SERVER = auto()
    CLIENT = auto()

class SocketManager:
    def __init__(self, host:str='127.0.0.1', port:int=12345, mode:ServerMode=ServerMode.SERVER):
        self.host:str = host
        self.port:int = port
        self.mode:ServerMode = mode
        self.socket:socket.socket = None
        self.connection_status:ConnectionStatus = ConnectionStatus.NOT_INITIALIZED

    def _init_sever(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server started on {self.host}:{self.port}")

    def _init_client(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.mode == ServerMode.SERVER:
            self._init_sever()
        elif self.mode == ServerMode.CLIENT:
            self._init_client()
        else:
            raise NotImplementedError(f"{self.mode} is not currently supported")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
        print("Socket closed.")
        return False

    def send(self, message:str, conn:socket.socket):
        socket.send(message.encode())

    def receive(self, expected_size:int):
        return self.socket.recv(expected_size)
