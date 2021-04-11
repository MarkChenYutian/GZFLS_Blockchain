"""
This file describe the Task Distributor of Task Queue
Task Distributor will get task from Task Queue and then distribute task into different queue for each process.
By Mark, 2021/3/16
"""
import json
import time
import multiprocessing as mp

from Utility.richConsole import console


def taskDistributor(mainQueue: mp.Queue, minerQueue: mp.Queue, workerQueue: mp.Queue) -> None:
    while True:
        if mainQueue.qsize() != 0:
            newTaskStr = mainQueue.get()
            newTask = json.loads(newTaskStr)
            target = newTask["to"]
            if target == "worker":
                workerQueue.put(newTaskStr)
            elif target == "miner":
                minerQueue.put(newTaskStr)
            elif target == "distributor":
                if newTask["instruction"] == "stop":
                    console.info("Distributor Receive STOP instruction. "
                                 "Delivering STOP instruction to other process.")
                    minerStopTask = {
                        "to": "miner",
                        "instruction": "stop",
                        "args": []
                    }
                    workerStopTask = {
                        "to": "worker",
                        "instruction": "stop",
                        "args": []
                    }
                    minerQueue.put(json.dumps(minerStopTask))
                    workerQueue.put(json.dumps(workerStopTask))
                    break
            else:
                console.error("Receive unrecognized task.\nDetails showed below:\n{}".format(newTask))
        else:
            time.sleep(0.1)
