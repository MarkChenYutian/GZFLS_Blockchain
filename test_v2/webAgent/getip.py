import os
import platform
from socket import *

def get_my_ip():
    return gethostbyname(gethostname())
def get_ip():
    all_ip = []
    result = []
    os.system('arp -a > temp.txt')
    with open('temp.txt') as fp:
        for line in fp:
            line = line.split()[1:2]
            all_ip.append(line)
        for i in range(0, len(all_ip)):
            result.append(all_ip[i][0][1:len(all_ip[i][0]) - 1])
        return result
arr = get_ip()
print(arr)