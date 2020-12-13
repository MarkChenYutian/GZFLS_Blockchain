# Description

A transaction object has several properties - `InTx`, `inSig`, `OutTx`, `reciverPubKey`, and `isUsed`.

## Transaction Validation

When we want to validate a transaction, we should

1. get public key from `AllTransactions[txn].reciverPubKey[i]`, in this step, if `AllTransactions[txn].isUsed[i]` is true, terminate the validation process since this input is False.
2. Use the public key get in step 1 to decrypt the signature in `CurrentTx.inSig[i']`.
3. Check whether `hash(AllTransactions[txn])` is equal to `decrypt(CurrentTx.inSig[i])`.
4. Perform this check process on all the `inTx`. If one of them is 'false', the whole Transaction is invalid.

## Create Transaction

