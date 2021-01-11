"""
Transaction Version 2
This File contains Transaction class with OP_Script and accept transaction to multiple person.

Transaction class in this version also contains the following structure:
-------------------------------------------------------------------------
|       inTransactions      |   outTransactions          |  isCoinBase  |
|---------------------------+----------------------------+--------------|
| (Txn, index, parameters)  | (amount, isUsed, OP_Script)|              |
| (Txn, index, parameters)  | ...                        |     False    |
|                           |                            |              |
-------------------------------------------------------------------------

The 'signature' in previous version is replaced by a tuple of parameters.

Since the constructor of Transaction Object is complex, we will use the 'factory mode' here to create Transaction object
The TransactionFactory class will provide multiple ways to create Transaction object.
"""
import time
import random
import json

from Transaction_exceptions import *
from Ledger import *

class TransactionFactory:
    def __init__(self, myPubKey: tuple, myPrivateKey: tuple):
        self.myPubKey = myPubKey
        self.myPrivateKey = myPrivateKey

    def createTransaction(self,
                          allTransactions: Ledger,
                          amount: tuple,
                          OPType: tuple,
                          OP_Parameters: tuple,
                          isCoinBase=False,
                          **kwargs):
        """
        Create a Transaction using Parameters

        :param amount: tuple of integer that represent the amount of money transact to different people.
        :param OPType: tuple of string that is either "2PubKey" or "2PubKeyHash"
        :param OP_Parameters: tuple of parameters given to setup the OP Script
        :param isCoinBase: if the Transaction is from coinbase, set as True
        :param kwargs: remained for future update

        :raise NotEnoughBalanceError(): There are not enough balance in the account to create the transaction

        :return: A Transaction Object
        """
        newTransaction = Transaction(isCoinBase=isCoinBase, **kwargs)
        """ Write Your Code Below """
        # TODO: Implement Transaction Initialization Here

        return newTransaction   # Do Not modify this line

    def loadSerializedTransaction(self, serializedDict: dict):
        """
        Create a Transaction using serialized result (a dictionary).

        :param a dictionary from Transaction.serialize()
        :return a new Transaction Object
        """
        newTransaction = Transaction(isCoinBase=False)
        newTransaction.load(serializedDict)
        return newTransaction


class Transaction:
    def __init__(self, isCoinBase=False, **kwargs):
        """
        :param isCoinBase: if the Transaction is from coinbase, set as True
        :param **kwargs: remained for future update

        :return None
        """
        # Properties used to Create Txn, Do NOT modify these two lines
        self.timestamp = int(time.time() * 1e4)
        self.randNum = int(random.random() * 1e4)

        # Basic Property
        self.version = 2
        self.isCoinBase = isCoinBase

        # Core Property
        self.kwargs = kwargs
        self.inTransactions = []
        self.outTransactions = []

    def getTxn(self):
        """
        Do Not Modify this Method
        This Method creates a unique ID (UID) for each Transaction Object.
        :return: an integer that represent the Transaction Number of current Transaction Object
        """
        return int(str(self.timestamp) + str(self.randNum))

    def serialize(self):
        """
        Do Not Modify this Method
        This method 'serialize' a Transaction Object into a string. In this way, we can calculate the hash and
        deliver it on the internet.
        :return: a string that contains vital information of Transaction Object.
        """
        result = dict()
        result['type'] = "Transaction"
        result['timestamp'] = self.timestamp
        result['randNum'] = self.randNum
        result['version'] = self.version
        result['isCoinBase'] = self.isCoinBase
        result['kwargs'] = self.kwargs
        result['inTransactions'] = self.inTransactions
        result['outTransactions'] = self.outTransactions
        return json.dumps(result)

    def load(self, serialized_Res: dict):
        """
        Do Not Modify this Method
        This method 'load' a dictionary that contains all the properties of transaction object to the current object.
        :param serialized_Res: a dictionary that comes from self.serialized()'s decoding result
        :return: None
        :raises: AssertionError
        """
        assert serialized_Res['type'] == "Transaction", \
            "Transaction object can only load from the serialized result of Transaction"
        self.timestamp = serialized_Res['timestamp']
        self.randNum = serialized_Res['randNum']
        self.version = serialized_Res['version']
        self.isCoinBase = serialized_Res['isCoinBase']
        self.kwargs = serialized_Res['kwargs']
        self.inTransactions = serialized_Res['inTransactions']
        self.outTransactions = serialized_Res['outTransactions']

if __name__ == "__main__":
    testLedger = Ledger()
    TransactionAgent = TransactionFactory((1109, 2003), (424, 2003))
    newTx = TransactionAgent.createTransaction(testLedger, tuple([10]), (), (), isCoinBase=True)
    testLedger.addTransaction(newTx)
    print(testLedger.items())
