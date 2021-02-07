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
import shelve
from Transaction_exceptions import *

class Ledger(dict):
    def __init__(self):
        super(Ledger, self).__init__()

    def addTransaction(self, newTransaction):
        """
        :param newTransaction: a Transaction object that wants to add into the Ledger
        :return: None
        :raise TransactionNotBalanceError - In and out transaction is not Balanced
        :raise TransactionDoubleSpendError - Some in transactions are already spent
        :raise TransactionInNotExist - In transaction not Exist in Ledger
        :raise TransactionOPError - In transaction failed to run OP_Script without exception.
        """
        pass
