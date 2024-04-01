from cryptography.hazmat.primitives.serialization import load_ssh_private_key, load_ssh_public_key

private_key = load_ssh_private_key(
    b"""-----BEGIN OPENSSH PRIVATE KEY-----
    b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
    QyNTUxOQAAACCxT0HlJknXPScgNMQM4doq4leJ4yGyPBGBtXNlaWFCtQAAAJh64bC3euGw
    twAAAAtzc2gtZWQyNTUxOQAAACCxT0HlJknXPScgNMQM4doq4leJ4yGyPBGBtXNlaWFCtQ
    AAAEDkqygDl+HsGtr/taNxQoZFvfMzNZ95jVHBmYTjqP6jqrFPQeUmSdc9JyA0xAzh2iri
    V4njIbI8EYG1c2VpYUK1AAAAE2Nhc3BlQEhhcmJvZS1LYXNzZW4BAg==
    -----END OPENSSH PRIVATE KEY-----""",
    password=None,)

signature = private_key.sign(b"hello")

print(signature)

# Load the public key
public_key = load_ssh_public_key(
    b'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILFPQeUmSdc9JyA0xAzh2iriV4njIbI8EYG1c2VpYUK1')

# Verify the signature
try:
    public_key.verify(signature, b"hello")
    print("Signature verified successfully.")
except Exception as e:
    print("Verification failed:", e)