from Transaction import Transaction
from Ledger import Ledger
from RSA_func import *

if __name__ == "__main__":
    names = ["A", "B", "C"]
    RSA_keys = dict()
    for name in names:
        RSA_keys[name] = generateMyKeys()

    #### INITIALIZE WITH SOME TRANSACTIONS ####
    allTransaction = Ledger()
    for name in names:
        newTx = Transaction(allTransaction, 100, 0, 0, 0, RSA_keys[name][1], isCoinBase=True)
        allTransaction.addTransaction(newTx)
    ###########################################
    
    # A -- 50 --> B
    newTx = Transaction(allTransaction, 50, RSA_keys["A"][1], RSA_keys["A"][0], RSA_keys["A"][2], RSA_keys["B"][1])
    allTransaction.addTransaction(newTx)
    
    # B -- 25 --> C
    newTx = Transaction(allTransaction, 25, RSA_keys["B"][1], RSA_keys["B"][0], RSA_keys["B"][2], RSA_keys["C"][1])
    allTransaction.addTransaction(newTx)

    # Tampered Transaction Test
    # B --- 10 ---x---> A
    newTx = Transaction(allTransaction, 10, RSA_keys["B"][1], RSA_keys["B"][0], RSA_keys["B"][2], RSA_keys["A"][1])
    newTx.outTransaction[0][0] = 20
    try:
        allTransaction.addTransaction(newTx)
    except:
        pass

    print(RSA_keys)
    print(allTransaction)
    print("\n")
    print(allTransaction.getBalanceStat())
    
    
