import socket
import struct
def find_char_positions(string, char):
    return [i for i, c in enumerate(string) if c == char]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1", 1234)
s.bind(address)
s.listen(1)
while True:
    connection, client_address = s.accept()
    data = connection.recv(2)
    string_length = struct.unpack('!H', data)[0]

    string = connection.recv(string_length).decode('utf-8')

    char = connection.recv(1).decode('utf-8')

    positions = find_char_positions(string, char)

    connection.send(struct.pack('!H', len(positions)))

    for pos in positions:
        connection.send(struct.pack('!H', pos))
    connection.close()

