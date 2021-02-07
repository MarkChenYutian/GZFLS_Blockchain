"""
This file contains the Worker Process for Client
The worker will create Transaction, Maintain Ledger, Manage Blockchain and check Transaction & Block
"""

import time


def workerProcess(workerTask, taskQueue, registerFn):
    """
    :param workerTask: multiprocessing Queue that store all the pending tasks for worker process
    :param taskQueue: multiprocessing Queue that store all the tasks so that worker can send task to Miner and webAgent
    :param registerFn: register a new Task in taskQueue in specific form
    :return: None
    """
    while True:
        if workerTask.qsize() > 0:
            newTask = workerTask.get()
            instruction = newTask['instruction']
            # poison pill for Worker Process
            if instruction == 'stop':
                break

            # Pass
            elif instruction == 'PASS':
                continue

            # Create a new Transaction
            elif instruction == 'CREATE_TX':
                print("get Instruction get Tx")

            # Unrecognized Instruction
            else:
                print("\033[1;33mWorker get Unrecognized instruction {}\033[0;;m".format(newTask))
        else:
            # If there is no pending task, suspend worker process for 0.5 sec to save resources
            time.sleep(0.5)
    print("\033[1;31mWorker Exit.\033[0;;m")