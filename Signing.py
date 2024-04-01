from cryptography.hazmat.primitives.asymmetric import ed25519
from key_to_bytes import key_to_bytes


def sign(message, key):
    try:
        # Convert key to bytes
        key_bytes = key_to_bytes(key)
        if key_bytes is None:
            return None

        # Check if the private key bytes have the correct length
        if len(key_bytes) != 32:
            print("Error: Invalid key length. Ed25519 private key should be 32 bytes long.")
            return None

        # Deserialize the private key
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes)

        # Sign the message
        signature = private_key.sign(message.encode('utf-8'))

        return signature
    except Exception as e:
        print("Error:", e)
        return None


# Example usage
private_key_pem = """
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACCxT0HlJknXPScgNMQM4doq4leJ4yGyPBGBtXNlaWFCtQAAAJh64bC3euGw
twAAAAtzc2gtZWQyNTUxOQAAACCxT0HlJknXPScgNMQM4doq4leJ4yGyPBGBtXNlaWFCtQ
AAAEDkqygDl+HsGtr/taNxQoZFvfMzNZ95jVHBmYTjqP6jqrFPQeUmSdc9JyA0xAzh2iri
V4njIbI8EYG1c2VpYUK1AAAAE2Nhc3BlQEhhcmJvZS1LYXNzZW4BAg==
-----END OPENSSH PRIVATE KEY-----
"""

# Use the private key bytes to sign a message
message = "Hello"
signature = sign(message, private_key_pem)
if signature:
    print("Signature:", signature.hex())
