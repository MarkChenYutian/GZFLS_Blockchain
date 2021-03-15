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
        return "You don't have enough balance to initiate the transaction. Transaction creation process" \
               "terminated.\nYou have {} coins while a minimum of {} coins is required." \
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


class BlockNotFoundException(BlockchainException):
    """
    The specific block is not found in the blockchain object.
    """

    def __init__(self, blockID):
        self.blockID = blockID

    def __str__(self): return "The Block with block ID {} is not stored in the BlockChain object.".format(self.blockID)


class BlockChainNotSyncException(BlockchainException):
    """
    When this exception is raised, the block chain object received a block that Can't be merged into the current blockchain
    ( the previous hash does not exist in blockchain dictionary ). In this case, the current block chain have to merge with the
    blockchain with another branch.
    """

    def __init__(self, blockID, prevHash):
        self.prevHash = prevHash
        self.blockID = blockID

    def __str__(self):
        return "The block chain receive a new block (with ID {}) where prevHash ({}) is not in the chain.".format(
            self.blockID, self.prevHash)


class BlockChainNotAcceptException(BlockchainException):
    """
    The blockchain refused to add a node into the chain since node's height is lower than current main chain stored in
    blockchain object.
    """

    def __init__(self, block, minHeight):
        self.blockHeight = block.height
        self.blockHash = block.hexHash()
        self.minHeight = minHeight

    def __str__(self):
        return "The blockchain refused to add block into the chain. The block {} has height {} while a " \
               "minimum height of {} is required.".format(self.blockHash, self.blockHeight, self.minHeight + 1)
