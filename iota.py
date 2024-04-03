import os
import json

from dotenv import load_dotenv

# Import the python iota client
# Make sure you have first installed it with `pip install iota_sdk`
from iota_sdk import Client, hex_to_utf8, utf8_to_hex

load_dotenv()

node_url = os.environ.get('NODE_URL', 'https://api.testnet.shimmer.network')

# Create a Client instance
client = Client(nodes=[node_url])


########################################################
# Step 1: Prepare the data in JSON format for your block
########################################################
# Data is submitted to the Shimmer network as a block.
# This block can contain a 'payload' with data.
# This payload has a 'tag' and the 'data' itself, both in hex format.
# The Shimmer network requires a "0x" at the beginning of hex strings.

# Prepare JSON data
data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Convert JSON to string
data_str = json.dumps(data)

# Convert to hex
data_hex = utf8_to_hex(data_str)

print('\nYour prepared block content is:')
print(f'  data: {data_str}')
print(f'  data converted to hex: {data_hex}')


########################################################
# Step 2: Submit your block to the Shimmer test network
########################################################
# A block must be built, to which the payload is attached.
# The build_and_post_block function handles this task.

# Create and post a block with a JSON data payload
# The client returns your block data (blockIdAndBlock)
blockIdAndBlock = client.build_and_post_block(
    secret_manager=None, tag=None, data=data_hex)

block_id = blockIdAndBlock[0]
block = blockIdAndBlock[1]

print('\nThe block ID for your submitted block is:')
print(f'  {block_id}')

print('\nMetadata for your submitted block is:')
print(f'  {block}')


########################################################
# Step 3: Use the block ID to read the payload back
########################################################
# The network can be queried using the block ID.
# There are two methods to query the network.
#   get_block_metadata - metadata only
#   get_block_data - metadata and payload

# Get the metadata for the block
metadata = client.get_block_metadata(block_id)

# Get the whole block
block = client.get_block_data(block_id)
payload_out = block.payload

# Unpackage the payload (from hex to JSON)
data_hex_out = block.payload.data
data_str_out = hex_to_utf8(data_hex_out)
data_out = json.loads(data_str_out)
print('\nYour data, read from the Shimmer network:')
print(f'  {data_out}')
