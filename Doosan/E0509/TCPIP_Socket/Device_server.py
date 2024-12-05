import socket
import threading
from queue import Queue

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Create send and receive queues
send_queue = Queue()
receive_queue = Queue()


# Start the server
start_server()
class RobotSocket:
    def __init__(self):
        self.send_queue = Queue()
        self.receive_queue = Queue()

    def handle_client(self, client_socket):
        while True:
            # Check if there is a message in the send queue
            if not self.send_queue.empty():
                message = self.send_queue.get()
                client_socket.send(message.encode())

            # Receive data from the client
            data = client_socket.recv(1024).decode()

            # Check if data is received
            if data:
                # Add the received data to the receive queue
                self.receive_queue.put(data)

    def start_server(self):
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        SERVER_ADDRESS = 'localhost'
        SERVER_PORT = 12345

        # Bind the socket to the server address and port
        server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

        # Listen for incoming connections
        server_socket.listen()

        print(f"Server is listening on {SERVER_ADDRESS}:{SERVER_PORT}")

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    # Create an instance of RobotSocket
    robot_socket = RobotSocket()

    # Start the server
    robot_socket.start_server()