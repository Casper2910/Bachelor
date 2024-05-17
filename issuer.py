import socket
import threading
from keys.Signing import sign_proof
from keys.keys import public_key, private_key
from queue import Queue
from connection.connector import obtain_ip

HOST = obtain_ip()  # own ip # own ip
PORT = 8080  # port


def handle_request(queue):
    while True:
        # Get client socket from the queue
        client_socket, client_address = queue.get()

        # Receive data from client
        DID = client_socket.recv(1024).decode("utf-8").strip()
        answer = input(f'Do you want to deliver proof for: {DID} \n Yes \n No \n').lower()

        # Process received data and decide response
        if answer == "yes":
            proof = sign_proof(DID, private_key, public_key)
            response = proof
            # Send response back to client
            client_socket.send(response)
        else:
            response = "no"
            # Send response back to client
            client_socket.send(response.encode("utf-8"))

        print('data send: ', response)
        # Close client socket
        client_socket.close()

        # Mark the task as done
        queue.task_done()


def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)
    print("Server listening for connections on", HOST, PORT)

    # Create a queue to hold incoming connections
    connection_queue = Queue()

    # Start the client handler thread
    client_handler_thread = threading.Thread(target=handle_request, args=(connection_queue,))
    client_handler_thread.start()

    while True:
        # Accept connection from client
        client_socket, client_address = server_socket.accept()
        print("Connection from:", client_address)

        # Add client socket to the queue
        connection_queue.put((client_socket, client_address))


if __name__ == "__main__":
    main()
