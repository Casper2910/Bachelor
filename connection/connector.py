import socket
import json


def send_string(data, ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ip, port))
            client_socket.sendall(data.encode())
            print("Data sent to:", ip, port)

    except Exception as e:
        print("Error sending data:", e)


def send_json(data, ip, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to the Arduino
            client_socket.connect((ip, port))

            # Convert the data to JSON format
            json_data = json.dumps(data)

            # Send the JSON data to the Arduino
            client_socket.sendall(json_data.encode())

            print("Data sent to Arduino:", data)

    except Exception as e:
        print("Error sending data to Arduino:", e)


def receive_specific_data_json(socket_obj, check_ip):
    while True:
        try:
            data, addr = socket_obj.recvfrom(1024)
            ip, port = addr
            if ip == check_ip:
                return json.loads(data.decode())
            else:
                return None
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break
    return None


def receive_specific_data_string(socket_obj, check_ip):
    while True:
        try:
            data, addr = socket_obj.recvfrom(1024)
            ip, port = addr
            if ip == check_ip:
                return data.decode()
            else:
                return None
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break
    return None


def receive_json(socket_obj):
    while True:
        try:
            data = socket_obj.recv(1024)
            if data:
                return json.loads(data.decode())
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break
    return None


def obtain_ip():
    try:
        # Create a socket and connect to an external IP (doesn't have to be reachable)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS server (can be any reachable IP)
        ip_address = s.getsockname()[0]  # Get the IP address of the local end of the socket
        s.close()
        return ip_address
    except Exception as e:
        return str(e)


# Example usage
if __name__ == "__main__":
    ip_address = obtain_ip()
    print(f"The device IP address is: {ip_address}")
