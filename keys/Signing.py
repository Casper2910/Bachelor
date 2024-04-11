from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key
import multibase


def sign_proof(message, private_key_, public_key_):
    # Load the private key
    private_key_object = load_ssh_private_key(private_key_, password=None, )

    # Sign the message
    signature = private_key_object.sign(message.encode('utf-8'))

    # Encode the public key using multibase
    base58 = multibase.encode('base58btc', public_key_)
    decoded = multibase.decode(base58)
    utf8_decoded = decoded.decode('utf-8')

    return signature


def verify_proof(signature, public_key_, message):
    # Verify the signature
    public_key_object = load_ssh_public_key(public_key_)
    try:
        public_key_object.verify(signature, message.encode('utf-8'))
        return True
    except Exception as e:
        return False


# Example usage
if __name__ == "__main__":
    from keys import public_key, private_key
    identifier = 'did:iota:test1'
    signature = sign_proof(identifier, private_key, public_key)
    print(signature)
    print(verify_proof(signature, public_key, identifier))

    print(verify_proof(b'\x92\x7f\x9b\x7f\xc2G\xc7\x14G\xab\xcfs(\xb7|\xa41I\xe8T\x10\x9d\x05\xf7z%\xd7\xf6\xab\xd3\x19\x0c\x8b\x05\xf3\x8a\x91^w\xb2\xf0\xd6Y|\xf7wWx\x81\xce/\x15\xa8\x8a\x00{\xe8\xdb\xac\x95\x80s9\x05', public_key, 'did:iota:test6'))
