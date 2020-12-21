"""
Ledger class for GZFLS_Blockchain Project, store all the Transactions and validate each input Transaction automatically.
"""
from RSA_func import decryptObject
import warnings

class Ledger(dict):
    def __init__(self):
        super().__init__()
    
    def addTransaction(self, Transaction):
        try:
            self.checkRecursiveTx(Transaction)
            self.checkInSig(Transaction)
            for Txn, index, signature in Transaction.inTransaction:
                self[Txn].outTransaction[index][2] = True
            super().update({hash(Transaction): Transaction})
        except Exception as e:
            raise e
                
    def checkIsBalance(self, Transaction):
        outputAmount, inputAmount = 0, 0

        for index in range(len(Transaction.inTransaction)):
            in_txn, in_index, signature = Transaction.inTransaction[index]
            inputAmount += self[in_txn].outTransaction[in_index][0]
        
        for index in range(len(Transaction.outTransaction)):
            outputAmount += Transaction.outTransaction[index][0]
        
        if inputAmount != outputAmount: raise TranactionNotBalanceError()
        return
    
    def checkIsUnused(self, Transaction):
        for index in range(len(Transaction.inTransaction)):
            in_txn, in_index, signature = Transaction.inTransaction[index]
            prev_tx = self[in_txn].outTransaction[in_index]
            if prev_tx[2]: return False # if any one of in_tx is already used before, the whole transaction is invalid
        return True
    
    def checkRecursiveTx(self, Transaction):
        if isCoinBase(Transaction): return True

        self.checkIsBalance(Transaction)
        self.checkInSig(Transaction)
        isValid = True
        for index in range(len(Transaction.inTransaction)):
            in_txn, in_index, signature = Transaction.inTransaction[index]
            if in_txn not in self: raise TransactionInNotExist()   # Transaction not in ledger
            isValid = isValid and self.checkRecursiveTx(self[in_txn])
        return isValid
    
    def getBalanceStat(self):
        balance = dict()

        for txn in self.keys():
            for index in range(len(self[txn].outTransaction)):
                amount, pubkey, isUsed = self[txn].outTransaction[index]
                if not isUsed:
                    if pubkey in balance: balance[pubkey] += amount
                    else: balance[pubkey] = amount
        
        return balance
    
    def checkInSig(self, currTransaction):
        for index in range(len(currTransaction.inTransaction)):
            in_txn, in_index, signature = currTransaction.inTransaction[index]
            prev_tx = self[in_txn]

            prev_pubKey = prev_tx.outTransaction[in_index][1]
            prev_sig = currTransaction.inTransaction[index][2]
            sig_result = decryptSignature(prev_sig, prev_pubKey, currTransaction.myN)

            if sig_result != hash(prev_tx): raise TransactionSignatureError()
        return True
    
    def __str__(self):
        result ="| Status | Current Number of Transaction Stored: {}\n".format(len(self))
        result +="------------ Transactions Stored in Ledger Below ----------\n"
        result +="| Ledger Balence Statistics: " + str(self.getBalanceStat()) + "\n"
        for Txn in self.keys():
            result += str(self[Txn])
            result += "\n|\n"
        result +="------------ Transactions Stored in Ledger Above ----------\n"
        return result
        
    def __repr__(self):
        return str(self)
    
    def exportFile(self, fileName="Ledger.txt"):
        with open(fileName, "w") as exportFile:
            exportFile.write(str(self))

def isCoinBase(transaction):
    return transaction.isCoinBase

def decryptSignature(signature, pubKey, n):
    return decryptObject(signature, pubKey, n)

################################ You Needn't Read the Stuffs Below #################################
class TranactionNotBalanceError(Exception):
    def __init__(self, message="The Transaction is not Balanced, check the init function in Transaction Class."):
        self.message = message
        super().__init__(self.message)

class TransactionDoubleSpendError(Exception):
    def __init__(self, message="At least one of the input in given transaction is already used, transaction is not recorded by Ledger."):
        self.message = message
        super().__init__(self.message)

class TransactionInNotExist(Exception):
    def __init__(self, message="At least one of the input of given Transaction is not recorded in the Ledger, transaction is not recorded by Ledger."):
        self.message = message
        super().__init__(self.message)

class TransactionSignatureError(Exception):
    def __init__(self, message="Signature in the given inTransaction fail to Pass the Signature Pass."):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    A = Ledger()
    