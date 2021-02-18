# GZFLS Blockchain Project

This project aims to build a working blockchain on the base of Python that work as the projects in CS2 - Blockchain and Cryptography.

## Project Structure

The project have three main parts - worker, miner and webAgent

```
Project
   |
   |-Worker
   |   |- Validate Transaction
   |   |- Create Transaction
   |   |- Maintain Ledger
   |-Miner
   |   |- Create Block (mining)
   |-WebAgent
       |- Send / Receive Transaction
       |- Sent / Receive Block
```

In the actual project, these three parts are divided into three different processes.

## Documentation

### Transaction

#### Class `Transaction`

##### Field

The `Transaction` class only store the information of a transaction. The methods stored in it includes:

1. Where the money comes from
   
   `.inTransactions` store the source of money in Transaction. Unless the money comes from `COINBASE`, the money in transaction should have a source (i.e. how the transaction initiator get these money)
   
   The `.inTransaction` property is a list with dictionaries in it.
   
   ```python
   self.inTransaction = [
       {
           "inTransactionID":  # Transaction ID, uuid4
           "inTransactionIndex": # where the money comes from in the outTransaction
           "scriptAnswer": # Proper parameter that will let OP Script return True
       }
   ]
   ```
   
2. Who will receive the money

   The `.outTransactions` property in the Transaction class is used to store where the money goes. It is a list with dictionaries inside.

   ```python
   self.outTransaction = [
       {
           "amount": # float, the amount of money give to this receiver
           "OP Script": # The OP Script that is used to verify the identity of receiver
           "isUsed": # whether this transaction output is already spent by receiver
       }
   ]
   ```

3. The time that Transaction is created

   `Transaction.time` is the time that Transaction object is created.

4. The ID of Transaction

   `Transaction.ID` is the `uuid` of Transaction Object that is created when running `__init__`.

5. Version

   The version of Transaction object - a float, currently `1.0`

6. Reserved Field

   The `self.kwargs` property is a reserved property of Transaction Object for future use. If you want to put something in the Transaction Object, you can pass through the keyword arguments of `__init__` function.

##### Methods

1. `addInTransaction(self, inTxID, inTxIndex, inTxAnswer)`

   Create a new entry in the `.inTransaction` property of `Transaction` object.

2. `addOutTransaction(self, amount, OP_Script, isUsed=False)`

   Create a new entry in the `.outTransaction` property of `Transaction` object.

3. `dumps(self)`

   **Serialize** The Transaction Object. Using JSON to serialize the Transaction object into a string so that it can be stored into the `shelve` (in file system).

   The serialized result will have a structure like this:

   ```json
   {
       "type": "Transaction",
       "version": 1.0,
       "isCoinBase": False,
       "time": 12345679,
       "id": "uuid-example-uuidString",
       "kwargs": {
          	/* Currently empty, reserved for future use */
       },
       "inTransactions": [
           {
               "inTransactionID": "uuid-example-uuidString2",
               "inTransactionIndex": 0,
               "inTransactionAnswer": [
                   12345,
                   "example-rsa-result"
               ]
           },
           /*Other inTransaction items*/
       ],
       "outTransactions": [
           {
               "amount": 4.29,
               "OP_Script": "Example Script",
               "isUsed": True
           },
           /*Other outTransaction items*/
       ]
   }
   ```

4. *`@classmethod`* `loads(cls, String)`

   This is a class method, which means that you should call this method by calling

   ```python
   Transaction.load(exampleString)		# Correct
   TxObject.load(exampleString)		# Incorrect, exception will be raised.
   ```

5. Internal Functions

   Functions like `__eq__`, `__hash__`, `__repr__`, and `__str__` are defined to provide some basic methods.

#### Class `TransactionFactory`

As we have described above, the `Transaction` class does not contain any methods to create its content. Since there are multiple was to create a Transaction object, we specially use a `TransactionFactory` class to create Transactions.

##### Field

> ⚠ ==This sections is not determined yet, the content may change as we develop the project.==

The `TransactionFactory` contains two fields - `mySecret` and `myIdentifier` , this is used to generate the `OPAnswer` in the `inTransaction` of new Transaction object and find the available money in Ledger.

##### Methods

A Transaction Factory has three methods to create Transactions

1. `fromCoinBase(self, amount:float) -> Transaction`

   Create a transaction from `COINBASE` send  `amount` to the owner of `TransactionFactory` himself.

2. `transactTo(self, receiverScript, amount, ledger) -> Transaction`

   Create a transaction to a specific receiver. The identity of receiver is designated by the `receiverScript`, which , by design, will return `True` only with the specific parameter provided by receiver.

3. `transactToMul(self, receiverScripts, amounts, ledger) -> Transaction`

   Create a transaction with multiple output. With this output methods, you can "combine" multiple transactions together and make the blockchain more efficient.

### Ledger

#### Class `ShelveManager`

In this project, we want the data be kept in the file system so that we can resume from the progress we have already made. To save data after the program is terminated, we use a python internal module called `shelve`. It will create a dictionary in the file system where we can open to perform get, delete, find, and change value of it.

However, since it is in the file system, every time you want to use the data inside it, you will have to open the shelve and close it like this:

```python
with shelve.open("./cache/ledger.db") as ledger:
    ledger['uuid-example-id1'] = newTransactionObject
```

It will be inconvinent if such code is repeated multiple times in the single file. To solve this problem, we use the `LedgerManager` class to encapsulate it so that you can interact with `LedgerManager` class just as it is a dictionary without thinking open / file IO.

##### Field

1. `self.len`

   The number of items currently in the shelve

2. `self.dataPath`

   The path of Shelve file (designated when `__init__` is called)

##### Method

1. `__len__(self)` 

   Get the number of item stored in the shelve. (call this function by using `len(ShelveManagerObj)`)

2. `__getitem__(self, key)`

   Get the value of corresponding key.

   > Call this method by calling `ShelveManagerObj[key]`

3. `__setitem__(self, key, value)`

   Set a new key-value pair in the shelve
   
   > Call this method by calling `ShelveManagerObj[key] = value`
   
4. `__delitem__(self, key)`
   
   Remove a specific key-value pair inside the shelve.
   
   > Call this method by calling `del ShelveManagerObj[key]` or `ShelveManagerObj.pop(key)`

5. `__iter__(self)`
   
   Return the iterator of `self.keys()`
   
   > Call this method by calling `for key in ShelveManagerObj`
   
6. `__contains__(self, key)`

   Return `True` or `False` depend on whether the key is stored in the shelve.

   > Call this method by calling `key in ShelveManagerObj`

7. `wipeData(self, doWipe=False)`

   clean all the data inside the shelve by deleting all the key-value pair. When the `doWipe` keyword argument is `True`, the wiping process will be silent, otherwise, a prompt will pop up in the terminal.

#### Class `Ledger`

This class inherited from class `ShelveManager` and modify the `__getitem__` and `__setitem__` method to encapsulate the serialize process.

##### Field

The field of Ledger object is the same as `ShelveManager` object.

##### Method

The Ledger class have most of its methods same as the `ShelveManager` class. Below will only list the overriding methods in class `Ledger`.

1. `__getitem__(self, key)`

   The ledger will automatically convert the serialized result stored in shelve into Transaction object and return it.

2. `__setitem__(self, key, value)`

   The parameter `value` must be a transaction object, or exception will be raised.

   The value will be serialized to string and then add into shelve.
   
3. `getUserBalance(self, identifier)`

   > ⚠ This method is not yet implemented. So there may have some changes in the release version.

   This method will return the unspent money under an identifier (currently, identifier is either Public Key or Public Key Hash).