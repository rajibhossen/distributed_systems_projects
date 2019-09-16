import sys, os
import socket
import time

HOST = "127.0.0.1"
PORT = 8080
BUFFER_SIZE = 7

filename = "test.txt"

def get_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connecting to port %s and server %s"%(PORT,HOST)
    server_socket.connect((HOST, PORT))
    ack = server_socket.recv(BUFFER_SIZE)
    if ack == "ACK":
        print "Connected to server and got acknowledgments: ",ack
        return server_socket

def main():
    connection = get_socket()
    for i in range(50):
        print "Requesting for access..."
        connection.send("ACQUIRE")
        data = connection.recv(BUFFER_SIZE)
        if data == "ACCESS":
            print "Got Access. Editing File..."
            fileobj = open(filename, 'r+')
            content = int(fileobj.read())
            fileobj.seek(0)
            fileobj.write(str(content+1))
            fileobj.close()
            print "After adding, file content is: " + str(content + 1)
            connection.send("RELEASE")
            data = connection.recv(BUFFER_SIZE)
        elif data == "REJECT":
            print "Access denied. retry again.."

    print "Closing connection..."
    connection.close()

main()
