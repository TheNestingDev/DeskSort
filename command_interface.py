import socket

def send_command(command):
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 12345        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode())
        print(f"Command sent: {command}")

def main():
    while True:
        cmd = input("Enter command: ")
        if cmd.lower() == 'exit':
            break
        send_command(cmd)

if __name__ == "__main__":
    main()
