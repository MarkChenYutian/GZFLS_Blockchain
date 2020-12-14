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
        self.tx_time = int(time.time() * 1000)
        self.inTransaction = []
        self.outTransaction = []
    
    def __hash__(self):
        return hash(self.tx_time) * hash(self.inTransaction) * hash(self.outTransaction)

    def addInputTransaction(self, txn, index, Signature):
        self.inTransaction.append((txn, index, Signature))
    
    def addOutputTransaction(self, amount, reciverPubKey):
        self.outTransaction.append((amount, reciverPubKey, False))

def isCoinBase(transaction):
    pass

def checkIsBalance(currTransaction, allTransaction):
    outputAmount, inputAmount = 0, 0

    for index in range(len(currTransaction.inTransaction)):
        in_txn, in_index, signature = currTransaction.inTransaction[index]
        inputAmount += allTransaction[in_txn].outTransaction[in_index][0]
    
    for index in range(len(currTransaction.outTransaction)):
        outputAmount += currTransaction.outTransaction[index][0]
    
    return inputAmount == outputAmount

def checkInUnused(currTransaction, allTransaction):
    for index in range(len(currTransaction.inTransaction)):
        in_txn, in_index, signature = currTransaction.inTransaction[index]
        prev_tx = allTransaction[in_txn].outTransaction[in_index]
        if prev_tx[2]: return False # if any one of in_tx is already used before, the whole transaction is invalid
    return True

def checkInSig(currTransaction, allTransaction):
    for index in range(len(currTransaction.inTransaction)):
        in_txn, in_index, signature = currTransaction.inTransaction[index]
        prev_tx = allTransaction[in_txn]

        prev_pubKey = prev_tx.outTransaction[in_index][1]
        prev_sig = currTransaction.inTransaction[index][2]
        sig_result = decryptSignature(prev_sig, prev_pubKey)

        if sig_result != hash(prev_tx): return False
    return True

def getTxn(transaction):
    return hash(transaction)

def checkRecursiveTx(currTransaction, allTransaction):
    if isCoinBase(currTransaction): return True

    if not (checkInSig(currTransaction, allTransaction) and checkIsBalance(currTransaction, allTransaction)):
        return False

    isValid = True
    for index in range(len(currTransaction.inTransaction)):
        in_txn, in_index, signature = currTransaction.inTransaction[index]
        if in_txn not in allTransaction: return False   # Transaction not in ledger
        isValid = isValid and checkRecursiveTx(allTransaction[in_txn], allTransaction)
    return isValid

def checkTransaction(transaction, allTransaction):
    return checkRecursiveTx(transaction, allTransaction) and checkInUnused(transaction, allTransaction)


def decryptSignature(signature, pubKey):
    pass

