from connection.Recieve import server, send_data
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key, private_key
from id_dict import id_dict
import base64
HOST = '192.168.0.133'  # ip
PORT = 8080  # port

# receives DID document from arduino
DID, arduino_ip_port = server(HOST, PORT)

print('did json:', DID)
print('did:', DID['DID']) # the DID String
print(arduino_ip_port)      # tuple
ip, port = arduino_ip_port
print("ip:", ip)
print("port:", port)

