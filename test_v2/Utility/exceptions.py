"""
Author: Mark, 2021/3/13
This file define the exceptions in Blockchain project.
"""

class BlockchainException(Exception):
    """
    The Base Exception Class for whole Project.
    """
    pass

class SerializationProcessException(BlockchainException):
    """
    This exception is raised when the Serialization / Loading Process failed in Blockchain Project.
    """
    def __init__(self, serializeMsg, isLoad=True):
        self.msg = serializeMsg
        self.isLoad = isLoad

    def __str__(self):
        if self.isLoad:
            return "Failed to load from the given Serialized string. " \
                   "See the property SerializationProcessException.msg for more details."


class TransactionNotExist(BlockchainException):
    """
    Raise this exception when the Transaction ID does not exist in the ledger
    """
    def __init__(self, TransactionID):
        self.TxID = TransactionID

    def __str__(self):
        return "Transaction with TxID {} does not exist in the Ledger.".format(self.TxID)


class NotEnoughBalanceException(BlockchainException):
    """
    Raise this exception when the Transaction initiator does NOT have enough balance in ledger.
    """
    def __init__(self, currentBalance, minBalanceAccepted):
        self.currBalance = currentBalance
        self.minBalance = minBalanceAccepted

    def __str__(self):
        return  "You don't have enough balance to initiate the transaction. Transaction creation process" \
                "terminated.\nYou have {} coins while a minimum of {} coins is required."\
                .format(self.currBalance, self.minBalance)


class NotBalanceTransactionException(BlockchainException):
    """
    Raise this exception when the transaction received is NOT balanced on input and outputs.
    """
    def __init__(self, inAmount, outAmount):
        self.inAmount = inAmount
        self.outAmount = outAmount

    def __str__(self):
        return "The given transaction is Not balance on inTransaction and outTransaction. There are {} \
        coins on inTransaction but {} on outTransaction.".format(self.inAmount, self.outAmount)


class SignatureVerifyFailException(BlockchainException):
    """
    raise this exception when the signature verification failed.
    """
    def __init__(self): pass
    def __str__(self): return "Signature Verification Failed, Transaction is invalid."


class BlockNotFinishException(BlockchainException):
    """
    Raise this exception when someone try to apply methods on an unfinished block inappropriately. e.g. calculate the
    hash of block when block is not finished yet (which is inappropriate since the root hash is not calculated yet)
    """
    def __init__(self): pass
    def __str__(self): return "The Block you are operating on is not marked as 'Finish' yet."

