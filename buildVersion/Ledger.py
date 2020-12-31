"""
Ledger class for GZFLS_Blockchain Project, store all the Transactions and validate each input Transaction automatically.
"""
from RSA_func import decryptObject
from Transaction_exceptions import *

class Ledger(dict):
    def __init__(self):
        super().__init__(self)
    
    def addTransaction(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether the input function is valid. If not, raise corresponding exceptions
        as described in part 1.3.1 of project requirement.
        """
        try:
            self.checkRecursiveTx(Transaction)
            self.checkIsUnused(Transaction)
            for Txn, index, signature in Transaction.inTransaction:
                self[Txn].outTransaction[index][2] = True
            super().update({hash(Transaction): Transaction})
        except Exception as e:
            raise e

                
    def checkIsBalance(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether the input transaction is balance on Input Amount and Output Amount. If
        the transaction is not balanced, raise TransactionNotBalanceError(). If it is balanced, return None
        """
        outputAmount, inputAmount = 0, 0

        for index in range(len(Transaction.inTransaction)):
            in_txn, in_index, signature = Transaction.inTransaction[index]
            try:
                inputAmount += self[in_txn].outTransaction[in_index][0]
            except KeyError:
                raise TransactionInNotExist()

        for index in range(len(Transaction.outTransaction)):
            outputAmount += Transaction.outTransaction[index][0]

        if inputAmount != outputAmount: raise TranactionNotBalanceError()
        return
    
    def checkIsUnused(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether each entry that .inTransaction points to is unUsed. If any of
        the entry is already used, raise TransactionDoubleSpendError.
        """
        for index in range(len(Transaction.inTransaction)):
            in_txn, in_index, signature = Transaction.inTransaction[index]
            prev_tx = self[in_txn].outTransaction[in_index]
            if prev_tx[2]: raise TransactionDoubleSpendError() # if any one of in_tx is already used before, the whole transaction is invalid
    
    def checkRecursiveTx(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None
        """
        if isCoinBase(Transaction): return True

        self.checkIsBalance(Transaction)
        self.checkInSig(Transaction)
        isValid = True
        for index in range(len(Transaction.inTransaction)):
            in_txn,in_index,signature = Transaction.inTransaction [index]
            if in_txn not in self: raise TransactionInNotExist()  # Transaction not in ledger
            isValid = isValid and self.checkRecursiveTx(self[in_txn])
        return isValid
    
    def getBalanceStat(self):
        balance = dict()

        for txn in self.keys():
            for index in range(len(self[txn].outTransaction)):
                amount, pubkey, isUsed = self[txn].outTransaction[index]
                if pubkey not in balance: balance[pubkey] = 0
                if not isUsed: balance[pubkey] += amount

        return balance
    
    def checkInSig(self, currTransaction):
        for index in range(len(currTransaction.inTransaction)):
            in_txn, in_index, signature = currTransaction.inTransaction[index]
            prev_tx = self[in_txn]

            prev_pubKey = prev_tx.outTransaction[in_index][1]
            prev_sig = currTransaction.inTransaction[index][2]
            try:
                sig_result = decryptSignature(prev_sig, prev_pubKey)
            except:
                raise TransactionSignatureError()

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

def decryptSignature(signature, pubKey: tuple):
    return decryptObject(signature, pubKey[0], pubKey[1])

if __name__ == "__main__":
    A = Ledger()
    