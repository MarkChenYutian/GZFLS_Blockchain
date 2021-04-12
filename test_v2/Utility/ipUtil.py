"""
2021/04/12

ipUtil.py contains several utilty functions to get local host IP and all active IP with a FLASK GW Chain client on it.

By Xiaoxiao, Qingzi Shi, Mark
"""
import os
import re
import requests
import json
from socket import gethostname, gethostbyname


def getMyIP():
    return gethostbyname(gethostname())


def listAllIP():
    result = list()
    os.system('arp -a > ./Storage/ipList.txt')
    with open('./Storage/ipList.txt') as fp:
        for line in fp.read().strip().split("\n"):
            matchResult = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if matchResult is not None:
                result.append(matchResult.group(0))
    return result


def isRunningClient(targetIP):
    content = {'msg': 'checkAlive'}
    try:
        r = requests.post(url=targetIP + ":8080/connection", json=content, timeout=5)
        return json.loads(r.text)["msg"] == "GWChainProject"
    except requests.exceptions.InvalidSchema:
        return False


def getActiveIPs():
    allIP = listAllIP()
    return [ip for ip in allIP if isRunningClient(ip)]
