import socket
import threading
import time
import json
import base64
from connection.connector import send_data, receive_data, receive_specific_data
from keys.Signing import verify_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_blacklisted, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key
from id_dict import id_dict
from blacklist import blacklist
from data.write import append_to_file

HOST = '192.168.0.141'  # own ip
PORT = 8081  # own port

ISSUER_HOST = '192.168.0.133'  # issuer ip
ISSUER_PORT = 8080  # issuer port


def handle_device(rasp_socket, ip, port):
    while True:
        json_data = receive_data(rasp_socket)
        if json_data:
            DID = json_data['DID']
            temperature = json_data['temperature']
            print('did:', DID)  # the DID String
            print(ip, port)  # tuple

            # Arduino server dest
            ARDUINO_HOST = ip
            ARDUINO_PORT = port

            if is_blacklisted(DID):
                pass

            elif DID not in id_dict.values():
                # 69420 is the code for request of did doc
                send_data(69420, ARDUINO_HOST, 8082)  # Arduino's is listening on port 8082
                DID_doc = receive_data(rasp_socket)
                received_proof = None
                # Receive proof response
                print('waiting for proof')

                while received_proof == None:
                    print('DID_doc:', DID_doc)
                    print(received_proof)

                    # Listening for incoming data from issuer
                    # ask for proof
                    send_data(DID, ISSUER_HOST, ISSUER_PORT)
                    received_proof = receive_specific_data(rasp_socket, ISSUER_HOST)
                    time.sleep(5)

                if received_proof == 'no':
                    add_to_blacklist(DID)
                    pass

                else:
                    print(received_proof)
                    print('ses')
                    DID_doc['proof'] = received_proof
                    DID_doc['publicKey'] = public_key
                    block_id = upload_block(DID_doc)
                    insert_entry(block_id, DID)

            elif DID in id_dict.values():
                block_id = find_id(DID)
                DID_document = retrieve_block_data(block_id)
                proof_base64 = DID_document['proof']
                proof_binary = base64.b64decode(proof_base64)
                if verify_proof(proof_binary, public_key, DID):
                    print(f'Arduino with {DID} is verified')
                    append_to_file(DID, temperature)
                else:
                    print(f'Arduino with {DID} is NOT verified')
            else:
                print('ERROR')
        else:
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            ip, port = addr
            print(f"Connection from {ip}:{port}")
            device_thread = threading.Thread(target=handle_device, args=(conn, ip, port))
            device_thread.start()


if __name__ == "__main__":
    main()
