from Transaction import TransactionFactory
from Ledger import Ledger
from OP_Factory import OP_Factory
from RSA.RSA_func import generateMyKeys
import json

testLedger = Ledger(doClearInit=True)

# Setup A Factory
Aprivate,Apublic,An = generateMyKeys()
testAOPFactory = OP_Factory()
testAFactory = TransactionFactory((Apublic,An),(Aprivate,An),testAOPFactory)


# setup B Factory
Bprivate, Bpublic, Bn = generateMyKeys()
testBOPFactory = OP_Factory()
testBFactory = TransactionFactory((Bpublic, Bn), (Bprivate, Bn), testBOPFactory)

newTx = testAFactory.createTransaction(testLedger, (20,), [testBFactory.myPubKeyHash], isCoinBase=True)
testLedger.addTransaction(newTx)

newTx2 = testBFactory.createTransaction(testLedger, (10,), [testAFactory.myPubKeyHash], isCoinBase=False)
testLedger.addTransaction(newTx2)

print(testLedger)