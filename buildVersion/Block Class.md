# Block Class

### 1.1 Brief Intro

this project we need to write the block class of the blockchain. The project is based on the last project. In this project we need to write `block.py`

### 1.2The Property Intro

This part introduce the property your `Block` class should include
|      Property      |   Type   | Meaning                                                      |
| :----------------: | :------: | ------------------------------------------------------------ |
| `Merkle_Tree_Root` | `String` | the Merkle_Tree_Root of the transactions,you need to use funcation`Make_tree()`to generate it from the given transactions |
|  `pre_block_hash`  |  `int`   | the previous block hash                                      |
|      `nounce`      |  `int`   | the `nounce` value of the block                              |
|    `timestamp`     | `float`  | the timestamp of the block you can get this by using time module |
|      `index`       |  `int`   | the index (or the height) of the block in the blockchain     |

###  1.3 The Method Intro

your `Block`class must include the following methods:

|   Function Name   |                     Function Description                     |
| :---------------: | :----------------------------------------------------------: |
|   `__init__()`    | this is the constructor of your `Block`class, you need to initialize the Property mention in the part 1.2 |
|     `hash()`      | you need to include the properties(***pre_block_hash***, ***nounce***,and ***timestamp***)to a str and hash it by using ==<u>[sha256](https://en.bitcoinwiki.org/wiki/SHA-256#:~:text=SHA-256%20is%20a%20member%20of%20the%20SHA-2%20cryptographic,the%20NSA.%20SHA%20stands%20for%20Secure%20Hash%20Algorithm.)</u>==. you need to return the hash of the block which is an Integer, you may need to use some function in `hashlib` module which will introduce in part 1.4 |
| `get_tree_root()` | given a list of transactions, you need to return the Merkle_tree root of this transactions,you may use the function `merge()` |
|     `merge()`     | given a list of hash you need to merge their by pair  until there is only one hash |

### 1.4 Notes

there are some function you can use went programming the `Block`class

#### `time`

you can use the funcation`time.time()`to get the time. notise,  it return the time in a format of float you need to convert it to `String` by using `str()`when writing the `hash()`function

#### `hashlib`

you can use function`hashlib.sha256()`to get the hash of an object, but it is in a format of Hash Object you need to use`hexdigist()`to make the result a hex and you need to convert it to Integer when wrting`hash()`

```python
import hashlib
hashlib.sha256(a).hexdigest()
```

### 1.5 Merkle Tree
##### get_tree_root()

in this function you need to convert every  transaction to their hash and used a list to contain them. Then you will need to used `merge()`to merge each hash together and finally get the tree root

##### merge()

you need to combine each hash together by pair until their is one .

All the steps are as following:

---

```mermaid
graph RL;
H1((SHA256))
H2((SHA256))
H3((SHA256))
H4((SHA256))
C5[Concat]
C6[Concat]
C7[Concat]
H5((Hash))
H6((Hash))
H7((Hash))

Tx1[(Transaction 1)]
Tx2[(Transaction 2)]
Tx3[(Transaction 3)]
Tx4[(Transaction 4)]

subgraph Height 0
node1(Hash Node 1)
node2(Hash Node 2)
node3(Hash Node 3)
node4(Hash Node 4)
end

subgraph Height 1
node5(Hash Node 5)
node6(Hash Node 6)
end

subgraph Height 2
root(Root)
end

Tx1 --> H1
Tx2 --> H2
Tx3 --> H3
Tx4 --> H4
H1 --> node1
H2 --> node2
H3 --> node3
H4 --> node4
node1 --> C5
node2 --> C5
node3 --> C6
node4 --> C6
C5 --> H5
C6 --> H6
H5 --> node5
H6 --> node6
node5 --> C7
node6 --> C7
C7 --> H7
H7 --> root
```



