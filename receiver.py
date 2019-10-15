#!/usr/bin/python3
from os.path import exists
from threading import Thread


class Receiver(Thread):
    def __init__(self, conn, address):
        super().__init__(daemon=True)
        self.conn = conn
        self.address = address
        print('New connection request to', address)

    def run(self):
        # get file length
        file_length = self.conn.recv(4)
        file_length = int.from_bytes(file_length, 'little')
        file_name = self.conn.recv(file_length).decode()
        # split for extention and name of file
        ind = file_name.rindex('.')
        file_name = file_name[:ind]
        extention = file_name[ind:]

        # find the index of file copy(if there are already some with the name)
        number_of_copies = 0
        if exists(file_name):
            number_of_copies += 1
        while exists(file_name + '_copy' + str(number_of_copies) + extention):
            number_of_copies += 1

        # create the name for file
        st = ""
        if number_of_copies > 0:
            st = "_copy" + str(number_of_copies)
        file_name += '_copy' + str(number_of_copies) + extention

        print('Download started %s ...' % file_name)

        # recieving the file
        with open(file_name, 'wb') as file:
            data = self.conn.recv(1024)
            while data:
                file.write(data)
                data = self.conn.recv(1024)

        self.conn.close()
        print(file_name, ' successfully downloaded.')
