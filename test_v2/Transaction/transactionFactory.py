"""
This file define the TransactionFactory class to create an actual transaction object.
By Mark, 2021/02/12
"""
from Transaction.transaction import Transaction
from Ledger.ledger import Ledger
from Utility.exceptions import NotEnoughBalanceException
from RSA.RSA_util import *


class TransactionFactory:
    def __init__(self, privateKeyPath="./RSA/PrivateKey.pem", publicKeyPath="./RSA/PublicKey.pem"):
        """
        :param privateKeyPath: The file path to private key file for the specific user.
        :param publicKeyPath: The file path to public key file for the user.
        """
        try:
            self.myPubKey, self._myPrivateKey = loadKeys(privateKeyPath=privateKeyPath, pubKeyPath=publicKeyPath)
        except FileNotFoundError:
            print("No Key File Detected. The RSA Keys will be generated in directory ./RSA as default.")
            generateRSAKey(publicKeyPath=publicKeyPath, privateKeyPath=privateKeyPath)
            self.myPubKey, self._myPrivateKey = loadKeys(privateKeyPath=privateKeyPath, pubKeyPath=publicKeyPath)
        self.myPubKeyString = open(publicKeyPath).read().strip().replace("\n", "")

    def fromCoinBase(self, amount: float) -> Transaction:
        """
        :param amount: The amount of coin transact to client through coinbase.
        :return: Transaction Object
        """
        newTx = Transaction(isCoinBase=True)
        newTx.addOutTransaction(amount, self.myPubKeyString)
        return newTx

    def transactTo(self, receiver_pubKey: str, amount: float, ledger) -> Transaction:
        """
        :param ledger: The Ledger object that stores all the VALID transaction in it.
        :param receiver_pubKey: The receiver's Public Key
        :param amount: Amount of money transact to receiver.
        :return: Transaction Object
        """
        balance, myTransactions = ledger.getUserBalance(self.myPubKeyString)
        if balance < amount:
            raise NotEnoughBalanceException(balance, amount)

        newTx = Transaction(isCoinBase=False)
        total_in, index = 0.0, 0
        while total_in < amount and index < len(myTransactions):
            myTxID, myTxIndex, myTxAmount = myTransactions[index]
            total_in += myTxAmount
            myTxSignature = signSignature(self._myPrivateKey, myTxID)
            newTx.addInTransaction(myTxID, myTxIndex, myTxSignature)
            index += 1

        if total_in > amount:
            newTx.addOutTransaction(total_in - amount, pubKey=self.myPubKeyString)
        newTx.addOutTransaction(amount, pubKey=receiver_pubKey)
        return newTx

    def transactToMult(self, pubKeys: tuple, amounts: tuple, ledger: Ledger) -> Transaction:
        """
        :param pubKeys: The public keys of receivers you want to transact to.
        :param amounts: Amount of money transact to each receiver
        :param ledger: The Ledger object that stores all the VALID transaction in it.
        :return: Transaction Object
        """
        balance, myTransactions = ledger.getUserBalance(self.myPubKeyString)
        totalAmount = sum(amounts)

        if balance < totalAmount:
            raise NotEnoughBalanceException(balance, totalAmount)

        newTx = Transaction(isCoinBase=False)
        total_in, index = 0.0, 0

        while total_in < totalAmount and index < len(myTransactions):
            myTxID, myTxIndex, myTxAmount = myTransactions[index]
            total_in += myTxAmount
            myTxSignature = signSignature(self._myPrivateKey, myTxID)
            newTx.addInTransaction(myTxID, myTxIndex, myTxSignature)
            index += 1

        if total_in > totalAmount:
            newTx.addOutTransaction(total_in - totalAmount, pubKey=self.myPubKeyString)

        for receiverPubKey, receiverAmount in zip(pubKeys, amounts):
            newTx.addOutTransaction(receiverAmount, receiverPubKey)

        return newTx
