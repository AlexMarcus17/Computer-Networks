
import socket
import threading
import random
import struct
import time

random.seed()
start = 1.0
stop = 100.0
my_num = random.uniform(start, stop)
print('Server number: ', my_num)
mylock = threading.Lock()
client_guessed = False
winner_thread = 0
e = threading.Event()
e.clear()
threads = []
client_count = 0
best_guess = None
best_client = None
best_error = float('inf')
last_connection_time = time.time()
client_sockets = []

def worker(cs):
    global mylock, client_guessed, my_num, winner_thread, client_count, e, best_guess, best_client, best_error, last_connection_time

    my_idcount = client_count
    print('client #', client_count, 'from: ', cs.getpeername(), cs)
    message = 'Hello client #' + str(client_count) + ' ! You are entering the number guess competition now!'
    cs.sendall(bytes(message, 'ascii'))

    while not client_guessed:
        try:
            cnumber = cs.recv(4)
            if not cnumber:
                break
            cnumber = struct.unpack('!f', cnumber)[0]
            print(f'Client #{my_idcount} guessed: {cnumber}')
            error = abs(my_num - cnumber)

            mylock.acquire()
            if error < best_error:
                best_error = error
                best_guess = cnumber
                best_client = cs
            mylock.release()

            last_connection_time = time.time()
            time.sleep(0.5)
        except socket.error as msg:
            print('Error:', msg.strerror)
            break

    cs.close()
    print("Worker Thread ", my_idcount, " end")

def resetSrv():
    global mylock, client_guessed, winner_thread, my_num, threads, e, client_count, best_guess, best_client, best_error, last_connection_time, client_sockets
    while True:
        time.sleep(1)
        if time.time() - last_connection_time > 10:
            mylock.acquire()
            if best_client:
                best_client.sendall(bytes(f'You have the best guess with an error of {best_error:.2f}!', 'ascii'))
                for cs in client_sockets:
                    if cs != best_client:
                        cs.sendall(b'You lost !')
                client_guessed = True
            mylock.release()

            print("All clients have been notified. Server resetting.")
            for cs in client_sockets:
                cs.close()
            break

if __name__ == '__main__':
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rs.bind(('0.0.0.0', 12345))
        rs.listen(5)
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    t = threading.Thread(target=resetSrv, daemon=True)
    t.start()

    while True:
        client_socket, addrc = rs.accept()
        client_sockets.append(client_socket)  # Store the client socket
        t = threading.Thread(target=worker, args=(client_socket,))
        threads.append(t)
        client_count += 1
        t.start()