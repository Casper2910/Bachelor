from connection.Recieve import server, send_data
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_in_blacklist, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key, private_key
from id_dict import id_dict, blacklist
import base64

HOST = '192.168.0.133'  # ip
PORT = 8080  # port

VERIFIER_Host = '192.168.0.133'  # raspberry pi ip
VERIFIER_PORT = 8081  # raspberry pi port

while True:
    DID = server(HOST, PORT)

    while True:

        answer = input(f'Do you want to deliver proof for: {DID} \n Yes \n No').lower()

        if answer == 'yes':
            proof = sign_proof(DID, private_key, public_key)

            # send proof to raspberry Pi
            send_data(DID, VERIFIER_Host, VERIFIER_PORT)
            break

        elif answer == 'no':
            # send proof to raspberry Pi
            send_data('no', VERIFIER_Host, VERIFIER_PORT)
            break

        else:
            print('invalid input')
