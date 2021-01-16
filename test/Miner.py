"""
This file contains the Miner Process of Client.
The Miner will create block and calculate nounce value.
"""

import time
import hashlib


def minerProcess(minerQueue, taskQueue, registerFn):
    """
    :param minerQueue: A multiprocess Queue that give miner task
    :param taskQueue: taskQueue for whole Client so that miner process can send task to webAgent
    :param registerFn: a Function that will register a task in the taskQueue in specific form

    :return: None
    """
    while True:
        if minerQueue.qsize() > 0:
            taskDict = minerQueue.get()
            instruction = taskDict['instruction']
            parameter = taskDict['args']

            # poison pill for Miner Process
            if instruction == 'stop':
                break

            # Mining Process
            elif instruction == 'CREATE_BLOCK':
                print("get Parameters {}".format(taskDict['args']))
                print("Creating Block ...")
                try:
                    print(dummyMiner(parameter[0], 7))
                except IndexError:
                    print("\033[1;33mNot Enough Parameter Provided\033[0;;m")
                print("\033[1;32mBlock Created.\033[0;;m")
                registerFn(taskQueue, "webAgent", 'SEND_BLOCK', "testMsg")

            # Pass Instruction, used to call up Miner after restart miner process.
            elif instruction == 'PASS': continue

            # TODO: Add more actions of miner here.

            # Unrecognized Instruction
            else:
                print("\033[1;33mMiner get Unrecognized instruction {}\033[0;;m".format(taskDict))
        else:
            time.sleep(0.5)

    print("\033[1;31mMiner Exit.\033[0;;m\n")


def dummyMiner(info, difficulty):
    nounce = 0
    while True:
        hash = hashlib.sha3_256((str(info) + str(nounce)).encode('ascii')).hexdigest()
        if hash[:difficulty] == "0" * difficulty: break
        else: nounce += 1
    return hash
