import socket
import subprocess
import threading
import random


random.seed()
start=1; stop=2**17-1
my_num= random.randint(start,stop)
print('Server number: ',my_num)
mylock = threading.Lock()
client_guessed=False
winner_thread=0
e = threading.Event()
e.clear()
threads = []
client_count=0


def worker(cs, client_id):
    print('Client #', client_id, 'connected from:', cs.getpeername())

    message = f'Hello Client #{client_id}! You are connected to the command execution server!'
    cs.sendall(bytes(message, 'ascii'))

    while True:
        try:
            cmd_bytes = cs.recv(1024)
            if not cmd_bytes:
                print(f"Client #{client_id} disconnected.")
                break
            cmd_str = cmd_bytes.decode('ascii').strip()

            if cmd_str.lower() == 'exit':
                print(f"Client #{client_id} requested exit.")
                break

            try:
                result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
                stdout = result.stdout
                stderr = result.stderr
                exit_code = result.returncode

                response = f"Output:\n{stdout}\nError:\n{stderr}\nExit Code: {exit_code}\n"
            except Exception as ex:
                response = f"Command execution failed: {ex}\n"

            cs.sendall(response.encode('ascii'))

        except socket.error as msg:
            print('Socket error:', msg)
            break

    cs.close()
    print(f"Worker Thread for Client #{client_id} ended")


def resetSrv():
    global mylock, client_guessed, winner_thread, my_num, threads,e, client_count
    while True:
        e.wait()
        for t in threads:
            t.join()
        print("all threads are finished now")
        e.clear()
        mylock.acquire()
        threads = []
        client_guessed = False
        winner_thread=-1
        client_count = 0
        my_num = random.randint(start,stop)
        print('Server number: ',my_num)
        mylock.release()


def main():
    server_port = 1234
    client_count = 0

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', server_port))
        server_socket.listen(5)
        print("Server is listening on port", server_port)

        while True:
            client_socket, client_addr = server_socket.accept()
            client_count += 1
            t = threading.Thread(target=worker, args=(client_socket, client_count))
            t.start()

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except socket.error as e:
        print("Socket error:", e)
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()