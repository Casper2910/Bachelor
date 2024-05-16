import socket
import threading
import base64
import json
import time
from queue import Queue
import os
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

REQUESTS_FILE = "auth_requests.json"


def store_request(data):
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)
    else:
        requests = []

    requests.append(data)

    with open(REQUESTS_FILE, "w") as file:
        json.dump(requests, file)


def send_stored_requests(issuer_socket):
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)

        for request in requests:
            issuer_socket.send(json.dumps(request).encode("utf-8"))
            proof = issuer_socket.recv(1024).decode("utf-8")

            if proof == 'no':
                add_to_blacklist(request['DID'])
            else:
                request['DID_doc']['proof'] = proof
                request['DID_doc']['publicKey'] = public_key
                block_id = upload_block(request['DID_doc'])
                insert_entry(block_id, request['DID'])

        os.remove(REQUESTS_FILE)


def handle_device(device_queue):
    while True:
        device_socket, device_address = device_queue.get()
        received_data = device_socket.recv(1024).decode("utf-8").strip()
        print('Data:', received_data)

        data = json.loads(received_data)
        DID = data['DID']
        temp = data['temperature']

        if is_blacklisted(DID):
            print('DID is blacklisted')
            continue

        if DID not in id_dict.values():
            print('New DID')
            send_json(69420, device_address[0], 8082)
            while True:
                print('Awaiting DID document from device...')
                received_data = device_socket.recv(1024).decode("utf-8")
                received_json = json.loads(received_data)
                if "proof" in received_json:
                    DID_doc = received_json
                    print('DID doc:', DID_doc)
                    break

            request_data = {
                "DID": DID,
                "DID_doc": DID_doc
            }

            store_request(request_data)
            print("Request stored due to issuer being down or for later processing")

        else:
            print('Known DID')
            block_id = find_id(DID)
            DID_document = retrieve_block_data(block_id)
            proof_base64 = DID_document['proof']
            proof_binary = base64.b64decode(proof_base64)

            if verify_proof(proof_binary, public_key, DID):
                print(f'Arduino with {DID} is verified')
                for i in range(100):
                    append_to_file(DID, temp)
            else:
                print(f'Arduino with {DID} is NOT verified')


def connect_to_issuer():
    while True:
        try:
            issuer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            issuer_socket.connect((ISSUER_HOST, ISSUER_PORT))
            print("Connected to issuer")
            send_stored_requests(issuer_socket)
            return issuer_socket
        except (ConnectionRefusedError, socket.error):
            print("Issuer is down, retrying in 5 seconds...")
            time.sleep(5)


def main():
    device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Device socket listening for connections on {HOST, PORT}...")

    device_socket.bind((HOST, PORT))
    device_socket.listen(5)
    device_queue = Queue()

    device_handler_thread = threading.Thread(target=handle_device, args=(device_queue,))
    device_handler_thread.start()

    issuer_socket = None

    while True:
        try:
            if issuer_socket is None:
                issuer_socket = connect_to_issuer()

            device_conn, device_address = device_socket.accept()
            print("Connection from device:", device_address)
            device_queue.put((device_conn, device_address))

        except (ConnectionRefusedError, socket.error):
            issuer_socket = None
            print("Lost connection to the issuer, retrying...")

if __name__ == "__main__":
    main()
