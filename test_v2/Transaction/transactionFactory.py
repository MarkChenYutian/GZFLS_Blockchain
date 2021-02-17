"""
This file define the TransactionFactory class to create an actual transaction object.
By Mark, 2021/02/12
"""
import json
from hashlib import sha3_256
from typing import *
from Transaction.transaction import Transaction

# Type Definition
Script = Dict[AnyStr, List[AnyStr]]


class TransactionFactory:
    def __init__(self, myScript: Script, mySecret: Any):
        """
        :param myScript: The script that will be written by others in transaction to you.
        :param mySecret: The parameters that will allow 'myScript' return True
        """
        assert myScript['type'] == 'Script'
        self.myScript = myScript
        self.myScriptHash = sha3_256(json.dumps(myScript).encode('utf-8')).hexdigest()
        # Protected Attribute
        self._mySecret = mySecret

    def fromCoinBase(self, amount: float) -> Transaction:
        """
        :param amount: The amount of coin transact to client through coinbase.
        :return: Transaction Object
        """
        newTx = Transaction(isCoinBase=True)
        newTx.addOutTransaction(amount, self.myScript)
        return newTx

    def transactTo(self, receiver_Script: Script, amount: float, ledger) -> Transaction:
        """
        :param ledger: The Ledger object that stores all the VALID transaction in it.
        :param OP_Script_param: Parameters to generate OP Script to check ownership of coins for receiver
        :param amount: Amount of money transact to receiver.
        :return: Transaction Object
        """
        # TODO: Create a Transaction Object normally.
        balance, availableTx = ledger.getUserBalance(self.myScriptHash)
        # FIXME: replace Exception with more specific Blockchain Exception Type
        if balance < amount: raise Exception("Not Enough Balance to create the designated transaction")

        newTx = Transaction()
        curr_amount = 0
        for txID, index, amount in availableTx:
            curr_amount += amount
            newTx.addInTransaction()
            if curr_amount >= amount:

    def transactToMul(self, OP_Script_param: Tuple[Script], amount: Tuple[float]) -> Transaction:
        """
        :param OP_Script_param: Tuple of OP Script Parameters for different receivers.
        :param amount: Amount of money transact to each receiver
        :return: Transaction Object
        """
        # TODO: Create a Transaction Object with multiple outputs.
