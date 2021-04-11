"""
This file define the worker process for client.
The worker will have several functions
    *   Create Transaction
    *   Verify Transaction
    *   Verify Block
    *   Maintain Ledger

By Mark, 2021/3/16
"""
import time
import json
import multiprocessing as mp

from Utility.richConsole import console
from Utility.exceptions import *
from Transaction.transactionFactory import TransactionFactory
from Block.blockchain import Blockchain
from Block.block import Block
from Ledger.ledger import Ledger
from Client.workerFn import *


def Worker(mainQueue: mp.Queue, taskQueue: mp.Queue):
    # Initialization
    console.info("Worker Process start. Initializing...")
    txFactory = TransactionFactory()
    ledger = Ledger(dataPath="Ledger.db")
    chain = Blockchain(dataPath="Blockchain.db")
    # Use some hack here to initialize block.
    currBlock = workerCreateBlock(newTask={"args": [5]}, chain=chain)

    # Runner Part
    while True:
        if taskQueue.qsize() > 0:
            newTask = taskQueue.get()
            console.info("Worker receive task: " + newTask)
            newTask = json.loads(newTask)

            if newTask["instruction"] == "stop":
                console.info("Worker receive a STOP instruction, terminated.")
                break

            elif newTask["instruction"] == "createCoinbaseTx":
                """
                Instruction:
                
                Chain >worker createCoinbaseTx 10.0
                
                Create a transaction from coinbase to oneself. Used to get money from COINBASE.
                """
                workerCreateCoinbaseTx(newTask, txFactory, mainQueue)

            elif newTask["instruction"] == "createTx":
                """
                Instruction:
                
                Chain >worker createTx 19.3 examplePublicKeyString
                Chain >worker createTx (1.5,3.4) ("examplePubKeyStr1","examplePubKeyStr2")
                
                Create a transaction object to transact to either one people or several peoples together. Note that the
                args are split by the space, so there must not have space between comma in tuple.
                
                Since we use eval() to parse tuple input, when you want to transact to multiple person, remember to add
                quotes before and after their pubKeys. (like the example above do)
                """
                workerCreateTx(newTask, txFactory, ledger, mainQueue)

            elif newTask["instruction"] == "visualize":
                """
                Instruction:
                
                Chain >worker visualize ledger
                Chain >worker visualize chain
                
                Call the visualization method for ledger / blockchain. The graphviz will draw an visualization image and 
                show in a pop out window.
                """
                try:
                    if newTask["args"][0] == "ledger":
                        ledger.visualize()
                    elif newTask["args"][0] == "chain":
                        chain.visualize()
                    else:
                        console.error("Invalid argument for instruction visualize.\n".format(json.dumps(newTask)))
                except Exception as e:
                    console.error("Failed to visualize. Exception detail showed below. {}".format(repr(e)))

            elif newTask["instruction"] == "createBlock":
                """
                This is an internal instruction, you SHOULD NOT call this method from terminal directly.
                
                If the current blockchain is empty, create an empty head block. Otherwise, create a tail block based on 
                the tail of current blockchain. 
                """
                currBlock = workerCreateBlock(newTask, chain)

            elif newTask["instruction"] == "addTx":
                """
                This is an internal instruction, you SHOULD NOT call this method from terminal directly.
                
                Add an transaction object into the current block.
                """
                if :


            else:
                console.error("Unrecognized Task {}".format(json.dumps(newTask)))
        else:
            time.sleep(0.1)
