"""
This File writes the Transaction Class For GZFLS Blockchain Project
By Mark, 2021 / 02 / 11
"""
import uuid
import json
import time
from hashlib import sha3_256


class Transaction:
    """
    Transaction class is only used to store value, no actual method is defined here.
    Methods to create a Transaction object is defined in TransactionFactory class.
    """
    def __init__(self, isCoinBase=False, **kwargs):
        self.version = 1.0
        self.time = time.time()
        self.id = str(uuid.uuid4())
        self.kwargs = kwargs  # reserved for future updates

        self.isCoinBase = isCoinBase
        self.inTransactions = []
        self.outTransactions = []

    def addInTransaction(self, inTxID: str, inTxIndex: int, inTxSignature: str) -> None:
        """
        :param inTxID: Transaction ID of inTransaction (note: it's different from hash(inTransaction) in this version)
        :param inTxIndex: The index of item in outTransaction of inTransaction
        :param inTxSignature: The signature of TxID for inTransaction
        :return: None
        """
        self.inTransactions.append({
            "inTransactionID": inTxID,
            "inTransactionIndex": inTxIndex,
            "inTransactionSig": inTxSignature,
        })

    def addOutTransaction(self, amount: float, pubKey: str, isUsed=False) -> None:
        """
        :param amount: The amount of money in transaction
        :param OP_Script: The OP Script used to prove the ownership of transaction
        :param isUsed: whether the output is used
        :return: None
        """
        self.outTransactions.append({
            "amount": amount,
            "pubKey": pubKey,
            "isUsed": isUsed
        })

    def dumps(self) -> str:
        """
        convert the current object to a string for web transport etc.
        :return:
        """
        info_dict = {
            "type": "Transaction",
            "version": self.version,
            "isCoinBase": self.isCoinBase,
            "time": self.time,
            "id": self.id,
            "kwargs": self.kwargs,
            "inTransactions": self.inTransactions,
            "outTransactions": self.outTransactions
        }
        return json.dumps(info_dict)

    @classmethod
    def loads(cls, string: str):
        """
        load all the properties from a serialized Transaction Result.
        :param string: string that is about to load
        :return: The loaded transaction object
        """
        info_dict = json.loads(string)
        assert info_dict['type'] == "Transaction", "Can only load from the serialized result of Transaction Class"
        newTx = cls(isCoinBase=info_dict['isCoinBase'])
        # Load basic properties
        newTx.id = info_dict['id']
        newTx.time = info_dict['time']
        newTx.version = info_dict['version']
        newTx.kwargs = info_dict['kwargs']
        # Add 'inTransaction'
        for json_inTx in info_dict['inTransactions']:
            inTxID = json_inTx['inTransactionID']
            inTxIndex = json_inTx['inTransactionIndex']
            inTxSig = json_inTx['inTransactionSig']
            newTx.addInTransaction(inTxID, inTxIndex, inTxSig)
        # Add 'outTransaction'
        for json_outTx in info_dict['outTransactions']:
            outAmount = json_outTx['amount']
            outPubKey = json_outTx['pubKey']
            outIsUsed = json_outTx['isUsed']
            newTx.addOutTransaction(outAmount, outPubKey, isUsed=outIsUsed)

        return newTx

    def __eq__(self, other) -> bool:
        return self.id == other.id and hash(self) == hash(other)

    def __hash__(self) -> int:
        infoString = self.id
        infoString += "".join([str(item['inTransactionID']) +
                              str(item['inTransactionSig']) for item in self.inTransactions])
        infoString += "".join([str(item["pubKey"]) for item in self.outTransactions])
        return int(sha3_256(infoString.encode('utf-8')).hexdigest(), 16)

    def __repr__(self) -> str:
        return "<Transaction object at {} with transactionID {}>".format(id(self), self.id)

    def __str__(self) -> str:
        string = "====================\n" \
                 "| Transaction ID: {}\n" \
                 "| isCoinBase: {}\n" \
                 "|-------------------\n" \
                 "| + In Transactions:\n".format(self.id, self.isCoinBase)
        string += "| " + json.dumps(self.inTransactions)
        string += "\n| + Out Transactions:\n"
        string += "| " + json.dumps(self.outTransactions)
        string += "\n===================="
        return string


if __name__ == "__main__":
    test = Transaction()
    test.addInTransaction("testID1", 0, "ExampleSignature")
    test.addOutTransaction(0.2, "ExamplePubKey")
    serialized = test.dumps()
    print(serialized)
    loaded = Transaction.loads(serialized)
    print(repr(loaded))


