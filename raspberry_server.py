from connection.Recieve import server, send_data
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key
from id_dict import id_dict
import base64
HOST = '192.168.0.133'  # ip
PORT = 8080  # port

# receives DID document from arduino
DIDjson, arduino_ip_port = server(HOST, PORT)

print('did json:', DIDjson)
print('did:', DIDjson['DID']) # the DID String
DID = DIDjson['DID']
print(arduino_ip_port)      # tuple
ip, port = arduino_ip_port
print("ip:", ip)
print("port:", port)

if DID not in id_dict.values():
    # Request did doc from arduino
    send_data('request-did-doc', ip, port)

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
    else:
        print(f'Arduino with {DID} is NOT verified')