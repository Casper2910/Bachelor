from cryptography.hazmat.primitives import serialization
import base64


def key_to_bytes(key):
    try:
        # Remove any leading/trailing whitespaces
        key = key.strip()

        # Remove the header and footer lines if present
        if key.startswith("-----BEGIN ") and key.endswith("-----"):
            key = key[key.find("\n")+1:key.rfind("\n")]

        # Decode the key content from base64
        key_bytes = base64.b64decode(key)

        return key_bytes
    except Exception as e:
        print("Error:", e)
        return None
