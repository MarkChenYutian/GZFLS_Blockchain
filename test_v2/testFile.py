from Block.block import Block
from Block.blockchain import Blockchain
from Block.dummyMiner import dummyMine
from Ledger.ledger import Ledger
from Transaction.transactionFactory import TransactionFactory

txFactoryA = TransactionFactory(privateKeyPath="./RSA/PrivateKeyA.pem", publicKeyPath="./RSA/PublicKeyA.pem")
txFactoryB = TransactionFactory(privateKeyPath="./RSA/PrivateKeyB.pem", publicKeyPath="./RSA/PublicKeyB.pem")
txFactoryC = TransactionFactory(privateKeyPath="./RSA/PrivateKeyC.pem", publicKeyPath="./RSA/PublicKeyC.pem")

commonLedger = Ledger(dataPath="commonLedger.db")
commonLedger.wipeData()

b0 = Block.createHead(difficulty=3)

# Give A and B 20 coins each.
newTx1 = txFactoryA.fromCoinBase(amount=20)
newTx2 = txFactoryB.fromCoinBase(amount=20)
newTx3 = txFactoryC.fromCoinBase(amount=20)

commonLedger.addNewTransaction(newTx1)
commonLedger.addNewTransaction(newTx2)
commonLedger.addNewTransaction(newTx3)
b0.addTransaction(newTx1)
b0.addTransaction(newTx2)
b0.addTransaction(newTx3)
b0.finishConstruction(miningFn=dummyMine)

b1 = Block.createTail(b0)
# A give B 5 coins
newTx3 = txFactoryA.transactTo(txFactoryB.myPubKeyString, 5, commonLedger)
commonLedger.addNewTransaction(newTx3)
b1.addTransaction(newTx3)

# B give A, C 10 coins
newTx4 = txFactoryB.transactToMult((txFactoryA.myPubKeyString, txFactoryC.myPubKeyString), (10, 10), commonLedger)
commonLedger.addNewTransaction(newTx4)
b1.addTransaction(newTx4)

# A give C 21 coins
newTx5 = txFactoryA.transactTo(txFactoryC.myPubKeyString, 21, commonLedger)
commonLedger.addNewTransaction(newTx5)
b1.addTransaction(newTx5)

b1.finishConstruction(miningFn=dummyMine)
b2 = Block.createTail(b1)
b3 = Block.createTail(b1)  # Simulate the branching situation in blockchain
# C give B 12 coins
newTx6 = txFactoryC.transactTo(txFactoryB.myPubKeyString, 12, commonLedger)
commonLedger.addNewTransaction(newTx6)
b2.addTransaction(newTx6)
b3.addTransaction(newTx6)
b3.finishConstruction(miningFn=dummyMine)

b4 = Block.createTail(b3)
# B give A 8 coins, C 3 coins
newTx7 = txFactoryB.transactToMult((txFactoryA.myPubKeyString, txFactoryC.myPubKeyString), (8, 3), commonLedger)
commonLedger.addNewTransaction(newTx7)
b2.addTransaction(newTx7)
b4.addTransaction(newTx7)
b2.finishConstruction(miningFn=dummyMine)
b4.finishConstruction(miningFn=dummyMine)

chain1 = Blockchain("testChain1.db")
chain2 = Blockchain("testChain2.db")
chain1.wipeData()
chain2.wipeData()

chain1.addNewBlock(b0)
chain2.addNewBlock(b0)

chain1.addNewBlock(b1)
chain2.addNewBlock(b1)

chain1.addNewBlock(b2)
chain2.addNewBlock(b3)
chain2.addNewBlock(b4)

chain1.merge(chain2)
print(chain1.findMainChain())
print(chain1.getTailID())
chain1.visualize()
