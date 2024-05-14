import {
    Client,
    hexToUtf8,
    initLogger,
    TaggedDataPayload,
    utf8ToHex,
    Utils,
} from '@iota/sdk';

require('dotenv').config({ path: '.env' });

let block_id

// Define types for tag and message parameters
async function upload(tag: string, message: string) {
    // Initialize the logger
    initLogger();

    // Check if NODE_URL and EXPLORER_URL environment variables are defined
    for (const envVar of ['NODE_URL', 'EXPLORER_URL']) {
        if (!(envVar in process.env)) {
            throw new Error(`.env ${envVar} is undefined, see .env.example`);
        }
    }

    // Create a new IOTA client
    const client = new Client({
        nodes: [process.env.NODE_URL as string],
    });

    // Convert tag and message to hex format
    const options = {
        tag: utf8ToHex(tag),
        data: utf8ToHex(message),
    };

    try {
        // Generate a mnemonic
        const mnemonic = Utils.generateMnemonic();
        const secretManager = { mnemonic: mnemonic };

        // Build and post the block
        const blockIdAndBlock = await client.buildAndPostBlock(
            secretManager,
            options,
        );

        // Print the tag and data sent in a readable format
        console.log('Tag sent:', tag);
        console.log('Data sent:', message);

        // Return the block ID
        return blockIdAndBlock[0];
    } catch (error) {
        console.error('Error: ', error);
    }
}


// Call the upload function and log the block ID
upload('Hello', '{"message": "Tangle"}')
    // saving block id in variable
    .then(blockId => {
        block_id = blockId;
        console.log('Block ID:', block_id);

    })
    .catch(error => console.error('Error:', error));

console.log("hihi: " + block_id)