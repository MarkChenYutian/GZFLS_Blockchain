"""
This is a version of transaction written by mark
"""

from random import random
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
    def __init__(self, allTransaction, amount, myPubKey, myPrivateKey, myN, reciverPubKey, isCoinBase=False):
        self.isCoinBase = isCoinBase
        self.tx_time = int(time.time() * 1000)
        self.randID = int(random() * 10000)
        self.inTransaction = []
        self.outTransaction = []

        if isCoinBase:
            self.addOutputTransaction(amount, reciverPubKey)
            return

        myBalance = getMyTransaction(allTransaction, myPubKey)

        curr_in = 0
        for Txn, index in myBalance:
            curr_in += allTransaction[Txn].outTransaction[index][0]
            allTransaction[Txn].outTransaction[index][2] = True
            self.addInputTransaction(Txn, index, signSignature(allTransaction[Txn], myPrivateKey, myN))
            if curr_in == amount:
                self.addOutputTransaction(amount, reciverPubKey)
                break
            elif curr_in > amount:
                self.addOutputTransaction(amount, reciverPubKey)
                self.addOutputTransaction(curr_in - amount, myPubKey)
                break

        if curr_in < amount:
            raise Exception("We can't collect enough UTXO to create the Transaction you want to build, the Transaction is invalid and no Output is made.")
    
    def __hash__(self):
        return abs(hash(self.tx_time) + hash(tuple(self.inTransaction)) + self.randID)

    def addInputTransaction(self, txn, index, Signature):
        self.inTransaction.append((txn, index, Signature))
    
    def addOutputTransaction(self, amount, reciverPubKey):
        self.outTransaction.append([amount, reciverPubKey, False])
    
    def getTxn(self):
        return hash(self)
    
    def __str__(self):
        result = "============ Transaction ===============\n"\
        "| Txn: {} \n".format(self.getTxn())
        if self.isCoinBase:
            result += "| THIS TRANSACTION IS FROM COINBASE \n"
        else:
            result += "| In Transactions:\n"\
            "| Txn | Index | Signature |\n"
            for inTx in self.inTransaction:
                result += "| {} | {} | {}\n".format(inTx[0], inTx[1], inTx[2])
        result += "| Out Transactions:\n"\
            "| Amount | reciver PubKey | isUsed\n"
        for outTx in self.outTransaction:
            result += "| {} | {} | {}\n".format(outTx[0], outTx[1], outTx[2])
        result += "========================================"
        return result
    
    def __repr__(self):
        return str(self)


# Auxilary Function that used to create a transaction
def getMyTransaction(allTransaction, pubKey):
    MyTransactions = []
    for Txn in allTransaction:
        for index in range(len(allTransaction[Txn].outTransaction)):
            outTx = allTransaction[Txn].outTransaction[index]
            if outTx[1] == pubKey and (not outTx[2]): MyTransactions.append((Txn, index))
    return MyTransactions   # My Transaction is a list with structure (Txn, index)

def signSignature(transaction, privateKey, n):
    # TODO: write sign signature process here
    msg = hash(transaction)
    return msg ** privateKey % n

# Functions to check / validate a given transaction
def isCoinBase(transaction):
    # TODO: here, we need to write a function to identify whether a transaction is from COINBASE
    return transaction.isCoinBase

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
    # TODO: write signature decryption here
    pass

def calcBalance(allTransaction):
    balance = dict()

    for txn in allTransaction:
        for index in range(len(allTransaction[txn].outTransaction)):
            amount, pubkey, isUsed = allTransaction[txn].outTransaction[index]
            if not isUsed:
                if pubkey in balance: balance[pubkey] += amount
                else: balance[pubkey] = amount
    
    return balance
