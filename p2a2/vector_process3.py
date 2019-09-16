import pickle
import random
import socket
import time
from queue import Queue
from threading import Thread

multicast_ports = [6001, 6002]
multicast_group = "127.0.0.1"
PID = 3
own_port = 6003
event_queue = Queue()
ack_list = []
own_events = Queue()
vector = [0, 0, 0]


class ReceiverThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global vector
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((multicast_group, own_port))

        while True:
            data, address = sock.recvfrom(1024)
            data = pickle.loads(data)
            vector = data
            print("[" + str(PID) + "] RECEIVED: ", vector)


class EventThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global vector
        print("Please wait for some time to generate events")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        while True:
            # time.sleep(1)
            rand_number = random.randint(0, 1000000)
            if rand_number == 0:
                vector[PID - 1] += 1
                message = pickle.dumps(vector)
                print("[" + str(PID) + "]: ", vector)
                for port in multicast_ports:
                    sock.sendto(message, (multicast_group, port))


rcvthread = ReceiverThread()
sendthread = EventThread()
# process_thread = ProcessingThread()

rcvthread.start()
time.sleep(2)
sendthread.start()
# process_thread.start()
