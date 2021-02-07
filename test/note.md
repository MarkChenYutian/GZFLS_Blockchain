Currently, there are some problems in the Blockchain Project that may violate the transaction system:
1. The Transaction ID is easy to duplicate and Hash Collision Attack is possible.
    Currently, Txn = `SHA3_256(str(tx.timestamp * tx.randNum))` Since txn is publish to everyone, everyone who has another transaction `tx2` can modify the `tx2.randNum` such that
    `tx2.randNum * tx2.timestamp = tx.randNum * tx.timestamp`. Because transaction 2 is valid, when Ledger add it into the dictionary, original tx will be erased.
    Malicious people can use this to 'recall' a transaction that is already written in Ledger.

2. It is possible for a malicious node to act like a miner and steal the money from others by operating in this sequence:
    
   a. Pretend to be a miner and get a newTransaction, which is totally valid.
   
   b. Instead of adding it into the block, deny the transaction and record the parameters of inTransactions.
   
   c. use the stored parameters to fake a transaction that use exactly the same inTransaction but different outTransaction.
   
   d. Since all the parameters are valid, attacker can send its own transaction and publish it.
   
**These two problems are all due to over-simplified hash for Transaction Object, so it is necessary to include the immutable informations in the .inTransaction and .outTransaction in the Hashing process of Transaction object.**