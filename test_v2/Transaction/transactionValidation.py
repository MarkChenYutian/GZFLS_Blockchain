"""
This File define several functions to check the given transaction.
Fn(Transaction: Transaction, Ledger: Ledger) -> None
Fn(Transaction: Transaction) -> None

If the transaction is invalid, corresponding Exception will be raised.

By Mark, 2021/02/13
"""
from Utility.exceptions import NotBalanceTransactionException, SignatureVerifyFailException
from Transaction.transaction import Transaction
from Ledger.ledger import Ledger
from RSA.RSA_util import verifySignature, loadKeyFromString


def isTransactionBalance(transaction: Transaction, ledger: Ledger) -> None:
    """
    Check whether the input and output of transaction is balance.
    :param transaction: The transaction object to be checked.
    :param ledger: The ledger that store all the valid transactions.
    :return: None

    FIXME: Currently, there is one way to hack the system by using not precise float comparison.
    For instance, suppose one deliberately let inTransaction = 1.0 and outTransaction to be 1.00000005, since we are using
    INACCURATE float comparison here, this Transaction will be considered as "Valid", and an 5 * 1e-7 coin will be
    created from nowhere.

    It is possible to solve this problem by
      1. restrict to transact only integer amount of coins
      2. use Python Decimal module to allow Accurate Float Comparison
    """
    inAmount, outAmount = 0.0, 0.0
    for inItem in transaction.inTransactions:
        inTransaction = ledger[inItem["inTransactionID"]]
        inAmount += inTransaction.outTransactions[inItem["inTransactionIndex"]]["amount"]
    for outItem in transaction.outTransactions:
        outAmount += outItem["amount"]
    if inAmount == outAmount:
        raise NotBalanceTransactionException(inAmount, outAmount)


def isTransactionSigValid(transaction: Transaction, ledger: Ledger) -> None:
    """
    Check whether all the signatures in given transaction is valid.
    :param transaction: the transaction object to be checked.
    :param ledger: The ledger to store all the valid transactions.
    :return: None
    """
    for inItem in transaction.inTransactions:
        inTxID, inTxIndex, inTxSig = inItem["inTransactionID"], inItem["inTransactionIndex"], inItem["inTransactionSig"]
        inTxPubKeyString = ledger[inTxID].outTransactions[inTxIndex]["pubKey"]
        inTxPubKey = loadKeyFromString(inTxPubKeyString)
        if not verifySignature(rsaKey=inTxPubKey, signatureString=inTxSig, expectContent=inTxID):
            raise SignatureVerifyFailException()


def recursiveCheck(transaction: Transaction, ledger: Ledger, depthRemain=10) -> None:
    """
    Check the Transaction Recursively for #depthRemain recursions.
    :param transaction: The transaction object that is about to be checked.
    :param ledger: The ledger to store all the valid transactions
    :param depthRemain: The remaining depth of recursion -- all the transaction deeper than this depth is trusted to
    be true automatically.
    :return: None
    """
    if transaction.isCoinBase or depthRemain == 0:
        return

    isTransactionBalance(transaction, ledger)
    isTransactionSigValid(transaction, ledger)
    
    for inItem in transaction.inTransactions:
        recursiveCheck(ledger[inItem["inTransactionID"]], ledger, depthRemain=depthRemain - 1)
