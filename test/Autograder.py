from Transaction import TransactionFactory, Transaction
from util.Serialize import Serializable
from Ledger import Ledger
from OP_Script.OP_Factory import OP_Factory
from RSA.RSA_func import generateMyKeys

# Structural Check
assert issubclass(Transaction, Serializable), "Transaction class should be serializable, Sanity Check Failed. Your file may be damaged."
assert issubclass(Ledger, Serializable), "Ledger class should be serializable, Sanity Check Failed. Your file may be damaged."

print("Structural Check Pass")

testLedger = Ledger(doClearInit=True)

# Setup A Factory
Aprivate,Apublic,An = generateMyKeys()
testAOPFactory = OP_Factory()
testAFactory = TransactionFactory((Apublic,An),(Aprivate,An),testAOPFactory)


# setup B Factory
Bprivate, Bpublic, Bn = generateMyKeys()
testBOPFactory = OP_Factory()
testBFactory = TransactionFactory((Bpublic, Bn), (Bprivate, Bn), testBOPFactory)

# A -- 20 --> B
newTx = testAFactory.createTransaction(testLedger, (20,), [testBFactory.myPubKeyHash], isCoinBase=True)
testLedger.addTransaction(newTx)

# B -- 10 --> A
# B -- 10 --> B
newTx2 = testBFactory.createTransaction(testLedger, (10,), [testAFactory.myPubKeyHash], isCoinBase=False)
testLedger.addTransaction(newTx2)

print(testLedger)