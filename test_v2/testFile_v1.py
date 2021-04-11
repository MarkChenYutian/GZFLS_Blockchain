import time
import json
import multiprocessing as mp

from Client.worker import Worker
from Client.taskDistributor import taskDistributor

from Utility.richConsole import console

if __name__ == "__main__":
    console.initialize()

    mainQueue = mp.Queue()
    workerQueue = mp.Queue()
    minerQueue = mp.Queue()

    distributorProcess = mp.Process(target=taskDistributor, args=(mainQueue, minerQueue, workerQueue))
    distributorProcess.start()

    workerProcess = mp.Process(target=Worker, args=(mainQueue, workerQueue))
    workerProcess.start()

    while True:
        newInstruction = input("Chain >")
        newInstruction = newInstruction.split(" ")
        try:
            newTask = {
                "to": newInstruction[0],
                "instruction": newInstruction[1],
                "args": newInstruction[2:]
            }
            mainQueue.put(json.dumps(newTask))
            if newTask["instruction"] == "stop" and newTask["to"] == "distributor":
                console.info("The Terminal Agent Terminated.")
                break
            time.sleep(1)
        except IndexError as e:
            console.error("Unable to parse the input instruction.\n{}".format(e))