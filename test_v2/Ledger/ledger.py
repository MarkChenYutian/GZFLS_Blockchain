"""
This File Describe a Ledger Object that is using shelve to store transactions in File System.

By Mark, 2021/02/13
"""
from typing import List

from Utility.shelveManager import ShelveManager
from Transaction.transaction import Transaction
from Utility.exceptions import TransactionNotExist
from Utility.richConsole import console

# Import Visualization Tools
CAN_VISUALIZE = False
try:
    from Visualize.visualizeTxChain import visualizeTransactionChain
    CAN_VISUALIZE = True
except ImportError:
    console.error("Failed to import Visualization Toolset. The visualization method(s) will not be available.")


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
        except KeyError:
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
        :param publicKey: The public key of the user.
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
            for outItem in self[TxID].outTransactions:
                pubKeys.add(outItem["pubKey"])
        for pubKey in pubKeys:
            balanceStat[pubKey] = self.getUserBalance(pubKey)[0]
        return balanceStat

    def visualize(self):
        if CAN_VISUALIZE:
            try:
                visualizeTransactionChain(self)
            except Exception as e:
                console.error("Failed to visualize Ledger object. No image output. Exception Detail: \n[red]{}[/red]".format(e))
        else:
            console.warning("Ledger.visualize() is called, but not executed since we can't import the visual tools.")

    def __str__(self):
        result = "Ledger Object\n----------"
        for txID in self.keys():
            result += str(self[txID]) + "\n----------\n"
        return result
