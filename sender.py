import socket
from os.path import getsize
from sys import argv
from threading import Thread


class Sender(Thread):

    def __init__(self, file, address):
        super().__init__(daemon=True)
        self.file_name = file
        self.file_size = -123
        self.address = address

    def run(self):
        # connect to socker
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.address)

        # get known with length of the file and send the length
        file_length = len(self.file_name).to_bytes(4, 'little')
        file_send = self.file_name
        if self.file_name[:2] == '.\\':
            file_length = (len(self.file_name) - 2).to_bytes(4, 'little')
            file_send = self.file_name[2:]
        sock.send(file_length)
        sock.send(file_send.encode())

        # open file and start sending by 1024 bytes
        self.bytes_sent = 0
        with open(self.file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                sock.send(data)
                data = file.read(1024)
                self.bytes_sent += len(data)
        sock.close()
        self.file_size = getsize(self.file_name)


def download_percentage(self):
    if self.file_size == 0:
        return 0
    return 100 * (self.bytes_sent / self.file_size)


def run_sender():
    file = argv[1]
    argv[-1] = int(argv[-1])
    addr = tuple(argv[-2:])

    sender = Sender(file, addr)
    sender.start()

    while sender.is_alive():
        print(sender.download_percentage(), '%', '\r')
        if (sender.download_percentage() == 100):
            print(sender.filename, ' successfully downloaded')

    sender.join()


if __name__ == '__main__':
    run_sender()
