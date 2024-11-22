

import socket
import struct

HOST = "127.0.0.1"
PORT = 1234

def send_via_tcp(numbers):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORT))
    data = struct.pack(f"{len(numbers)}i", *numbers)
    sock.sendall(data)
    response = sock.recv(1024)
    result = response.decode("ascii")
    print(result)


def send_via_udp(numbers):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = struct.pack(f"{len(numbers)}i", *numbers)
    sock.sendto(data, (HOST, PORT))
    response = sock.recv(1024)
    result = response.decode("ascii")
    print(result)

def send_via_udp2(function):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = str.encode(function)
    sock.sendto(data, (HOST, PORT))
    response = sock.recv(1024)
    result = response.decode("ascii")
    print(result)

def start():
    numbers = [1, 2, 3, 4, 5]
    function = "x*2"
    protocol = "UDP"
    if protocol == "TCP":
        send_via_tcp(numbers)
    else:
        send_via_udp(numbers)
        send_via_udp2(function)


if __name__ == "__main__":
    start()
