import time, threading
import os
from os.path import isfile, join
import platform
import socket

CLIENT_DIR = "/home/rajib/Courses/Distributed_Systems_5306/project1/client_dir/" 

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 1024

def get_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to port %s and server %s"%(PORT,HOST)
    server_socket.connect((HOST, PORT))
    ack = server_socket.recv(BUFFER_SIZE)
    if ack == "ACK":
        print "Connected to server and got acknowledgments: ",ack
        return server_socket

def get_creation_time(filepath):
    filepath = CLIENT_DIR + filepath
    stat = os.stat(filepath)
    
    birthtime, modified = "", ""
    try:
        birthtime = stat.st_birthtime
    except AttributeError:
        modified = stat.st_mtime
    if modified:
        return modified
    else:
        return birthtime

def upload_file(filename):
    connection = get_socket()
    connection.send("UPLOAD " + filename)
    filepath = CLIENT_DIR + filename 
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f_send:
            print "Sending data.."
            data = f_send.read()
            connection.send(data)
            print "Sent....."
        connection.close()
        #success = connection.recv(BUFFER_SIZE)
        print "Uploaded file successfully: ", filename
    else:
        print "File not found"
    connection.close()
    return

def delete_file(filename):
    connection = get_socket()
    connection.send("DELETE " + filename)
    message = connection.recv(BUFFER_SIZE)
    print "Server Message: ", message
    connection.close()
    return

next_iteration_files = []
last_update_time = ""
iteration = 0
def synchronize():
    global next_iteration_files,last_update_time,iteration
    print(iteration, time.ctime())
    onlyfiles = [f for f in os.listdir(CLIENT_DIR) if isfile(join(CLIENT_DIR, f))] 
    if iteration == 0:
        next_iteration_files = onlyfiles
        last_upadte_time = time.time()
        
        print "Uploading all files initially"
        
        for singlefile in onlyfiles:
            upload_file(singlefile)
        print "Sync Complete"
    else:
        new_files = list(set(onlyfiles) - set(next_iteration_files))
        for singlefile in new_files:
            print "Uploading new file... "
            upload_file(singlefile)

        for singlefile in onlyfiles:
            update_time = get_creation_time(singlefile)
            if update_time > last_update_time:
                print "Updating old file..."
                upload_file(singlefile)
        
        deleted_files = list(set(next_iteration_files) - set(onlyfiles))
        
        for singlefile in deleted_files:
            print "Deleting Files..."
            delete_file(singlefile)
        print "Sync complete.."
        last_update_time = time.time()
        next_iteration_files = onlyfiles
    iteration += 1
    print "Waiting for next iteration.."
    
    threading.Timer(10, synchronize).start()
    

synchronize()


