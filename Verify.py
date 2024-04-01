from cryptography.hazmat.primitives.asymmetric import ed25519
import base64

def verify(signature, public_key, message):
    try:
        # Decode the public key
        public_key_bytes = base64.b64decode(public_key.split()[1])

        # Deserialize the public key
        public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)

        # Verify the signature
        public_key_obj.verify(signature, message.encode('utf-8'))

        return True  # Signature verification successful
    except Exception as e:
        print("Error:", e)
        return False  # Signature verification failed


# Example usage
public_key = """
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILFPQeUmSdc9JyA0xAzh2iriV4njIbI8EYG1c2VpYUK1
"""

# Assume `signature` is already defined
message = "Hello"
signature = '42182bcd8f401f63e310268fdc9e71f3ac8da1505fab08b057bd87d184c330f973299f18f38cb2a07c53684900feb842aac2f266befc877db610d2eed5a6ed0d'
if verify(signature, public_key, message):
    print("Signature is valid")
else:
    print("Signature is not valid")
