from Block.block import Block
from Block.blockchain import Blockchain
from Block.dummyMiner import dummyMine
from Ledger.ledger import Ledger
from Transaction.transactionFactory import TransactionFactory
from Utility.exceptions import *

# Setup Testing Environment

txFactoryA = TransactionFactory(privateKeyPath="./RSA/PrivateKeyA.pem", publicKeyPath="./RSA/PublicKeyA.pem")
txFactoryB = TransactionFactory(privateKeyPath="./RSA/PrivateKeyB.pem", publicKeyPath="./RSA/PublicKeyB.pem")
txFactoryC = TransactionFactory(privateKeyPath="./RSA/PrivateKeyC.pem", publicKeyPath="./RSA/PublicKeyC.pem")

ledgerA = Ledger("testLedgerA.db")
ledgerB = Ledger("testLedgerB.db")
ledgerC = Ledger("testLedgerC.db")

chainA = Blockchain("testChainA.db")
chainB = Blockchain("testChainB.db")
chainC = Blockchain("testChainC.db")

# Initialize Environment
ledgerA.wipeData()
ledgerB.wipeData()
ledgerC.wipeData()
chainA.wipeData()
chainB.wipeData()
chainC.wipeData()

# Send 100 Coins to A, B, C
# Initialize Head Blocks on each client
bA0 = Block.createHead(difficulty=3)

txs = [
    txFactoryA.fromCoinBase(100),
    txFactoryB.fromCoinBase(100),
    txFactoryC.fromCoinBase(100)
]

for tx in txs:
    bA0.addTransaction(tx)

bA0.finishConstruction(dummyMine)
chainA.addNewBlock(bA0)
chainB.addNewBlock(bA0)
chainC.addNewBlock(bA0)

chainA.syncWithLedger(ledgerA)
chainB.syncWithLedger(ledgerB)
chainC.syncWithLedger(ledgerC)


# C send 15 coins to A, B send 12 coins to C
# Initialize Tail Blocks on each client
bB1 = Block.createTail(chainB.getTail())
bC1 = Block.createTail(chainC.getTail())    # Simulate the Branching

txs = [
    txFactoryC.transactTo(txFactoryA.myPubKeyString, 15, ledgerC),
    txFactoryB.transactTo(txFactoryC.myPubKeyString, 12, ledgerB)
]

bB1.addTransaction(txs[1])

bC1.addTransaction(txs[0])
bC1.addTransaction(txs[1])

bB1.finishConstruction(dummyMine)
bC1.finishConstruction(dummyMine)

chainA.addNewBlock(bB1)
chainB.addNewBlock(bB1)
chainC.addNewBlock(bC1)

chainA.syncWithLedger(ledgerA)
chainB.syncWithLedger(ledgerB)
chainC.syncWithLedger(ledgerC)


# In the previous block, the ledger is split into two versions
# Ledger A, B | A: 105 | B: 98  | C: 97
# Ledger C    | A: 105 | B: 110 | C: 85
#
# C -- 20 --> A && B -- 5 --> C
# A, C continue to construct block based on their own chain (the split continues)

bA2 = Block.createTail(chainA.getTail())
bC2 = Block.createTail(chainC.getTail())

txs = [
    txFactoryB.transactTo(txFactoryC.myPubKeyString, 50, ledgerB),
    txFactoryC.transactTo(txFactoryA.myPubKeyString, 20, ledgerC)
]
for tx in txs:
    bA2.addTransaction(tx)
    bC2.addTransaction(tx)

bA2.finishConstruction(dummyMine)
bC2.finishConstruction(dummyMine)


chainA.addNewBlock(bA2)
chainC.addNewBlock(bC2)
try:
    chainB.addNewBlock(bC2) # Conflict will occur here.
except BlockChainNotSyncException:
    chainB.merge(chainC)

chainA.syncWithLedger(ledgerA)
chainB.syncWithLedger(ledgerB)
chainC.syncWithLedger(ledgerC)
chainB.visualize()

# In the previous block, different branches has been merged.
bB3 = Block.createTail(chainB.getTail())
tx = txFactoryB.transactTo(txFactoryC.myPubKeyString, 21, ledgerB)
bB3.addTransaction(tx)
bB3.finishConstruction(dummyMine)


chainB.addNewBlock(bB3)

try:
    chainA.addNewBlock(bB3)
except BlockChainNotSyncException:
    chainA.merge(chainB)
chainC.addNewBlock(bB3)
chainA.syncWithLedger(ledgerA)
chainB.syncWithLedger(ledgerB)
chainC.syncWithLedger(ledgerC)

ledgerB.visualize()