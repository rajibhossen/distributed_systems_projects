import random
import socket
import time
from queue import Queue
from threading import Thread
import pickle
import copy
multicast_ports = [6001, 6002, 6003]
multicast_group = "127.0.0.1"
PID = 0
own_port = 6001
event_queue = Queue()
ack_list = []
own_events = Queue()
class e():
    vec=[0]*3
    ppid = 1 
own=e()
    

class ReceiverThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.bind((multicast_group, own_port))

        while True:
            data, address = sock.recvfrom(1024)
            event =pickle.loads(data)
            if(event.ppid !=PID+1):
                #print("qwe")
                event_queue.put(event)
            

class ProcessingThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


    def run(self):
        
        while True:
            try:
                event = event_queue.get()
                v=event.vec
                p=event.ppid-1
                #print(p,v,own.vec)
            except Exception as e:
                continue
            #print("[%s] queue top event: %s" % (str(PID), event))
            #event_pid, event_id = event.split('.')
            #event_pid = int(event_pid)
            #event_id = int(event_id)
            flag =0
            #print("qqq")
            si=event_queue.qsize()
            if (v[p]==own.vec[p]+1):
                for i in range(len(v)):
                    if (v[i]<=own.vec[i]):
                        flag =1
                    else:
                        flag =0
            for i in range(len(v)):
                own.vec[i]=max(own.vec[i],v[i])
            if(flag == 1):
                print(PID+1,": msg delivered vector updated:",own.vec)

                

class EventThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.event_count = 0

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        no=0
        while True:
            #time.sleep(1)
            rand_number = random.randint(0,1000000)
            if rand_number == 0 and no<=5:
                no=no+1
                #print (own.vec)
                self.event_count += 1
                own.vec[PID]=self.event_count
                #print(own.vec[PID])
                event =copy.deepcopy(own)
                event.vec=copy.deepcopy(own.vec)
                event.ppid=copy.deepcopy(own.ppid)
                event.vec[PID]=event.vec[PID]
                print("send event, updating vector",event.vec)
                #event = event.encode('utf-8')
                #own_events.put(event)
                x = pickle.dumps(event)
                for port in multicast_ports:
                    sock.sendto(x, (multicast_group, port))
                time.sleep(5)



rcvthread = ReceiverThread()
sendthread = EventThread()
process_thread = ProcessingThread()

rcvthread.start()
time.sleep(2)
sendthread.start()
process_thread.start()


