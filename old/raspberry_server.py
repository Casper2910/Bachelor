from connection.connector import server, send_data
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id, is_in_blacklist, add_to_blacklist
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key, private_key
from id_dict import id_dict, blacklist
import base64
from data.write import append_to_file
import socket

HOST = '192.168.0.133'  # own ip
PORT = 8081  # own port

ISSUER_HOST = '192.168.0.133'  # issuer ip
ISSUER_PORT = 8080  # issuer port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(HOST, PORT)
    server.listen()
    conn, addr = server.accept()

while True:
    # receives DID from arduino
    json, arduino_ip_port = server(HOST, PORT)

    # Extract the DID and temperature
    DID = json['DID']
    temperature = json['temperature']

    print('did:', DID)  # the DID String
    print(arduino_ip_port)  # tuple
    ip, _ = arduino_ip_port
    port = 8082
    print("ip:", ip)
    print("port:", port)

    # check if the arduino is blacklisted
    if is_in_blacklist(DID):
        pass

    # If DID is not verified
    elif DID not in id_dict.values():
        # Request did doc from arduino
        send_data('request-did-doc', ip, port)

        # Now wait for the response from the Arduino
        DID_doc, _ = server(HOST, PORT)

        # send did to issuer
        send_data(DID, ISSUER_HOST, ISSUER_PORT)

        # Now wait for the response from the issuer
        proof, _ = server(ISSUER_HOST, ISSUER_PORT)

        # if proof is 'no', means no proof for the Arduino
        if proof == 'no':
            add_to_blacklist(DID)
            pass

        else:
            # Add proof to did document and store it in iota
            DID_doc['proof'] = proof
            DID_doc['publicKey'] = public_key

            # upload DID document to iota tangle
            block_id = upload_block(DID_doc)

            # store associated block id to the DID
            insert_entry(block_id, DID)

    # If DID is verified
    elif DID in id_dict.values():
        # find associated block id for the DID
        block_id = find_id(DID)

        # obtain DID document for the DID
        DID_document = retrieve_block_data(block_id)

        # Decode the proof signature from base64 to binary format
        proof_base64 = DID_document['proof']
        proof_binary = base64.b64decode(proof_base64)

        # Verify proof from issuer
        if verify_proof(proof_binary, public_key, DID):
            print(f'Arduino with {DID} is verified')
            append_to_file(DID, temperature)
        else:
            print(f'Arduino with {DID} is NOT verified')

    else:
        print('ERROR')