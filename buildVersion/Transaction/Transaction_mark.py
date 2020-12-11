"""
This is a version of transaction written by mark
"""

import time

"""
One Transaction Object
|   inTx         |   inSig   |   outTx   |   reciverPubKey   |  isUsed  |
|  [txn1, index] | SHA256-...|  10 BTC   |     12387908      |  False   |
|  [txn2, index] | SHA256-...|   5 BTC   |     23456789      |   True   |
...

allTransaction is a dictionary, key [Transaction Number (txn)] -> value [Transaction object]
"""

class Transaction:
    def __init__(self):
        self.inTransaction = []
        self.outTransaction = []

    def addInputTransaction(self, txn, index, Signature):
        self.inTransaction.append((txn, index, Signature))
    
    def addOutputTransaction(self, amount, reciverPubKey):
        self.outTransaction.append((amount, reciverPubKey, False))
    
    def checkIsBalance(self, allTransaction):
        outputAmount, inputAmount = 0, 0

        for index in range(len(self.inTransaction)):
            in_txn, in_index, signature = self.inTransaction[index]
            inputAmount += allTransaction[in_txn].outTransaction[in_index][0]
        
        for index in range(len(self.outTransaction)):
            outputAmount += self.outTransaction[index][0]
        
        return inputAmount == outputAmount
    
    def checkInUnused(self, allTransaction):
        for index in range(len(self.inTransaction)):
            in_txn, in_index, signature = self.inTransaction[index]
            prev_tx = allTransaction[in_txn].outTransaction[in_index]
            if prev_tx[2]: return False # if any one of in_tx is already used before, the whole transaction is invalid
        return True
    
    def checkInSig(self, allTransaction):
        for index in range(len(self.inTransaction)):
            in_txn, in_index = self.inTransaction[index]
            prev_tx = allTransaction[in_txn]

            prev_pubKey = prev_tx.outTransaction[in_index][1]
            prev_sig = self.inTransaction[index][]

