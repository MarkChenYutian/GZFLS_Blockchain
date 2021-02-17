"""
This File Describe a Ledger Object that is using shelve to store transactions in File System.

By Mark, 2021/02/13
"""
import json
from hashlib import sha3_256
from typing import List, Tuple

from Utility.shelveManager import ShelveManager
from Transaction.transaction import Transaction


class Ledger(ShelveManager):
    def __init__(self, dataPath):
        super(Ledger, self).__init__(dataPath)

    def __setitem__(self, key: str, item: Transaction):
        """
        Convert the transaction to string, and then store it in Ledger Shelve File.

        :param key: Key of Dictionary stored by shelve. In Ledger class, usually be Transaction ID (uuid4)
        :param item: Transaction Object (which will be serialized to string and saved into Shelve)
        :return: None
        """
        assert isinstance(item, Transaction), "Ledger Object can only store Transaction Object as value"
        item_value = item.dumps()
        super().__setitem__(key, item_value)

    def __getitem__(self, key: str) -> Transaction:
        """
        Get the serialized result from Shelve File, and then convert it back to Transaction Object and return.

        :param key: Transaction ID
        :return: Transaction Object
        """
        item_value = super().__getitem__(key)
        return Transaction.loads(item_value)

    def getUserBalance(self, ScriptHash: str) -> List[float, List[Tuple[str, int]]]:
        """
        :param ScriptHash: the hash value of an user's OP Script.
        :return: [the available balance under that Script, [list of txID, index, and amount for available transactions]]
        """
        balance = 0.0
        tx_items = []
        for txID in self:
            for index, outItem in enumerate(self[txID].outTransactions):
                txScriptHash = sha3_256(json.dumps(outItem['OP_Script']).encode('utf-8')).hexdigest()
                if (not outItem['isUsed']) and ScriptHash == txScriptHash:
                    balance += outItem['amount']
                    tx_items.append((txID, index, outItem['amount']))
        return [balance, tx_items]
