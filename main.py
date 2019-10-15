import reciever_of_connection


def run_server():
    start_server = reciever_of_connection.RecieverOfConnection()
    start_server.start()
    start_server.join()


if __name__ == '__main__':
    run_server()
