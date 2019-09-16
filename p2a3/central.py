import sys, os
import Queue
import socket
from thread import *
import threading
import fcntl
import time

print_lock = threading.Lock()

filename = "test.txt"
LOCK_STATUS = False
process_queue = Queue.Queue()

lockfile = open(filename, 'r+')

def acquire_lock(connection, address):
    global LOCK_STATUS, proces_queue, lockfile
    if LOCK_STATUS:
        print "["+str(address)+"] Lock can't grant"
        process_queue.put((connection, address))
        connection.send("REJECT")
    else:
        if process_queue.empty():
            print "["+str(address)+"] lock granted immediately"
            fcntl.flock(lockfile, fcntl.LOCK_EX)
            LOCK_STATUS = True
            connection.send("ACCESS")
        else:
            queue_connection = process_queue.get()
            print "processing from queue:", queue_connection[1]
            fcntl.flock(lockfile, fcntl.LOCK_EX)
            LOCK_STATUS = True
            queue_connection[0].send("ACCESS")
            print "["+str(queue_connection[1])+"] lock granted"
    time.sleep(5)
    return

def release_lock(connection, address):
    print "["+str(address)+"] releasing lock.."
    global LOCK_STATUS, process_queue, lockfile
    fcntl.flock(lockfile, fcntl.LOCK_UN)
    LOCK_STATUS = False
    connection.send("Released")
    return

#print_lock = threading.Lock()
BUFFER_SIZE = 7

def threaded(connection, address):
    for i in range(100):
        commands = connection.recv(BUFFER_SIZE)
        print "["+str(address)+"]Received command: ", commands
        input_values = commands.split(' ')
        if input_values[0] == "ACQUIRE":
            acquire_lock(connection, address)
        elif input_values[0] == "RELEASE":
            release_lock(connection, address)
        else:
            continue
    
    #print_lock.release()
    #connection.close()
    #print "[" + str(address)+ "]" + " Connection closed"

def main():
    HOST = "127.0.0.1"
    PORT = 8080
    
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s"%(PORT,HOST)
    s_socket.bind((HOST, PORT))
    
    s_socket.listen(5)
    
    while True:
        print "waiting for connection.."
        connection, address = s_socket.accept()
        print "Got connection from ", address
        print "Sending acknowledgment.."

        connection.send("ACK")

        start_new_thread(threaded, (connection,address,))
        #threaded(connection, address)

    s_socket.close()


if __name__ == '__main__':
    main()



