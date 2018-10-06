import time
def partition(A,p,r):       #the partition function
    x=A[r]                  #last element is pivot
    i=p-1
    for j in range(p,r):        #sorting using pivot
        if A[j]<=x:
            i=i+1
            A[i],A[j]=A[j],A[i]
    A[i+1],A[r]=A[r],A[i+1]
    return i+1
def quicksort(A,p,r):
    if p<r:
        q=partition(A,p,r)
        quicksort(A,p,q-1)
        quicksort(A,q+1,r)
def sort(A,s):                  #this function makes it easy to input this file into other programs
    p = 0
    r = s-1
    strt=time.time()            #timing the algorithm
    quicksort(A,p,r)
    #print"time: ",(time.time()-strt)
    return A
    



if __name__ == '__main__':
    
    A = list()
    size=int(input("Enter the size of the array"))
    print("enter numbers in array:")
    for i in range(size):
        a=int(input("element:"))
        A.append(a)
    
    p = 0
    r = size-1
    #print"Unsorted Array: ",A
    A=sort(A,size)
    #print"Sorted Array: ",A
