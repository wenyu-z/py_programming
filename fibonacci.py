
def fibo(length, init_num=1):
    vector = [init_num]
    if length == 1:
        pass
    elif length == 2:
        vector.append(1)
    else:
        vector.append(1)
        i = 3
        while (i>2) & (i<length+1):
            vector.append(vector[-1]+vector[-2])
            i += 1
    return vector
