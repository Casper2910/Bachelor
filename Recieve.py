import socket

# Set up the socket
HOST = '0.0.0.0'   # Listen on all network interfaces
PORT = 12345       # Port to listen on
BUFFER_SIZE = 1024

# Create a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    print("UDP server started. Listening for incoming UDP packets...")

    # Receive and print data continuously
    while True:
        data, addr = s.recvfrom(BUFFER_SIZE)
        if data:
            temperature = data.decode()   # Convert received data to string
            print(f"Received temperature: {temperature}")
