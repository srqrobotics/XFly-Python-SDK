import socket
import time
import json

UDP_IP = "192.168.4.1"
UDP_PORT = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

command_timeout = 0.5
action_timeout = 5.0

def transmit(msg):
    sock.sendto(msg, (UDP_IP, UDP_PORT))


def getMsgConfirmation():
    start_time = time.time()
    while(time.time() - start_time < command_timeout):
        data, addr = sock.recvfrom(1024)
        temp_data = json.loads(data)
        if (temp_data["validated"] == 1):
            return 1
    return 0

def getActionConfirmation():
    start_time = time.time()
    while(time.time() - start_time < action_timeout):
        data, addr = sock.recvfrom(1024)
        temp_data = json.loads(data)
        print(temp_data)
        if (temp_data["act_done"] == 1):
            return 1
    return 0

def packetMonitor(duration = 0.1):
    start_time = time.time()
    while(time.time() - start_time < duration):
        data, addr = sock.recvfrom(1024)
        temp = json.loads(data)
        print(temp)
    return 0