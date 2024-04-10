import socket
import json
from threading import Thread
from keys.Signing import sign_proof
from iota.block_handler import upload_block, retrieve_block_data
from block_id_dictonary.write_read_dict import find_id, insert_entry

# Define the IP address and port to listen on
HOST = '192.168.0.133'  # Replace with your server's IP address
PORT = 8080  # Replace with your desired port number


def handle_connection(client_socket):
    # Receive data from the client
    received_data = b""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        received_data += chunk

    # Decode received data
    received_json = received_data.decode("utf-8")
    print("Received JSON data:")
    print(received_json)

    # Parse received JSON
    data = json.loads(received_json)

    # Close the client socket
    client_socket.close()

    # Return the parsed JSON object
    return data


def server(HOST, PORT):
    # Variable to store received JSON object
    received_json = None

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))

        # Start listening for incoming connections
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        # Accept incoming connections and start a new thread to handle each one
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            # Handle the connection and get the received JSON object
            received_json = handle_connection(client_socket)
            # Break the loop if the received JSON object is obtained
            if received_json:
                break

    # Return the received JSON object
    return received_json

