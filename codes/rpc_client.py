import sys, os
import socket
import pickle
import numpy

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


class foo(object):
    pass


def addit(x,y, connection):
    
    s= 0
    connection.send("ADD " + x + ' '+y)
    s =connection.recv(BUFFER_SIZE)
    s=s.split(' ')
    print " sum =",int(s[0])
    return


def calc_pi(connection):
    
    connection.send("calculate_pi ")
    print(connection.recv(BUFFER_SIZE))
    return


def sort(connection):
    cobj=foo()
    
    A=list()
    n=raw_input("enter the size of array")
    print"enter the numbers in array"
    for i in range(int(n)):
        x=raw_input("num"+str(i)+":")
        A.append(x)
    print A
    cobj.x=A    
    serial=pickle.dumps(cobj)
    connection.send("sort "+serial)
    s=pickle.loads(connection.recv(BUFFER_SIZE))
    return(s.x)

def mat(connection):
    mat1=list()
    mat2=list()
    print"enter size of matix 1"
    n1=int(input("n1: "))
    m1=int(input("m1: "))
    print"enter size of matix 2"
    n2=int(input("n2: "))
    m2=int(input("m2: ")) 
    if m1!=n2:
        print"cannot multiply"
        return  
    print "enter matrix 1"
    
    mat1 = [[int(raw_input("Enter (%s,%s): "%(i,j))) for i in range(m1)] for j in range(n1)]
    #print mat1
    print "enter matrix 2"
    mat2 = [[int(raw_input("Enter (%s,%s): "%(i,j))) for i in range(m2)] for j in range(n2)]
    #print mat2
    #for i in range(n1):
        
    #print "enter matrix 1"
    #for i in range(n1):
     #   for j in range(m1):
      #      mat1[i][j]=float(input(str(i)+","+str(j)))
    #print "enter matrix 2"
    #for i in range(n2):
     #   for j in range(m2):
      #      mat2[i][j]=float(input(str(i)+","+str(j)))
    cobj=foo()
    cobj.x=mat1
    cobj.y=mat2
    cobj.xn=n1
    cobj.xm=m1
    cobj.yn=n2
    cobj.ym=m2
    serial=pickle.dumps(cobj)
    print mat1,mat2
    connection.send("mat "+serial)
    s=pickle.loads(connection.recv(BUFFER_SIZE))
    return(s.x)
                   
    
def client_option():

    connection = get_socket()

    while True:
        menu = raw_input("Enter your choices: add,calculate_pi,sort,matrix_multiply,exit: ")
        if menu == "add":
            x= raw_input("Enter number1  ")
            y = raw_input("Enter number2  ")
            addit(x,y, connection)
        elif menu == "calculate_pi":
            calc_pi(connection)
        elif menu == "sort":
            B=sort(connection)
            print B
        elif menu == "matrix_multiply":
            pro=mat(connection)
            print pro
            
        elif menu == "exit":
            connection.send("exit ")
            break
        else:
            print "Invalid choices, choose again"
    print "Closing connection..."
    connection.close()


client_option()
