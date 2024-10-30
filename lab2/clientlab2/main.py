import socket

import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect( ("127.0.0.1",1234) )
string = input("Enter a string: ")
char = input("Enter a character to search for: ")

s.send(struct.pack('!H', len(string)))

s.send(string.encode('utf-8'))

s.send(char.encode('utf-8'))

data = s.recv(2)
num_positions = struct.unpack('!H', data)[0]

positions = []
for _ in range(num_positions):
    data = s.recv(2)
    position = struct.unpack('!H', data)[0]
    positions.append(position)

print(f"The character '{char}' was found at positions: {positions}")
s.close()