from connection.Recieve import server
from keys.Signing import verify_proof, sign_proof
from block_id_dictonary.write_read_dict import insert_entry, find_id
from iota.block_handler import upload_block, retrieve_block_data
from keys.keys import public_key, private_key
from id_dict import id_dict
import base64
HOST = '192.168.0.133'  # ip
PORT = 8080  # port

# receives DID document from arduino
DID_doc = server(HOST, PORT)
DID = DID_doc['id']

print('did:', DID)
print('did doc:', DID_doc)

# check if DID document needs to be authenticated by issuer
if DID_doc['proof'] == 'NEEDS_PROOF' and DID not in id_dict.values():

    # give proof by signing:
    answer = input(f"Do you want to deliver proof for ID: {DID}? (Yes/No): ").lower()

    if answer == 'yes':
        # Call the sign_proof function
        proof = sign_proof(DID, private_key, public_key)
        DID_doc['proof'] = proof
        print(proof)
        print(DID_doc['proof'])
        response = f'proof delivered for {DID}'

        # upload DID document to iota tangle
        block_id = upload_block(DID_doc)

        # store associated block id to the DID
        insert_entry(block_id, DID)

    else:
        response = f'"Proof declined for {DID}'

# otherwise, lookup the DID document for the given DID in iota tangle
else:
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
