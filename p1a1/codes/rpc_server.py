import sys, os
import socket
from decimal import Decimal, getcontext
from thread import *
import threading
import quicksort
import pickle
import numpy
print_lock = threading.Lock()

BUFFER_SIZE = 1024

class foo(object):
    pass


def addit(connection,address,a,b):    #getting and adding the numbers
    
    s=int(a)+int(b)
    connection.send(str(s)+' ')
    return
        

def calculate_pi(connection):     #returninig the value of pi
    getcontext().prec=100
    s=sum(1/Decimal(16)**k*(Decimal(4)/(8*k+1) - Decimal(2)/(8*k+4) -Decimal(1)/(8*k+5)-Decimal(1)/(8*k+6)) for k in range(1000))
    connection.send(str(s))
    return


def sort(connection,A):         #getting the array and sorting it
    A=A.split(" ",1)
    B=pickle.loads(A[1])           #obtanining the object from serialized input
    B.x=[int(i) for i in B.x]
    B.x=quicksort.sort(B.x,len(B.x))        #persorming quicksort
    x=pickle.dumps(B)                       #serializing the result
    connection.send(x)
    return

def mat(connection,A):              #getting matrix and computing the prodcut
    A=A.split(" ",1)
    B=pickle.loads(A[1])            #obtanining the object from serialized input
    #pro=numpy.zeros((B.xn,B.ym))
    pro = [[0 for i in range(B.ym)] for j in range(B.xn)]
    for i in range (B.xn):          
        for j in range (B.ym):
            for k in range(B.xm):
                pro[i][j]+=B.x[i][k]*B.y[k][j]
    B.x=pro
    serial=pickle.dumps(B)          #serializing the result
    connection.send(serial)
    return
    

    
        
def threaded(connection, address):
    while True:
        commands = connection.recv(BUFFER_SIZE)
        input_values = commands.split(' ')
        if input_values[0] == "ADD":
            print_lock.acquire()
            addit(connection,address,input_values[1],input_values[2])
            print_lock.release()
        elif input_values[0] == "calculate_pi":
            print_lock.acquire()
            calculate_pi(connection)
            print_lock.release()
        elif input_values[0] == "sort":
            print_lock.acquire()
            sort(connection,commands)
            print_lock.release()
        elif input_values[0] == "mat":
            print_lock.acquire()
            mat(connection,commands)
            print_lock.release()
        elif input_values[0] == "exit":
            break
    
    #print_lock.release()
    connection.close()
    print "Connection closed: ", address
    
    #return
#threads=[]
def main():
    HOST = "127.0.0.1"
    PORT = 8080
    
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Starting server on port %s and server %s"%(PORT,HOST)
    s_socket.bind((HOST, PORT))
    
    s_socket.listen(5)
    try :
        while True:
            print "waiting for connection..press control+c  to exit server"
            try:
                key=win.getkey()
            except:
                key=None
            if key==" ":
                break
            connection, address = s_socket.accept()
            #print_lock.acquire()
            print "Got connection from ", address
            print "Sending acknowledgment.."

            connection.send("ACK")

            start_new_thread(threaded, (connection,address,))
            #threads.append(nt)
    except KeyboardInterrupt:
        pass
    print "\n server closed.."
    s_socket.close()
    #for thrd in threads:
        #thrd.join()
    

if __name__ == '__main__':
    main()
