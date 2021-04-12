"""
2021/04/12

Web Receiver defines a FLASK server running on local host to receive message from other clients and add corresponding
tasks to the main Task Queue.

By Mark
"""
from flask import Flask, request
import multiprocessing as mp
import json
import logging
import traceback
import os

from Utility.richConsole import console


def webReceiver(mainTaskQueue):
    """
    Receiver of web agent. Receive message from web and put instruction into the task queue.

    :param mainTaskQueue: Multiprocessing Queue that store the tasks for all workers
    :return: None
    """
    # Disable Logging in Console
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app = Flask(__name__)
    # Define Detailed Functions

    @app.route("/connection", methods=["GET", "POST"])
    def respondClientTest():
        console.info("Connection Test from {} Received".format(request.remote_addr))
        return json.dumps({
            "msg": "GWChainProject",
            "data": []
        }), 200

    @app.route("/chain", methods=["GET"])
    def prepSendBlockchain():
        try:
            queryValue = request.args.get("q")
            requestIP = request.remote_addr
            if queryValue == "all":
                console.info("Client @ {} query for whole Blockchain.".format(request.remote_addr))
                newTask = {
                    "to": "worker",
                    "instruction": "getBlockChain",
                    "args": [requestIP]
                }
                mainTaskQueue.put(json.dumps(newTask))
            elif queryValue == "height":
                console.info("Client @ {} query for Blockchain height.".format(request.remote_addr))
                newTask = {
                    "to": "worker",
                    "instruction": "getBlockchainHeight",
                    "args": [requestIP]
                }
                mainTaskQueue.put(json.dumps(newTask))
            return json.dumps({
                "msg": "request received, send back through {}:8080/receive route with POST method.".format(requestIP),
                "data": []
            }), 200
        except Exception as e:
            console.error("Error raised when receiving {}'s GET on /chain. Detailed Exception is printed below."
                          "\n {}".format(request.remote_addr, repr(e)))
            return json.dumps({
                "msg": "Internal Server Error",
                "data": []
            }), 500

    @app.route("/transaction", methods=["POST"])
    def getTransactionFromWeb():
        strTransaction = request.form["msg"]
        newTask = {
            "to": "worker",
            "instruction": "addTx",
            "args": [strTransaction]
        }
        mainTaskQueue.put(json.dumps(newTask))
        return json.dumps({
            "msg": "received",
            "data": []
        }), 200

    @app.route("/debug", methods=["GET"])
    def debugFunction():
        taskList = []
        while mainQueue.qsize() > 0: taskList.append(mainQueue.get())
        return json.dumps(taskList, indent=4), 200
    app.run()


if __name__ == "__main__":
    mainQueue = mp.Queue()
    webReceiver(mainQueue)