import socket
import json
from threading import Thread
from keys.Signing import sign_proof

# Define the IP address and port to listen on
HOST = '192.168.0.133'  # Replace with your server's IP address
PORT = 8080  # Replace with your desired port number


def handle_proof(data):
    # Check if 'proof' == 'NEEDS_PROOF'
    response = ''

    if 'proof' in data and data['proof'] == 'NEEDS_PROOF':
        # Ask the user if they want to deliver proof
        answer = input(f"Do you want to deliver proof for ID: {data['id']}? (Yes/No): ").lower()

        if answer == 'yes':
            # Call the sign_proof function
            data['proof'] = sign_proof(data['id'])
            response = f'proof delivered for {data['id']}'

        else:
            response = f'"Proof declined for {data['id']}'

    return response


# Function to handle incoming connections and process data
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

    # Process the data
    handle_proof(data)

    # Close the client socket
    client_socket.close()


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
        thread = Thread(target=handle_connection, args=(client_socket,))
        thread.start()
