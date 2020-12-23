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
        """WRITE YOUR CODE BELOW"""
        pass

                
    def checkIsBalance(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether the input transaction is balance on Input Amount and Output Amount. If
        the transaction is not balanced, raise TransactionNotBalanceError(). If it is balanced, return None
        """
        """ WRITE YOUR CODE BELOW """
        pass

    
    def checkIsUnused(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you should check whether each entry that .inTransaction points to is unUsed. If any of
        the entry is already used, raise TransactionDoubleSpendError.
        """
        """ WRITE YOUR CODE BELOW """
        pass
    
    def checkRecursiveTx(self, Transaction):
        """
        :param: Transaction - a transaction object that needs to be added into the Ledger
        :return: None

        In this function, you will check the transaction and their upperstream transactions recursively until you meet
        the transaction from COINBASE. Any transaction from COINBASE is directly considered as valid transaction. If the
        transaction is valid after checking recursively, raise corresponding Exceptions, otherwise, return nothing.
        """
        """ WRITE YOUR CODE BELOW """
        pass
    
    def getBalanceStat(self):
        """
        :param: Nothing
        :return: A dictionary that represent the total usable (unused) coins in the ledger. The key is the public key of
        receiver while the value is balance (amount of money) under each public key.
        """
        """ WRITE YOUR CODE BELOW """
        pass
    
    def checkInSig(self, currTransaction):
        for index in range(len(currTransaction.inTransaction)):
            in_txn, in_index, signature = currTransaction.inTransaction[index]
            prev_tx = self[in_txn]

            prev_pubKey = prev_tx.outTransaction[in_index][1]
            prev_sig = currTransaction.inTransaction[index][2]
            sig_result = decryptSignature(prev_sig, prev_pubKey)

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
    