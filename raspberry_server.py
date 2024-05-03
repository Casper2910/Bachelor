import socket
import threading
import json
import base64
from connection.connector import send_data
from keys.Signing import verify_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_in_blacklist, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key
from id_dict import id_dict, blacklist
from data.write import append_to_file

HOST = '192.168.0.133'  # own ip
PORT = 8081  # own port

ISSUER_HOST = '192.168.0.133'  # issuer ip
ISSUER_PORT = 8080  # issuer port


def receive_data(socket_obj):
    while True:
        try:
            data = socket_obj.recv(1024)
            if data:
                return json.loads(data.decode())
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break
    return None


def handle_device(socket_obj, ip, port):
    while True:
        json_data = receive_data(socket_obj)
        if json_data:
            DID = json_data['DID']
            temperature = json_data['temperature']
            print('did:', DID)  # the DID String
            print(ip, port)  # tuple
            print("ip:", ip)
            print("port:", port)

            if is_in_blacklist(DID):
                pass
            elif DID not in id_dict.values():
                send_data('request-did-doc', ip, port)
                DID_doc = receive_data(socket_obj)
                send_data(DID, ISSUER_HOST, ISSUER_PORT)
                proof = receive_data(socket_obj)

                if proof == 'no':
                    add_to_blacklist(DID)
                    pass
                else:
                    DID_doc['proof'] = proof
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
