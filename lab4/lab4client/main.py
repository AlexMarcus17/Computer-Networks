import socket


def main():
    server_address = ('127.0.0.1', 1234)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        welcome_message = client_socket.recv(1024).decode('ascii')
        print("Server:", welcome_message)

        while True:
            command = input("Enter a command to execute on the server (or type 'exit' to quit): ")
            if command.lower() == 'exit':
                print("Exiting...")
                break

            client_socket.sendall(command.encode('ascii'))

            response = client_socket.recv(4096).decode('ascii')
            print("Server response:\n", response)

    except socket.error as e:
        print("Socket error:", e)

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()