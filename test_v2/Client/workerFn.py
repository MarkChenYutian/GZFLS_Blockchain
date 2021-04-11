import json
from Utility.richConsole import console
from Utility.exceptions import *
from Block.block import Block


def workerCreateCoinbaseTx(newTask, txFactory, mainQueue):
    try:
        args = newTask["args"]
        amount = float(args[0])
        newTx = txFactory.fromCoinBase(amount)

        minerTask = {
            "to": "miner",
            "instruction": "packBlock",
            "args": [newTx.dumps()]
        }
        mainQueue.put(json.dumps(minerTask))

    except BlockchainException as e:
        console.error("Blockchain Internal Exception is raised.\n{}".format(repr(e)))
    except Exception as e:
        console.error("Worker Failed to execute the instruction.\n{}".format(repr(e)))


def workerCreateTx(newTask, txFactory, ledger, mainQueue):
    try:
        args = newTask["args"]
        amount = eval(args[0])
        if isinstance(amount, tuple):
            pubKeys = eval(args[1])
            newTx = txFactory.transactToMult(pubKeys, amount, ledger)
        else:
            pubKey = args[1]
            newTx = txFactory.transactTo(pubKey, amount, ledger)

        minerTask = {
            "to": "miner",
            "instruction": "packBlock",
            "args": [newTx.dumps()]
        }
        mainQueue.put(json.dumps(minerTask))

    except BlockchainException as e:
        console.error(
            "Blockchain Internal exception. Failed to execute task\n{}\nException Detail\n{}".format(
                json.dumps(newTask), repr(e)))

    except Exception as e:
        console.error("Failed to execute. Exception Detail\n{}".format(repr(e)))


def workerCreateBlock(newTask, chain):
    try:
        if chain.numBlock == 0:
            difficulty = int(newTask["args"][0])
            newBlock = Block.createHead(difficulty)
            console.info("The blockchain is empty, so a header block will be created.")
        else:
            if len(newTask["args"]) > 0:
                difficulty = int(newTask["args"][0])
                newBlock = Block.createTail(chain.getTail(), difficulty=difficulty)
                console.info("A new block is created with difficulty update to {}".format(difficulty))
            else:
                newBlock = Block.createTail(chain.getTail())
                console.info("A new block is created on the tail")
        return newBlock

    except Exception as e:
        console.error("Failed to execute task\n{}\nDetailed Exception\n{}".format(json.dumps(newTask), repr(e)))

