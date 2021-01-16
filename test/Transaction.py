"""
Transaction Version 2
This File contains Transaction class with OP_Script and accept transaction to multiple person.

Transaction class in this version also contains the following structure:
-------------------------------------------------------------------------------------
|       inTransactions      |   outTransactions                      |  isCoinBase  |
|---------------------------+----------------------------------------+--------------|
| (Txn, index, parameters)  | (amount, isUsed, OP_Script, pubKeyHash)|              |
| (Txn, index, parameters)  | ...                                    |     False    |
|                           |                                        |              |
-------------------------------------------------------------------------------------

The 'signature' in previous version is replaced by a tuple of parameters.

Since the constructor of Transaction Object is complex, we will use the 'factory mode' here to create Transaction object
The TransactionFactory class will provide multiple ways to create Transaction object.
"""
import time
import random
import json
import hashlib

from Transaction_exceptions import *
from Ledger import *
from RSA.RSA_func import encryptString, decryptString

class TransactionFactory:
    def __init__(self, myPubKey: tuple, myPrivateKey: tuple, OP_Factory):
        # RSA_Features
        self.myPubKey = myPubKey
        self._myPrivateKey = myPrivateKey
        self.myPubKeyHash = hashlib.sha3_256(str(myPubKey).encode('ascii')).hexdigest()

        # OP_Script Factory
        self.OP_Factory = OP_Factory

    def createTransaction(self,
                          allTransactions: Ledger,
                          amount: tuple,
                          receiver_pubKeyHash: list,
                          isCoinBase=False,
                          **kwargs):
        """
        Create a Transaction using Parameters

        :param amount: tuple of integer that represent the amount of money transact to different people.
        :param isCoinBase: if the Transaction is from coinbase, set as True
        :param receiver_pubKeyHash: a list of public Key Hash that is used as parameters to create OP_Script
        :param kwargs: remained for future update

        :raise NotEnoughBalanceError(): There are not enough balance in the account to create the transaction

        :return: A Transaction Object
        """
        # Create a blank Transaction Object
        newTransaction = Transaction(isCoinBase=isCoinBase, **kwargs)
        """ Write Your Code Below """
        # TODO: Implement Transaction Initialization Here

        # get All My Transactions
        myTransactions = allTransactions.getMyTransactions(self.myPubKeyHash)
        # [(txn, index), (txn, index), ...]

        # if the Transaction is from coinbase, no inTransaction is needed
        if isCoinBase:
            for index in range(len(amount)):
                newOP_Script = self.OP_Factory.create('tx2pbh', receiver_pubKeyHash[index], newTransaction.getTxn())
                newTransaction.outTransactions.append((amount[index], False, newOP_Script, receiver_pubKeyHash[index], 'tx2pbh'))
                # tx2pbh stands for Transaction to Public Key Hash
            return newTransaction

        # get my balance
        totalOut = 0
        for txn, index in myTransactions:
            txDict = json.loads(allTransactions.get(txn))
            totalOut += txDict['outTransactions'][index][0]
            signature = encryptString(txn, *self.myPubKey)
            newTransaction.inTransactions.append((txn, index, (signature, self.myPubKey), 'tx2pbh'))
            if totalOut >= sum(amount):
                # out Transaction to everyone designated
                for index in range(len(amount)):
                    newOP_Script = self.OP_Factory.create('tx2pbh', receiver_pubKeyHash[index], newTransaction.getTxn())
                    newTransaction.outTransactions.append((amount[index], False, newOP_Script, receiver_pubKeyHash[index], 'tx2pbh'))
                if totalOut > sum(amount):
                    # give charge to transaction initiator
                    newOP_Script = self.OP_Factory.create('tx2pbh', self.myPubKeyHash[index], newTransaction.getTxn())
                    newTransaction.outTransactions.append((totalOut - sum(amount), False, newOP_Script, self.myPubKeyHash, 'tx2pbh'))

        if totalOut < sum(amount): raise NotEnoughBalanceError()   # Transaction Initiator does not have enough Balance

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
        return hashlib.sha3_256(str(self.timestamp * self.randNum).encode('ascii')).hexdigest()

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

    def __str__(self):
        str_result = "----------\n"
        str_result += "txn: {}\n".format(self.getTxn())
        str_result += "timestamp: {}\n".format(self.timestamp)
        str_result += "randID: {}\n".format(self.randNum)
        str_result += "inTransactions:\n"
        for _ in range(len(self.inTransactions)):
            str_result += str(self.inTransactions[_]) + "\n"
        str_result += "outTransactions:\n"
        for _ in range(len(self.outTransactions)):
            str_result += str(self.outTransactions[_][:2]) + " [OP_Script Omitted ...]" + "\n"
        str_result += "----------"
        return str_result

    def __repr__(self):
        return self.serialize()

if __name__ == "__main__":
    testLedger = Ledger()
    TransactionAgent = TransactionFactory((1109, 2003), (424, 2003))
    newTx = TransactionAgent.createTransaction(testLedger,tuple([10]),(),(),isCoinBase=True)
    testLedger.addTransaction(newTx)
    print(testLedger.items())
