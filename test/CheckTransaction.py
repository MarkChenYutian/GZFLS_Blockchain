"""
This File contains several methods to check the validity of Transactions.
"""
from util.Transaction_exceptions import *

def checkOPScript(transaction, ledger):
    """
    :param transaction: The transaction Object that is being checked
    :param ledger: ledger that store all the valid transactions
    :raise TransactionOPError(BlockchainError): The OP Script Fail to Execute / OP_RETURN is called when running OP Script
    :return: None
    """
    pass


def checkInTransactionExists(transaction, ledger):
    """
    :param transaction: The transaction Object that is being checked
    :param ledger: ledger that store all the valid transactions
    :raise TransactionInNotExist(BlockchainError): The transaction that .inTransaction is pointing at Does Not Exist.
    :return: None
    """
    pass


def checkTransactionBalance(transaction, ledger):
    """
    :param transaction: The transaction Object that is being checked
    :param ledger: ledger that store all the valid transactions
    :raise TransactionNotBalanceError(BlockchainError): Amount of money in .inTransaction does not equal to amount of money in .outTransaction
    :return: None
    """
    pass


def checkDoubleSpend(transaction, ledger):
    """
    :param transaction: The transaction Object that is being checked
    :param ledger: ledger that store all the valid transactions
    :raise TransactionDoubleSpendError(BlockchainError): Some of the inTransactions in transaction object is already used.
    :return: None
    """
    pass


def checkRecursively(transaction, ledger, remainDepth):
    """
    :param transaction: The transaction Object that is being checked
    :param ledger: ledger that store all the valid transactions
    :param remainDepth: The remaining depth of recursive to reach 'trust without condition depth'.
    :raise BlockChainError: Specifically, this function may raise TransactionNotBalanceError, TransactionOPError, TransactionInNotExist, and TransactionDoubleSpendError
    :return: None
    """
    pass