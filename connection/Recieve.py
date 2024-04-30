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
    try:
        # Receive data from the client
        received_data = b""
        chunk = client_socket.recv(1024)
        received_data += chunk

        # Decode received data
        received_json = received_data.decode("utf-8")
        print("Received JSON data:")
        print(received_json)

        # Parse received JSON
        data = json.loads(received_json)

        # Return the parsed JSON object and client address
        return data, client_socket.getpeername()

    except Exception as e:
        print("Error handling connection:", e)
        return None, None


def server(HOST, PORT):
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
            # Handle the connection and get the received JSON object and client address
            received_json, client_address = handle_connection(client_socket)
            # Break the loop if the received JSON object is obtained
            if received_json:
                break

    # Return the received JSON object and client address
    return received_json, client_address


def send_data(data, ip, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the Arduino
            client_socket.connect((ip, port))

            # Convert the data to JSON format
            json_data = json.dumps(data)

            # Send the JSON data to the Arduino
            client_socket.sendall(json_data.encode())

            print("Data sent to Arduino:", data)

    except Exception as e:
        print("Error sending data to Arduino:", e)
