

import socket
import struct
import threading

def udpfunction(socket):
    while True:
        data, adr = socket.recvfrom(1024)
        try:
            numbers = struct.unpack(f"{len(data) // 4}i",data)
            result = sum(numbers)
            print(result)
        except:

            function = data.decode("ascii")
            print(function)
        socket.sendto(bytes("greetings message", "ascii"), adr)



def tcpfunction(conn, adr):
    data = conn.recv(1024)
    numbers = struct.unpack(f"{len(data) // 4}i", data)
    result = sum(numbers)
    conn.sendto(struct.pack("!i", result), adr)

def start_program():

    host = "127.0.0.1"
    port = 1234
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcpsock.bind((host,port))
    tcpsock.listen(1)
    udpsock.bind((host,port))

    udp_th = threading.Thread(target=udpfunction, args=([udpsock]),daemon=True)
    udp_th.start()
    while True:
        conn, adr = tcpsock.accept()
        threading.Thread(target=tcpfunction, args=(conn, adr), daemon=True).start()

if __name__ == '__main__':
    start_program()

