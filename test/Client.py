"""
This File defines the Client class, which is the fundamental class for all the actions taken.

A client class will contain the offline parts of Blockchain Project
"""
import multiprocessing
import json
import time
import datetime

from RSA.RSA_func import generateMyKeys, encryptString, decryptString
from Transaction import TransactionFactory
from OP_Script.OP_Factory import OP_Factory

from Miner import minerProcess
from Worker import workerProcess


def taskDistributeAgent(taskQueue, minerQueue, workerQueue, webAgentQueue, registerFn):
    """
    Get task from taskQueue and distribute it to the minerQueue and workerQueue in Client Object.

    :param taskQueue: A multiprocessing Queue that receive tasks from main process (stdin) and webAgent process
    :param minerQueue: A multiprocessing Queue that store the to-do for miner process
    :param workerQueue: A multiprocessing Queue that store the to-do for worker process
    :param registerFn: register Task Function for Environment
    :return: None
    """
    while True:
        if taskQueue.qsize() > 0:
            newTask = taskQueue.get()
            taskDict = json.loads(newTask)
            destination = taskDict['to']
            # distribute miner work to MinerTask Queue
            if destination.lower() == "miner":
                print("task distribute to Miner")
                minerQueue.put(taskDict)
            # distribute worker work to WorkerTask Queue
            elif destination.lower() == "worker":
                print("task distribute to Worker")
                workerQueue.put(taskDict)
            # distribute webAgent work to webAgentTask Queue
            elif destination.lower() == "webagent":
                print("task distribute to webAgent")
                webAgentQueue.put(taskDict)
            # 'poison pill' for distributor
            elif destination.lower() == "distributor":
                if taskDict['instruction'] == 'stop':
                    registerFn(taskQueue, 'miner', 'stop')  # stop miner Process
                    registerFn(taskQueue, 'worker', 'stop') # stop worker Process
                    registerFn(taskQueue, 'distributor', 'final_stop')  # stop distributor Process finally
                    print("\033[1;31mDistributor Stopping Workers ...\033[0;;m")
                elif taskDict['instruction'] == 'final_stop':
                    print("\033[1;31mTask Distributor Exit.\033[0;;m")
                    break
            # can't distribute unrecognized task
            else:
                print("\033[1;33mUnrecognized Instruction {}, Failed to Distribute.\033[0;;m".format(newTask))

        else:
            # If the task queue is empty, sleep for 0.5 sec to lower resource usage
            time.sleep(0.5)


def taskRegister(taskQueue, target, instruction, *args, **kwargs):
    """
    Register a task in the task queue of Client object. This method will be wrapped into a dictionary in the form of
    task and register into the taskQueue after serialized by JSON.

    :param taskQueue: A multiprocess Queue.
    :param target: A string, either 'worker' or 'miner'
    :param instruction: Instruction to worker / miner to call corresponding functions
    :param args: parameters for the instructions **(Parameters should be serialized)**
    :param kwargs: positional parameters for instructions **(Parameters should be serialized)**

    :return: True if the task is register successfully, False otherwise.
    """
    task = dict()
    if target.lower() not in {"miner", "worker", "distributor", "webagent"}:
        print("\033[1;33mTask destination must be Miner, Worker, webAgent, or Distributor, Register Fail.\nTarget Detail: {}\033[0;;m".format(target))
        return False
    task['to'] = target.lower()
    task['instruction'] = instruction
    task['args'] = list(args)
    task['kwargs'] = kwargs
    try:
        task = json.dumps(task)     # This line may raise TypeError as parameters may not be serialized.
        taskQueue.put(task)
        print("Task Registered as {}".format(task))
        return True
    except TypeError as e:
        print("\033[1;33mYou may forget to serialize the parameters befor you register a task, Register Fail\033[0;;m")
        return False


class Client:
    def __init__(self):
        """
        A client contains a Task List (a multiprocess queue), the distributor in client will check the queue all the time.
        If the task list is not Empty, the distributor will distribute the task to specific worker's own to-do list in
        Client and pop the task out of Queue.

        Adding Task into the client should use self.register_Task function

        Miner and worker will take the tasks from their own to-do list (MinerQueue & WorkerQueue)

        The client's task will come from two agents - webAgent and terminalAgent. The webAgent will register a task when
         receiving specific data. (e.g. when receiving a block, add task of check Block)

        The terminal agent can decide two things
            * start / stop mining process
            * create Transaction to another client

        WebAgent and TerminalAgent are in different process, so they will not clog each other's work.
        """
        print("GZFLS Blockchian Client Start @ {}".format(datetime.datetime.now()))
        print("Initializing Client")

        # Core Property of Client Class - Task Queue
        self.taskQueue = multiprocessing.Queue()
        self.minerQueue = multiprocessing.Queue()
        self.workerQueue = multiprocessing.Queue()
        self.webAgentQueue = multiprocessing.Queue()
        # Task Distributor will get task from task queue and call appropriate objects in Client.
        self.taskDistributor = multiprocessing.Process(target=taskDistributeAgent,
                                                       args=(self.taskQueue,
                                                             self.minerQueue,
                                                             self.workerQueue,
                                                             self.webAgentQueue,
                                                             taskRegister))
        self.miner = None
        self.worker = None

        # RSA Keys of Client
        privateKey, publicKey, rsa_n = generateMyKeys()
        self._privateKey = (privateKey, rsa_n)
        self.publicKey = (publicKey, rsa_n)

        # Factories and Helper Agents in Client
        # Transaction Factory create Transaction Object from various ways
        myOPFactory = OP_Factory()
        self.TxFactory = TransactionFactory(self.publicKey, self._privateKey, myOPFactory)
        # TODO: we may need a BlockFactory / LedgerManager here.

        # start distributor process
        print("Task Distribution Process Start")
        self.taskDistributor.start()

        # start miner process
        try:
            self.startMiner()
            print("Miner Process Start")
        except:
            print("Miner Start Fail")

        # start worker process
        try:
            self.startWorker()
            print("Worker Process Start")
        except:
            print("Worker Start Fail")

        # Handle Terminal
        print("Terminal Agent Start\n--------------------")
        self.terminalAgent()



    def startMiner(self):
        if self.miner is None or not self.miner.is_alive():
            self.miner = multiprocessing.Process(target=minerProcess,args=(self.minerQueue,self.taskQueue,taskRegister))
            self.miner.start()
        else:
            print("\033[1;33mMiner already start.\033[0;;m")

    def startWorker(self):
        if self.worker is None or not self.worker.is_alive():
            self.worker = multiprocessing.Process(target=workerProcess, args=(self.workerQueue, self.taskQueue, taskRegister))
            self.worker.start()
        else:
            print("\033[1;33mWorker already start.\033[0;;m")

    def statProcess(self, printOut=False):
        status = dict()
        status ['miner'] = []
        status ['worker'] = []
        status ['distributor'] = []
        # Miner Status
        status['miner'].append(self.miner is not None and self.miner.is_alive())
        status['miner'].append(self.minerQueue.qsize())
        # Worker Status
        status['worker'].append(self.worker is not None and self.worker.is_alive())
        status['worker'].append(self.workerQueue.qsize())
        # Distributor Status
        status['distributor'].append(self.taskDistributor is not None and self.taskDistributor.is_alive())
        status['distributor'].append(self.taskQueue.qsize())

        if printOut:
            # Distributor Status
            print("Process 0: Distributor",end="")
            if status ['distributor'] [0]:
                print(" \033[1;32m[  OK  ]\033[0;;m" + "  Task Queue |" + "*" * status ['distributor'] [1])
            else:
                print(" \033[1;31m[ DEAD ]\033[0;;m" + "  Task Queue |" + "*" * status ['distributor'] [1])

            # Worker Status
            print("Process 1: Worker     ",end="")
            if status ['worker'] [0]:
                print(" \033[1;32m[  OK  ]\033[0;;m" + "  Task Queue |" + "*" * status ['worker'] [1])
            else:
                print(" \033[1;31m[ DEAD ]\033[0;;m" + "  Task Queue |" + "*" * status ['worker'] [1])

            # Miner Status
            print("Process 2: Miner      ",end="")
            if status ['miner'] [0]:
                print(" \033[1;32m[  OK  ]\033[0;;m" + "  Task Queue |" + "*" * status ['miner'] [1])
            else:
                print(" \033[1;31m[ DEAD ]\033[0;;m" + "  Task Queue |" + "*" * status ['miner'] [1])

        return status

    def terminalAgent(self):
        # Handel the stdin below
        while True:
            terminalTask = input().split(" ")

            # Emergency Stop
            if terminalTask [0] == "STOP":
                print("\033[1;31mClient Stop Forcely. Terminating worker process.\033[0;;m")
                self.taskDistributor.terminate()
                self.miner.terminate()
                break

            # print client status
            if terminalTask [0] == "stat":
                self.statProcess(printOut=True)
                continue


            # Start Miner
            if terminalTask [1] == 'start':
                if terminalTask [0] == 'miner':
                    self.startMiner()
                elif terminalTask [0] == 'worker':
                    self.startWorker()
                continue

            try:
                # Parse terminal task
                taskStat = taskRegister(self.taskQueue,terminalTask [0],terminalTask [1],*terminalTask [2:])

                # Normal Stop
                if terminalTask [1] == 'stop' and terminalTask [0].lower() == 'distributor':
                    break

                # Register Fail
                elif not taskStat:
                    print("\033[1;33mTask Register Fail\033[0;;m")

            except IndexError:
                print("\033[1;33mTask Register Fail, at least two parameters makes up a valid task\033[0;;m")

        print("\033[1;31mTerminal Agent Exit.\033[0;;m")


if __name__ == "__main__":
    testClient = Client()
