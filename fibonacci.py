
#%% return the first N values of the Fibonacci number
def fibo(length, init_num=1):
    vector = [init_num]
    if length == 1:
        pass
    elif length == 2:
        vector.append(1)
    else:
        vector.append(1)
        i = 3
        while i<length+1:
            vector.append(vector[-1]+vector[-2])
            i += 1
    return vector

#%% return the Nth value in Fibonacci number

def fiboN(N):
    m = dict()
    m[0]=1; m[1]=1
    
    def fib(m, N):
        if N not in m.keys():
            m[N] = fib(m, N-1) + fib(m, N-2)
        return m

#%% return the first N values of the Fibonacci sequence
def fibo(n):
    if n == 0:
        return [0]
    if n == 1:
        return [0, 1]
    
    return fibo(n-1) + [fibo(n-1)[-1]+fibo(n-1)[-2]]

print fibo(8)

#%% return the Nth value of the Fibonacci sequence
def fibo(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    return fibo(n-1)+fibo(n-2)

print fibo(0)
print fibo(1)
print fibo(2)
print fibo(3)
print fibo(4)
print fibo(5)
print fibo(6)
print fibo(7)

#%% return the minimum number of steps to reach end of array
def minSteps(l):
    n = len(l)
    jumps = [0]*n
    if n==1:
        return 0
        
    if l[0] == 0:
        return 1e99
    
    i = 1
    while i < n:
        jumps[i] = 1e99
        j = 0
        while j < i:
            if (j+l[j]>=i) & (jumps[j]!= 1e99):
                jumps[i] = min(jumps[i], jumps[j]+1)
            j+=1
        i+=1
    return jumps[n-1]
    
    
#%% skipping stones
#move from left to right, by the value at the index but only to right; 
#return if there is a solution
def stones(l):
    n = len(l)
    flags = [0]*n; flags[0]=1
    indexes = []
    if n==1:
        return True
    
    if l[0]==0:
        return False
        
    i = 1
    while i<n:
        j = 0
        while j<i:
            if (j+l[j]==i) & (flags[j]==1):
                flags[i] = 1
                indexes.append(j)
            j+=1
        i+=1
    return bool(flags[-1]), flags, indexes
    
#%% skipping stones
#move from left to right, by the value at the index to both left & right;
#return if there is a solution

import copy
def stones2(l):
    n = len(l)
    flags = [0]*n; flags[0]=1
    indexes = [0]
    if n==1:
        return True
    
    if l[0]==0:
        return False
    
    def scan_right(l, flags, indexes):
        flags_return = copy.deepcopy(flags)
        i = 1
        while i<n:
            j = 0
            while j<i:
                if (j+l[j]==i) & (flags[j]==1):
                    flags_return[i] = 1
                    if j not in indexes:
                        indexes.append(j)
                j+=1
            i+=1
        return flags_return, indexes
    
    def scan_left(l, flags, indexes):
        flags_return = copy.deepcopy(flags)
        i = 1
        while i<n:
            j = n-1
            while j>i:
                if (j-l[j]==i) & (flags[j]==1):
                    flags_return[i] = 1
                    if j not in indexes:
                        indexes.append(j)
                j-=1
            i+=1
        return flags_return, indexes
    
    flags_right, indexes = scan_right(l, flags, indexes)
    while (flags_right != flags) & (flags_right[n-1]==0):
        flags, indexes = scan_left(l, flags_right, indexes)
        flags_right, indexes = scan_right(l, flags, indexes)
        
    return bool(flags_right[-1]), flags_right, indexes
    
#%% return path of a directed graph structure

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
        
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
            
    return None


#%% return if there exist three integers that have a summation of a number
def sumThree(l, sumnum):
    n = len(l)
    
    i = 0
    while i<n:
        resi_i = sumnum - l[i]
        j=i+1
        while j<n:
            resi_j = resi_i - l[j]
            k = j+1
            while k<n:
                if l[k]==resi_j:
                    return True, i,j,k
                k+=1
            j+=1
        i+=1
    
    return False


#%% return if there exist a number of integers that have a summation of a number
def sumAny(l, sumnum, picknum):
    n = len(l)
    


