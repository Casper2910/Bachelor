import socket

# Define the IP address and port to listen on
HOST = '192.168.0.133'  # Replace with your server's IP address
PORT = 8080  # Replace with your desired port number

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))

    # Start listening for incoming connections
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

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
