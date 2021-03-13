"""
This File Describe a Ledger Object that is using shelve to store transactions in File System.

By Mark, 2021/02/13
"""
import os
from typing import List, Tuple

from Utility.shelveManager import ShelveManager
from Transaction.transaction import Transaction
from Utility.exceptions import TransactionNotExist

# Import Visualization Tools
CAN_VISUALIZE = False
try:
    from Visualize.visualizeTxChain import visualizeTransactionChain
    CAN_VISUALIZE = True
except ImportError:
    print("Failed to import Visualization Toolset. The visualization method will not be available.")


class Ledger(ShelveManager):
    def __init__(self, dataPath):
        super(Ledger, self).__init__(dataPath)

    def __setitem__(self, key: str, item: Transaction):
        """
        Convert the transaction to string, and then store it in Ledger Shelve File.

        *** DO NOT USE THIS FUNCTION DIRECTLY ***

        :param key: Key of Dictionary stored by shelve. In Ledger class, usually be Transaction ID (uuid4)
        :param item: Transaction Object (which will be serialized to string and saved into Shelve)
        :return: None
        """
        assert isinstance(item, Transaction), "Ledger Object can only store Transaction Object as value"
        item_value = item.dumps()
        super().__setitem__(key, item_value)

    def __getitem__(self, key: str) -> Transaction:
        """
        Get the serialized result from Shelve File, and then convert it back to Transaction Object and return.

        :param key: Transaction ID
        :return: Transaction Object
        """
        try:
            item_value = super().__getitem__(key)
            return Transaction.loads(item_value)
        except:
            raise TransactionNotExist(key)

    def addNewTransaction(self, transactionObj: Transaction) -> None:
        """
        Add an new Transaction object into the ledger
        :return: None
        """
        self[transactionObj.id] = transactionObj

        # Set source Tx as used
        for inItem in transactionObj.inTransactions:
            txID, txIndex = inItem["inTransactionID"], inItem["inTransactionIndex"]
            sourceTx = self[txID]
            sourceTx.outTransactions[txIndex]["isUsed"] = True
            self[txID] = sourceTx

    def getUserBalance(self, publicKey: str) -> List[any]:
        """
        :param ScriptHash: the hash value of an user's OP Script.
        :return: [the available balance under that Script, [list of txID, index, and amount for available transactions]]
        """
        balance = 0.0
        myTransactions = []
        for TxID in self.keys():
            for index, outItem in enumerate(self[TxID].outTransactions):
                if not outItem["isUsed"] and outItem["pubKey"] == publicKey:
                    balance += outItem["amount"]
                    myTransactions.append((TxID, index, outItem["amount"]))
        return [balance, myTransactions]

    def getBalanceStat(self):
        pubKeys = set()
        balanceStat = dict()
        for TxID in self.keys():
            for outItem in self[TxID].outTransactions: pubKeys.add(outItem["pubKey"])
        for pubKey in pubKeys:
            balanceStat[pubKey] = self.getUserBalance(pubKey)[0]
        return balanceStat

    def visualize(self):
        if CAN_VISUALIZE: visualizeTransactionChain(self)
        else: print("Ledger.visualize() is called, but not executed since Import of Visualization Tools failed.")