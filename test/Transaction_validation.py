"""
This file contains several functions that are used to validate the Transaction Object
"""


def checkIsBalanced(newTransaction):
    """
    Check whether the inTransaction and outTransaction of a Transaction Object is valid. Return None if the Transaction
    is valid, otherwise, raise TransactionNotBalanceError()

    :param newTransaction: a transaction object that is checked
    :raise TransactionNotBalanceError: The amount of inTransaction and outTransaction does NOT balance out
    :return: None
    """
    pass


def checkOPScript(newTransaction,allTransactions):
    """
    Check whether the keys provided by Transactions are valid or not

    :param newTransaction: a transaction object that is checked
    :param allTransactions: a Ledger class that contains all the valid transactions recorded
    :return: None
    :raise TransactionOPError: The parameters in newTransaction can't make OP_Script run through without raising Exceptions
    """
    pass


def checkDoubleSpend(newTransaction,allTransactions):
    """
    Check whether the entries pointed by inTransaction is already used to prevent double spend.

    :param newTransaction: a transaction object that is checked
    :param allTransactions: a Ledger class that contains all the valid transactions recorded
    :return: None
    :raise TransactionDoubleSpendError: At least one entry that inTransaction points to is already used.
    """
    pass

def checkRecursively(newTransaction, allTransaction, currDepth=0, trustDepth=10):
    """
    Check the Transactions that form current transaction recursively

    :param newTransaction: a transaction object that is checked
    :param allTransactions: a Ledger class that contains all the valid transactions recorded
    :param currDepth: current recursion depth.
    :param trustDepth: transactions that is 10 blocks ago is accepted without condition. (This is used to prevent callstack overflow and improve performance)
    :return: None
    """
    pass