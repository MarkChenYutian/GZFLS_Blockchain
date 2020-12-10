# This is a version of transaction written by mark

"""
One Transaction Object
|   inTx       |   inSig   |   outTx   |   reciverPubKey   |  isUsed  |
|  Txn-index_1 | SHA256-...|  10 BTC   |     12387908      |  False   |
|  Txn-index_2 | SHA256-...|   5 BTC   |     23456789      |   True   |
...
"""

class Transaction:
    def __init__(self, allTransaction, amount, reciverPubKey, myPrivateKey, myPubKey):
        """
        self.reciverPubKey is a list of public keys. the #0 of key correspond to the 
        #0 transaction in self.outTx
        self.inTx is a list representing how money come from.
        """
        self.inTx = []
        self.inSig = []
        self.outTx = []
        self.reciverPubKeys = []
        self.isUsed = []
        # You should not save the private key in Transaction object.

        myTxs = self.findMyTransaction(allTransaction, myPubKey)
        currCount = 0
        for Txn, i in myTxs:
            self.inTx.append((Txn, i))
            currCount += allTransaction[Txn].outTx[i]
            if currCount > amount: break
        
        self.outTx.append(amount)
        self.reciverPubKeys.append(reciverPubKey)
        self.isUsed.append(False)

        if currCount > amount:
            self.outTx.append(currCount - amount)
            self.reciverPubKeys.append(myPubKey)
            self.isUsed.append(False)

    def findMyTransaction(self, allTransaction, myPubKey):
        myTransaction = []

        for Txn in allTransaction.keys():       # Txn is the transaction ID
            for i in range(len(allTransaction[Txn].reciverPubKeys)):
                if allTransaction[Txn].reciverPubKeys[i] == myPubKey and allTransaction[Txn].isUsed[i] == False:
                    myTransaction.append((Txn, i))
        
        return myTransaction


