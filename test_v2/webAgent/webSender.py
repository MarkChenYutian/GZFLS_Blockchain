"""
2021/04/12

This file describe a function that take over all the output to web.

By Mark
"""
from Utility.ipUtil import getMyIP, getActiveIPs
from Utility.richConsole import console
import requests
import json


def webSender(webQueue) -> None:
    """
    webSender is a function that controls all the output on internet by GW Chain Project. It receives task from
    webQueue, a multiprocessing queue.

    :param webQueue: A multiprocessing queue that contains JSON tasks.
    :return: None
    """
    activeIP = getActiveIPs()


def broadcast(msg, data, route, activeIPs, method="GET"):
    for ip in activeIPs:
        if method == "GET":
            res = requests.get("http://" + ip + ":8888" + route, timeout=5)
        elif method == "POST":
            data = {"msg": msg, "data": data}
            res = requests.post("http://" + ip + ":8888" + route, json=data, timeout=5)
        else:
            raise AssertionError("Method expect to be POST or GET, get {}".format(method))
        if res.status_code != 200:
            console.info("Failed to connect with remote host {}:8888{}".format(ip, route))


def sendTransaction(txString, activeIP):
    broadcast("new tx", [txString], "/transaction", activeIP, method="POST")


def sendBlock(blockString, activeIP):
    broadcast("new block", [blockString], "/block", activeIP, method="POST")


def sendBlockchain(blockchainString, activeIP):
    broadcast("full chain", [blockchainString], "/chain", activeIP, method="POST")


if __name__ == "__main__":
    broadcast("", "/connection", ['127.0.0.1'], method="POST")
