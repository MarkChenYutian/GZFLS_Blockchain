# GW Blockchain Project

This project aims to implement a blockchain that can run on local network for educational purpose with pure python.

## Documentation

### class Transaction

This class implement an transaction object in the blockchain. A transaction object is only used to store the information related with transaction.

#### Fields

| Field           | Type         | Explanation                                                  |
| --------------- | ------------ | ------------------------------------------------------------ |
| version         | `float`      | The version of this transaction object. Currently 1.0, if there are soft forking, then the version can be changed. |
| time            | `str`        | The time that transaction object is created.                 |
| id              | `str`        | The unique id of each transaction. (The id is generated using `uuid.uuid4()` in Python) |
| kwargs          | `dict`       | The reserved field to store other properties in transaction object in the future. Currently empty. |
| isCoinBase      | `bool`       | Whether the transaction is from COINBASE.                    |
| inTransactions  | `List[Dict]` | Where the money in transaction comes from.                   |
| outTransactions | `List[Dict]` | Where the money in transaction goes.                         |

The data in `inTransactions` will have such a form

```json
[
    {
        "inTransactionID": "e00538f7-cc63-4846-a45a-25f0c3c1a239",
        "inTransactionIndex": 0,
        "inTransactionSig": "CwaJpxKTEWoauoHyo/ylhoVUsZbtYYM14KrunnFJG43GmyijEdVAXxdBqi6ly3zi0JWNKvOsaxhf3kn0Ki3BHZvVQnC9M03O64/ZeW9snS9VlXX+xReaevH4FMC7ozMX4RpeBo1X/uFo/CTXcv51mOMzYfrD/jRlLFPpXbCTBcY="
    },
    {
        "inTransactionID": "exampleaa-uuid-txid-aaaa-aaaaaaaaaaa",
        "inTransactionIndex": 1,
        "inTransactionSig": "Example Base64 RSA Signature"
    }
]
```

The data in `outTransactions` will have such a form

```json
[
    {
        "amount": 10.0,
        "pubKey": "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC2vrvtk/Rl8OaSsG+IwyvtQs6BrC6pkMkHM8lkX9jQAN8YmX1we5mCBbqykvMfp81XWjktk4P2EiYFqHwPxv2auk1A5B1WOoZaJLByZsufNo2mp/upgMVUDwi/SRopgNWHDtKqqOHo0ljIYyfh1GVxl4qHmKejB4lJ3TTdEdJKCwIDAQAB-----END PUBLIC KEY-----",
        "isUsed": false
    }
]
```

#### Methods

##### addInTransaction(self, inTxID: str, inTxIndex: int, inTxSignature: str) -> None

Add an item of `inTransaction` into the `Transaction` object.

##### addOutTransaction(self, amount: float, pubKey: str, isUsed=False) -> None

Add an item of `outTransaction` into the `Transaction` object.

##### dumps(self, indent=0) -> str

Convert the transaction object to a JSON string. (indent can control the indent of resulting JSON string)

##### @classmethod loads(cls, string: str)

Load the serialized JSON String from method `dumps` to a new Transaction object. Note this is a *classmethod*, so this method should be called directly on class `Transaction` instead of calling on an `Transaction` object.

```python
ExampleString = "{.... Example JSON Serialized Result of Tx Object ...}"
newTransactionObject = Transaction.loads(ExampleString)
```



#### class TransactionFactory

The `Transaction` class will not change the content stored in itself, so the creation of Transaction object is done by the `TransactionFactory`. There are three types of transaction that can be created - Transaction from COINBASE to oneself, Transaction to a single person, Transaction to multiple person at the same time.

#### Fields

| Fields         | Type                    | Explanation                                                  |
| -------------- | ----------------------- | ------------------------------------------------------------ |
| myPubKey       | `RsaKey`                | The public key of owner of TransactionFactory                |
| _myPrivateKey  | `RsaKey`, private field | The private key of owner of TransactionFactory, used to create signature |
| myPubKeyString | `str`                   | The string version of owner's public key (directly loaded from .pem key file) |

During the initialization process, if the RSA keys failed to load from the file path, then RSA keys will be generated automatically and then loaded.

#### Methods

##### fromCoinBase(self, amount: float) -> Transaction

Transaction from COINBASE to oneself.

##### transactTo(self, receiver_pubKey: str, amount: float, ledger) -> Transaction

Create a Transaction object transact to specific receiver public key.

##### transactToMult(self, pubKeys: tuple, amounts: tuple, ledger: Ledger) -> Transaction

Transact to multiple public keys at a same time.



### class ShelveManager

This class provide an encapsulation on Python Shelve operation so we can use a shelve object exactly like a Python Dictionary (and don't need to open / close shelve explicitly in our code).

#### Fields

| Field    | Type  | Explanation                   |
| -------- | ----- | ----------------------------- |
| dataPath | `str` | The path of Shelve File.      |
| len      | `int` | The number of item in Shelve. |

If the dataPath designated does not exist, the ShelveManager will create a new shelve automatically at the position of dataPath.

#### Methods

##### \_\_getitem\_\_(self, item: str) -> str

##### \_\_setitem\_\_(self, key: str, item: str) -> None

##### \_\_delitem\_\_(self, key) -> None

##### \_\_contains\_\_(self, key) -> bool

With this method implemented, you can check whether a key is in the dictionary using

```python
key in ShelveManagerObject
```

##### \_\_iter\_\_(self) -> iterator

Returns an iterator on all the keys in dictionary.

##### keys(self) -> dictKeys

##### wipeData(self) -> None

Wipe all the data in shelve method. **This operation is NOT INVERTABLE, the data will lost forever.**

