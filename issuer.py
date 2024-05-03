import socket
import threading
import time
import json
import base64
from connection.connector import send_json, receive_specific_data_json, receive_specific_data_string
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import pop_queue_list, add_to_queue_list
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key, private_key
from id_dict import id_dict
from blacklist import blacklist
from data.write import append_to_file
from queue_list import queue_list

HOST = '192.168.0.133'  # ip
PORT = 8080  # port

VERIFIER_HOST = '192.168.0.141'  # own ip
VERIFIER_PORT = 8081  # own port


def handle_request(issuer_socket, ip, port):
    DID = receive_data(issuer_socket)
    if DID:
        answer = input(f'Do you want to deliver proof for: {DID} \n Yes \n No \n').lower()

        if answer == 'yes':
            proof = sign_proof(DID, private_key, public_key)
            print(proof)
            send_json({"proof": proof}, VERIFIER_HOST, VERIFIER_PORT)
            pop_queue_list()

        elif answer == 'no':
            send_json('no', VERIFIER_HOST, VERIFIER_PORT)
            pop_queue_list()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            ip, port = addr
            print(f"Connection from {ip}:{port}")
            device_thread = threading.Thread(target=handle_request, args=(conn, ip, port))
            device_thread.start()


if __name__ == "__main__":
    main()
