import socket
import threading
import base64
import json
import time
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

RETRY_DELAY = 5  # seconds


def connect_to_issuer():
    try:
        print('Attempting to connect to issuer...')
        issuer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        issuer_socket.connect((ISSUER_HOST, ISSUER_PORT))
        print('Successfully connected to the issuer.')
        return issuer_socket
    except Exception as e:
        print('Error occurred while connecting to the issuer:', e)
        return None


def handle_device(device_socket, device_address):
    while True:
        try:
            # Receive data from device
            received_data = device_socket.recv(1024).decode("utf-8").strip()
            if not received_data:
                print("No data received. Closing connection.")
                break
            print('data:', received_data)

            data = json.loads(received_data)
            DID = data['DID']
            temp = data['temperature']

            if is_blacklisted(DID):
                print('DID is blacklisted')
                continue

            if DID not in id_dict.values():
                print('New DID')
                # request did doc:
                send_json(69420, device_address[0], 8082)  # Arduino's is listening on port 8082

                # Wait for the did document
                while True:
                    print('Awaiting did document from device...')
                    # Receive data from the device
                    received_data = device_socket.recv(1024).decode("utf-8")
                    if not received_data:
                        print("No data received for DID document. Retrying...")
                        continue

                    # Parse the received JSON string
                    received_json = json.loads(received_data)

                    if "proof" in received_json:
                        DID_doc = received_json
                        print('DID doc:', DID_doc)
                        break

                # Attempt to connect to the issuer for authentication and send the DID to the issuer for authentication
                while True:
                    issuer_socket = connect_to_issuer()
                    if issuer_socket is None:
                        time.sleep(RETRY_DELAY)
                    else:
                        break

                print('Sending DID doc to issuer')
                issuer_socket.send(DID.encode("utf-8"))

                while True:
                    print('Awaiting issuer\'s signature...')
                    # Receive data from the issuer
                    proof = issuer_socket.recv(1024).decode("utf-8")

                    if proof == 'no':
                        print('DID has been blacklisted')
                        add_to_blacklist(DID)
                        break
                    else:
                        print('DID has been authorized')
                        DID_doc['proof'] = proof
                        DID_doc['publicKey'] = public_key
                        block_id = upload_block(DID_doc)
                        insert_entry(block_id, DID)
                        # add the entry to the local dict in memory
                        id_dict[block_id] = DID
                        break


            if DID in id_dict.values():
                print('Known DID')
                block_id = find_id(DID)
                DID_document = retrieve_block_data(block_id)
                proof_base64 = DID_document['proof']
                proof_binary = base64.b64decode(proof_base64)

                if verify_proof(proof_binary, public_key, DID):
                    print(f'Arduino with {DID} is verified')
                    append_to_file(DID, temp)
                else:
                    print(f'Arduino with {DID} is NOT verified')

        except (socket.error, json.JSONDecodeError) as e:
            print(f"Error: {e}. Restarting connection handling.")
            break

    device_socket.close()
    print(f"Connection with {device_address} closed.")


def main():
    # Create a socket object for device
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Display ip and port for the Arduino config
    print(f"Device socket listening for connections on {HOST, PORT}...")

    # Bind the device socket to a specific address and port
    device_socket.bind((HOST, PORT))

    # Listen for incoming connections on the device socket
    device_socket.listen(5)

    while True:
        # Accept connection from device
        device_conn, device_address = device_socket.accept()
        print("Connection from device:", device_address)

        # Start a thread to handle the device connection
        device_thread = threading.Thread(target=handle_device, args=(device_conn, device_address))
        device_thread.start()


if __name__ == "__main__":
    main()
