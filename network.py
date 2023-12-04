import socket
from enum import Enum, auto
from dataclasses import dataclass

class ConnectionStatus(Enum):
    CONNECTED = auto()
    DISCONNECTED = auto()
    CONNECTION_FAILED = auto()
    NOT_INITIALIZED = auto()
    CLIENT_DISCONNECTED = auto()
    SERVER_DISCONNECTED = auto()

class ServerStatus(Enum):
    ACTIVE = auto()
    STOPPED = auto()
    STOPPED_ERROR = auto()
    STOPPED_MANUAL = auto()

class ServerMode(Enum):
    SERVER = auto()
    CLIENT = auto()

class StatusCodes(Enum):
    SUCCESS = 200
    CLIENT_DISCONNECTED = 201
    ERROR = 300

@dataclass
class Client:
    connection: socket.socket
    address: tuple  # (IP, Port)
    status: ConnectionStatus

class SocketManager:
    def __init__(self, host:str='127.0.0.1', port:int=12345, mode:ServerMode=ServerMode.SERVER):
        self.host:str = host
        self.port:int = port
        self.mode:ServerMode = mode
        self.socket:socket.socket = None
        self.connection_status:ConnectionStatus = ConnectionStatus.NOT_INITIALIZED

    def init_sever(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"[SocketManager] Server started on {self.host}:{self.port}")

    def init_client(self):
        self.socket.connect((self.host, self.port))
        print(f"[SocketManager] Connected to server at {self.host}:{self.port}")

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            self.socket.close()
        print("[SocketManager] Socket closed.")
        return False

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
