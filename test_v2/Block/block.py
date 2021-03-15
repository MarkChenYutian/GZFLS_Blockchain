"""
This file contains the definition of Block Class.

By Mark, 2021/3/13
"""
import json
import datetime
from hashlib import sha3_256

from Transaction.transaction import Transaction
from Utility.exceptions import BlockNotFinishException, SerializationProcessException


class Block:
    def __init__(self, difficulty):
        """
        The base constructor for Block Object.
        *** YOU SHOULD NEVER USE THIS CONSTRUCTOR DIRECTLY ***
        """
        self.info = {
            "Creation Time": datetime.datetime.now().strftime("%c"),
            "Finish Time": None,
            "Block Status": False,
            "isLiteNode": False
        }
        self.difficulty = difficulty
        self.hashRoot = ""
        self.transactions = []
        self.transactionIDs = set()
        self.height = None
        self.prevHash = None
        self.nounce = None

    @classmethod
    def createTail(cls, prevBlock, difficulty=None):
        """
        The alternative constructor to construct a Block that has a previous block object.
        :param prevBlock: The previous block that current block will attach after
        :param difficulty: if set as None (default), then inherit difficulty from previous block.
        :return: The new Block created
        """
        if difficulty is None:
            diff = prevBlock.difficulty
        else:
            diff = difficulty
        self = cls(difficulty=diff)
        self.height = prevBlock.height + 1
        self.prevHash = prevBlock.hexHash()
        return self

    @classmethod
    def createHead(cls, difficulty):
        """
        The alternative constructor to construct a Block that has NO PREVIOUS BLOCK (the 0th block).
        :param difficulty: The difficulty of First block.
        :return: The Head Block
        """
        self = cls(difficulty)
        self.height = 0
        self.prevHash = "0ff"
        return self

    def addTransaction(self, transaction):
        """
        Add one Transaction Object to the Block that is constructing.
        :param transaction:
        :return: None
        """
        self.transactions.append(transaction)
        self.transactionIDs.add(transaction.id)

    def finishConstruction(self, miningFn):
        """
        Finish the construction of block, find out the nounce value using mining function.

        Note the result nounce value returned by miningFn will NOT BE CHECKED for CORRECTNESS. In other word, the returned
        nounce value from miningFn will be trusted without any condition.

        :param miningFn: A function of mining. will be called in the form of miningFn(blockObject) and return proper nounce value.
        :return: None
        """
        self.hashRoot = calculateRoot(self)
        self.info["Block Status"] = True
        self.nounce = miningFn(self)
        self.info["Finish Time"] = datetime.datetime.now().strftime("%c")

    def dumps(self) -> str:
        if not self.info["Block Status"]:
            raise BlockNotFinishException()
        blockDict = {
            "type": "Block",
            "blockInfo": self.info,
            "blockDifficulty": self.difficulty,
            "blockHeight": self.height,
            "blockNounce": self.nounce,
            "blockHashRoot": self.hashRoot,
            "blockPrevHash": self.prevHash,
            "blockTxs": [tx.dumps() for tx in self.transactions],
            "blockTxID": list(self.transactionIDs)
        }
        return json.dumps(blockDict)

    @classmethod
    def loads(cls, jsonString: str):
        self = cls(difficulty=0)
        infoDict = json.loads(jsonString)
        if infoDict["type"] != "Block":
            raise SerializationProcessException(jsonString)
        self.info = infoDict["blockInfo"]
        self.difficulty = infoDict["blockDifficulty"]
        self.height = infoDict["blockHeight"]
        self.nounce = infoDict["blockNounce"]
        self.hashRoot = infoDict["blockHashRoot"]
        self.prevHash = infoDict["blockPrevHash"]
        serializedTxs = infoDict["blockTxs"]
        self.transactions = [Transaction.loads(serializedTx) for serializedTx in serializedTxs]
        self.transactionIDs = set(infoDict["blockTxID"])
        return self

    def convertToLite(self):
        self.transactions = []  # Remove all the
        self.info["isLiteNode"] = True

    def hexHash(self):
        if not self.info["Block Status"]:
            raise BlockNotFinishException()

        return sha3_256((str(self.prevHash) + str(self.hashRoot) + str(self.nounce)).encode("ascii")).hexdigest()

    def __hash__(self):
        return int(self.hexHash(), 16)

    def __str__(self):
        return self.dumps()

    def __repr__(self):
        status = "Ready" if not self.info["Block Status"] else "Not Ready"
        return "<Block Object @ {}, with {} Transactions in it, status: {}>".format(id(self), len(self.transactions),
                                                                                    status)

    def __eq__(self, otherBlock):
        return self.prevHash == otherBlock.prevHash and self.nounce == otherBlock.nounce and self.hashRoot == otherBlock.hashRoot

    def __contains__(self, item: Transaction):
        return item.id in self.transactionIDs


def calculateRoot(blockObject: Block) -> str:
    """
    Given a block object, calculate the Hash Root for block
    :return: hashRoot
    """
    txList = blockObject.transactions
    msgList = [str(hash(tx)) for tx in txList]
    msg = "".join(msgList)
    return sha3_256(msg.encode("ascii")).hexdigest()
