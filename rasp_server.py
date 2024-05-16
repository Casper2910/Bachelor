import socket
import threading
import base64
import json
from queue import Queue
from keys.Signing import verify_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_blacklisted, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key
from id_dict import id_dict
from data.write import append_to_file
from connection.connector import send_json

HOST = socket.gethostbyname(socket.gethostname())  # own ip
PORT = 8081  # port

ISSUER_HOST = '192.168.0.133'  # issuer ip
ISSUER_PORT = 8080  # issuer port


def handle_device(issuer_socket, device_queue):
    while True:
        # Get device socket from the queue
        device_socket, device_address = device_queue.get()

        # Receive data from device
        received_data = device_socket.recv(1024).decode("utf-8").strip()

        print('data:', received_data)

        data = json.loads(received_data)

        DID = data['DID']
        temp = data['temperature']

        if is_blacklisted(DID):
            print('DID is blacklisted')
            pass

        if DID not in id_dict.values():
            print('New DID')
            # request did doc:
            send_json(69420, device_address[0], 8082)  # Arduino's is listening on port 8082

            # Wait for the did document
            while True:
                print('Awaiting did document from device...')
                # Receive data from the device
                received_data = device_socket.recv(1024).decode("utf-8")

                # Parse the received JSON string
                received_json = json.loads(received_data)

                if "proof" in received_json:
                    DID_doc = received_json
                    # Do something if the field and its content match
                    print('DID doc:', DID_doc)
                    break

            # Send the DID to the issuer for authentication
            print('Sending DID doc to issuer')
            issuer_socket.send(DID.encode("utf-8"))

            while True:
                print('Awaiting issuers signature...')
                # Receive data from the issuer
                proof = issuer_socket.recv(1024)

                # Example: Check if the received data from the issuer matches a specific condition
                if proof == 'no':
                    # add to blacklist
                    print('DID has been blacklisted')
                    add_to_blacklist(DID)
                    break

                else:
                    print('DID has been authorized')
                    DID_doc['proof'] = proof
                    DID_doc['publicKey'] = public_key
                    block_id = upload_block(DID_doc)
                    insert_entry(block_id, DID)
                    break

        if DID in id_dict.values():
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


def main():
    # Create a socket object for device
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a socket object for issuer
    issuer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the issuer
    issuer_socket.connect((ISSUER_HOST, ISSUER_PORT))

    # Bind the device socket to a specific address and port
    device_socket.bind((HOST, PORT))

    # Listen for incoming connections on the device socket
    device_socket.listen(5)
    print(f"Device socket listening for connections on {HOST, PORT}...")

    # Create a queue to hold incoming device connections
    device_queue = Queue()

    # Start the device handler thread
    device_handler_thread = threading.Thread(target=handle_device, args=(issuer_socket, device_queue))
    device_handler_thread.start()

    while True:
        # Accept connection from device
        device_conn, device_address = device_socket.accept()
        print("Connection from device:", device_address)

        # Add device socket to the queue
        device_queue.put((device_conn, device_address))


if __name__ == "__main__":
    main()
