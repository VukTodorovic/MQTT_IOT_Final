# Broker

import socket
import threading
import time

# Define the IP addresses and port number to send and receive on
UDP_IP = "0.0.0.0"  # Listen on all available network interfaces
UDP_PORT = 1337
BROADCAST_IP = "192.168.0.255"  # Broadcast IP

# Create a UDP socket for receiving responses
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen_sock.bind((UDP_IP, UDP_PORT))

# Create a separate thread for receiving responses
def receive_responses():
    while True:
        data, addr = listen_sock.recvfrom(1024)  # Buffer size is 1024 bytes
        decoded_message = data.decode("utf-8")
        if decoded_message.startswith("NOTIFY"):
            # Extract values from NOTIFY message
            message_lines = decoded_message.splitlines()
            SERVER = message_lines[6].replace("SERVER: ", "")

            print("\nReceived response from", addr[0], SERVER)
            print(f"Response contents:\n{decoded_message}\n")


# Start the response-receiving thread
response_thread = threading.Thread(target=receive_responses)
response_thread.daemon = True
response_thread.start()

# Create a UDP socket for sending messages
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# M-SEARCH SSDP message
def gen_msearch_ssdp():
    return "M-SEARCH * HTTP/1.1\r\nHOST: 192.168.0.255:1337\r\nMAN: ssdp:discover\r\nMX: 4\r\nST: null\r\nUSER-AGENT: WIN10.\r\nCPFN.UPNP.ORG: server\r\nCPUUID.UPNP.ORG: f81d4fae-7dec-11d0-a765-00a0c91e6bf6"


# Send a message to the broadcast IP address every 5 seconds
while True:
    print("\n[!] Scanning the network for available devices...\n")
    message = gen_msearch_ssdp()
    send_sock.sendto(message.encode("utf-8"), (BROADCAST_IP, UDP_PORT))
    time.sleep(10)
