#!/usr/bin/python3
import socket
from threading import Thread, Event
from time import sleep

from receiver import Receiver


class RecieverOfConnection(Thread):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__stop_event = Event()

    def run(self):
        self.__serve()

    def stop(self):
        self.__stop_event.set()
        self.sock.close()
        print('Closed main socket.')

    def __serve(self):
        self.sock.bind(('', 28762))
        self.sock.listen(8)

        print('Ready to receive connection')

        conn, addr = self.sock.accept()
        Receiver(conn, addr).start()

        print('Stopped Server.')
        sleep(1)
        self.sock.close()
