import socket
import threading
import base64
import json
import time
from queue import Queue
from keys.Signing import verify_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_blacklisted, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key
from id_dict import id_dict
from data.write import append_to_file
from connection.connector import send_json, obtain_ip

HOST = obtain_ip()  # own ip
PORT = 8081  # port

ISSUER_HOST = '192.168.0.141'  # issuer ip
ISSUER_PORT = 8080  # issuer port


def handle_device(device_socket, device_address, issuer_socket):
    # Receive data from device
    received_data = device_socket.recv(1024).decode("utf-8").strip()
    print('data:', received_data)

    data = json.loads(received_data)

    DID = data['DID']
    temp = data['temperature']

    if is_blacklisted(DID):
        print('DID is blacklisted')
        return

    if DID not in id_dict.values():
        print('New DID')
        # Save pending request locally
        with open("pending_requests.json", "a") as f:
            f.write(json.dumps(data) + '\n')
    else:
        print('Known DID')
        block_id = find_id(DID)
        DID_document = retrieve_block_data(block_id)
        proof_base64 = DID_document['proof']
        proof_binary = base64.b64decode(proof_base64)

        if verify_proof(proof_binary, public_key, DID):
            print(f'Arduino with {DID} is verified')

            # continue to document for 100 cycles:
            for i in range(100):
                append_to_file(DID, temp)
        else:
            print(f'Arduino with {DID} is NOT verified')


def handle_issuer(device_queue, issuer_socket):
    while True:
        # Check if there are pending requests
        if not device_queue.empty():
            # Accept connection from device
            device_conn, device_address = device_queue.get()
            print("Connection from device:", device_address)

            # Start handling device in a separate thread
            device_thread = threading.Thread(target=handle_device, args=(device_conn, device_address, issuer_socket))
            device_thread.start()
        else:
            # Sleep for a while before checking again
            time.sleep(1)


def main():
    # Create a socket object for device
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a socket object for issuer
    issuer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Display ip and port for the Arduino config
    print(f"Device socket listening for connections on {HOST, PORT}...")

    # Connect to the issuer
    try:
        issuer_socket.connect((ISSUER_HOST, ISSUER_PORT))
    except ConnectionRefusedError:
        print("Issuer is currently unreachable. Pending requests will be saved locally.")

    # Bind the device socket to a specific address and port
    device_socket.bind((HOST, PORT))

    # Listen for incoming connections on the device socket
    device_socket.listen(5)

    # Create a queue to hold incoming device connections
    device_queue = Queue()

    # Start the issuer handler thread
    issuer_handler_thread = threading.Thread(target=handle_issuer, args=(device_queue, issuer_socket))
    issuer_handler_thread.start()

    while True:
        # Accept connection from device
        device_conn, device_address = device_socket.accept()
        print("Connection from device:", device_address)

        # Add device socket to the queue
        device_queue.put((device_conn, device_address))


if __name__ == "__main__":
    main()
