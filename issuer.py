import socket
import threading
from connection.connector import send_data, server
from keys.Signing import sign_proof
from keys.keys import public_key, private_key
import queue

HOST = '192.168.0.133'  # ip
PORT = 8080  # port

proof_queue = queue.Queue()


def handle_request():
    while True:
        DID, verifier = proof_queue.get()
        VERIFIER_HOST, VERIFIER_PORT = verifier

        while True:
            answer = input(f'Do you want to deliver proof for: {DID} \n Yes \n No \n').lower()

            if answer == 'yes':
                proof = sign_proof(DID, private_key, public_key)
                send_data(proof, VERIFIER_HOST, VERIFIER_PORT)
                break

            elif answer == 'no':
                send_data('no', VERIFIER_HOST, VERIFIER_PORT)
                break

            else:
                print('Invalid input')


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        # Start a thread to handle proof requests
        threading.Thread(target=handle_request, daemon=True).start()

        while True:
            DID, verifier = server(HOST, PORT)
            proof_queue.put((DID, verifier))


if __name__ == "__main__":
    main()
