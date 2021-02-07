"""
The Ledger class is inherited from the dictionary class.

Ledger class use module 'shelve' to store itself in file system. Everytime we use it, we should use
>> exampleLedger = Ledger()
>> exampleTransaction = TransactionFactory.createTransaction(...)
>> with exampleLedger as myLedger:
>>     myLedger.addTransaction(exampleTransaction) # Do Something
Ledger use the Txn of Transaction as key, and the value is Transaction object.
Everytime we add a transaction into the Ledger using 'addTransaction' method, the transaction should be checked.
If the Transaction is valid, add it into the ledger
If it is not, raise corresponding exceptions
"""
import json

from util.ShelveManager import ShelveManager
from util.Serialize import Serializable

class Ledger(Serializable):
    def __init__(self, storePath="./storage/Ledger.db", doClearInit=False):
        self.storePath = storePath
        self.shelveManager = ShelveManager(self.storePath)
        if doClearInit: self.clear(silent=True)

    def addTransaction(self, newTransaction):
        """
        :param newTransaction: a Transaction object that wants to add into the Ledger
        :return: None
        :raise TransactionNotBalanceError - In and out transaction is not Balanced
        :raise TransactionDoubleSpendError - Some in transactions are already spent
        :raise TransactionInNotExist - In transaction not Exist in Ledger
        :raise TransactionOPError - In transaction failed to run OP_Script without exception.
        """
        # TODO: Improve the implementation here to check the transaction
        self.set(newTransaction.getTxn(), newTransaction.serialize())

    def get(self,key):
        """
        :param key: key of dictionary
        :return: value that is paired with the key
        """
        return self.shelveManager.read(key)

    def set(self, key: str, item: str):
        """
        :param key: String, key of a pair in dictionary
        :param item: String, value of a pair in dictionary
        :return:
        """
        self.shelveManager.write(key,item)

    def getAllItems(self):
        """
        :return: A list of (key, item) in the Ledger
        """
        return self.shelveManager.getAll()

    def getMyTransactions(self, myPubKeyHash):
        """
        :param myPubKeyHash: SHA3_256 of My Public Key
        :return: A list of Transaction ID & Index. That represent usable UTXO.
        """
        myTransactions = []
        allPairs = self.getAllItems()
        for txn, item in allPairs:
            try:
                transaction_dict = json.loads(item)
                for _ in range(len(transaction_dict['outTransactions'])):
                    amount, isUsed, OP_Script, pubKeyHash, op_type = transaction_dict['outTransactions'][_]
                    if op_type == 'tx2pbh' and not isUsed and pubKeyHash == myPubKeyHash:
                        myTransactions.append((txn, _))
            except Exception as e:
                print("Warning: JSON can't load the object stored in Ledger. Ledger may be damaged")
                print(e)
        return myTransactions

    def serialize(self):
        """
        Implement Serialize Method in Serializable Abstract Class

        :return: JSON String of Ledger Object
        """
        ledgerDict = dict()
        ledgerDict['type'] = "Ledger"
        ledgerDict['data'] = self.getAllItems()
        return json.dumps(ledgerDict, indent=4)

    def load(self, serialize):
        """
        Implement load Method in Serializable Abstract Class

        Load serialize dictionary to create a new object.
        """
        assert serialize['type'] == "Ledger", "Ledger can only load from serialized string with Type Ledger"
        print("Original Ledger is cleared to load new Ledger.")
        self.clear(silent=False)
        for key, item in serialize['data']:
            self.set(key, item)

    def clear(self, silent=False):
        self.shelveManager.wipeData(silent=silent)

    def __str__(self):
        str_result = ""
        counter = 0
        for key, item in self.getAllItems():
            str_result += "\nTransaction #{}\n".format(counter)
            str_result += str(item)
            str_result += "\n"
            counter += 1
        return str_result
