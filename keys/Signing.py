from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key
import multibase
from keys import private_key, public_key


def sign_proof(identifier):
    # Load the private key
    private_key_object = load_ssh_private_key(private_key, password=None, )

    # Sign the message
    signature = private_key_object.sign(identifier.encode('utf-8'))

    # Encode the public key using multibase
    base58 = multibase.encode('base58btc', public_key)
    decoded = multibase.decode(base58)
    utf8_decoded = decoded.decode('utf-8')

    return signature


def verify_proof(signature, public_key, identifier):
    # Verify the signature
    public_key_object = load_ssh_public_key(public_key)
    try:
        public_key_object.verify(signature, identifier.encode('utf-8'))
        return True
    except Exception as e:
        return False


# Example usage
if __name__ == "__main__":
    identifier = 'did:iota:test1'
    signature = sign_proof(identifier)
    print(signature)
    print(verify_proof(signature, public_key, identifier))
