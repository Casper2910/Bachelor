import os
from dotenv import load_dotenv
from iota_sdk import Client, hex_to_utf8, utf8_to_hex

load_dotenv()

node_url = os.environ.get('NODE_URL', 'https://api.testnet.shimmer.network')
client = Client(nodes=[node_url])


########################################################
# Step 1: Prepare the DID document in hex format
########################################################
# Example DID document
did_document = {
    "id": "did:example:123456",
    "publicKey": [{
        "id": "did:example:123456#key-1",
        "type": "Ed25519VerificationKey2018",
        "controller": "did:example:123456",
        "publicKeyBase58": "pub_key_base58_here"
    }],
    "authentication": ["did:example:123456#key-1"],
    "service": [{
        "id": "did:example:123456#vcs",
        "type": "VerifiableCredentialService",
        "serviceEndpoint": "https://example.com/vc/"
    }]
}

# Convert to hex
did_document_hex = utf8_to_hex(str(did_document))


########################################################
# Step 2: Submit the DID document to the Shimmer network
########################################################
blockIdAndBlock = client.build_and_post_block(
    secret_manager=None, tag=utf8_to_hex('DID'), data=did_document_hex)

block_id = blockIdAndBlock[0]
block = blockIdAndBlock[1]

print('\nThe block ID for your submitted block is:')
print(f'  {block_id}')

print('\nMetadata for your submitted block is:')
print(f'  {block}')


########################################################
# Step 3: Retrieve and Resolve the DID document
########################################################
# Get the whole block
block = client.get_block_data(block_id)
did_document_hex_out = block.payload.data

# Unpackage the DID document (from hex to text)
did_document_out = hex_to_utf8(did_document_hex_out)
print('\nYour DID document, read from the Shimmer network:')
print(f'  {did_document_out}')

# Or see the DID document online, with the testnet explorer.
print(
    f'\nOr see the document with the testnet explorer: {os.environ["EXPLORER_URL"]}/block/{block_id}')
