"""
This File describes the blockchain class.
A blockchain will store a series of blocks, which will have a structure of **tree**
Note that there may have sub-chains due to conflict etc.
"""
from Utility.shelveManager import ShelveManager
from Utility.exceptions import BlockNotFoundException, BlockChainNotSyncException, BlockChainNotAcceptException
from Block.block import Block
from Utility.richConsole import console

# Import Visualization Tools
CAN_VISUALIZE = False
try:
    from Visualize.visualizeBlockChain import visualizeBlockChain
    CAN_VISUALIZE = True
except ImportError:
    console.error("Failed to import Visualization Toolset. The visualization method(s) will not be available.")


class Blockchain(ShelveManager):
    def __init__(self, dataPath: str):
        super(Blockchain, self).__init__(dataPath)
        self.maxHeight = -1
        self.numBlock = len(self.keys())
        super().__setitem__("0ff", "ROOT")  # The root of chain.

    def wipeData(self):
        super().wipeData()
        super().__setitem__("0ff", "ROOT")  # The root of chain.

    def __setitem__(self, key: str, item: Block):
        """
        Add a block object into the BlockChain.
        :param key: Key of Dictionary stored by shelve. In BlockChain class, usually the hexHash of block object.
        :param item: the block item to be stored
        :return: None
        """
        assert isinstance(item, Block), "Blockchain class can only store Block Object as value."
        if key in self.keys():
            console().warning("The Blockchain appears to have a hash collision on key {}".format(key))

        item_value = item.dumps()
        super(Blockchain, self).__setitem__(key, item_value)

    def __getitem__(self, key: str) -> Block:
        """
        Get the block object stored in the corresponding key.

        :param key: Block Hash Value
        :return: Block Object
        """
        try:
            item_value = super().__getitem__(key)
            return Block.loads(item_value)
        except KeyError:
            raise BlockNotFoundException(key)

    def addNewBlock(self, newBlock: Block) -> None:
        """
        Add a new block object into the BlockChain
        :return: None
        """
        if newBlock.height <= self.maxHeight:
            # Refuse the block when the block is on a shorter chain.
            raise BlockChainNotAcceptException(newBlock, self.maxHeight)
        if newBlock.prevHash not in self.keys() and self.numBlock != 0:
            # Refuse the block that is not connected to current chain. (Then sync & merge immediately)
            raise BlockChainNotSyncException(newBlock.hexHash(), newBlock.prevHash)

        self.numBlock += 1
        self.maxHeight = newBlock.height

        self[newBlock.hexHash()] = newBlock

    def merge(self, otherChain) -> None:
        diffIds = set(otherChain.keys()) - set(self.keys())
        CHANGENUM = 0

        hasChange = True
        while hasChange:
            hasChange = False
            for diffId in diffIds:
                if otherChain[diffId].prevHash in self.keys() and diffId not in self.keys():
                    self[diffId] = otherChain[diffId]
                    CHANGENUM += 1
                    hasChange = True

        if CHANGENUM < len(diffIds): console.warning("Some of the Blocks failed to merge")

    def findMainChain(self) -> list:
        """
        Find the main Chain of block chain.
        :return: a set of block ids that is on the main chain of blockchain.
        """
        cache = {blockID: list() for blockID in self.keys()}
        tails = self.findLeafNodes()
        for tail in tails:
            currNode = tail
            currPath = [tail]
            while self[currNode].prevHash != "0ff":
                if len(currPath) > len(cache[currNode]):
                    cache[currNode] = currPath
                currNode = self[currNode].prevHash
                currPath.append(currNode)

            if len(currPath) > len(cache["0ff"]):
                cache["0ff"] = currPath

        return cache["0ff"]

    def findLeafNodes(self) -> set:
        """
        Find the leave nodes in the blockchain.
        :return: a set of block ids that is the leave nodes in blockchain.
        """
        isLeafID = {blockId: True for blockId in self.keys()}
        isLeafID.pop("0ff")
        for blockID in self.keys():
            if blockID != "0ff":
                isLeafID[self[blockID].prevHash] = False
        leafID = set()
        for blockID in isLeafID:
            if isLeafID[blockID]:
                leafID.add(blockID)
        return leafID

    def getTailID(self) -> str:
        return list(set(self.findMainChain()).intersection(self.findLeafNodes()))[0]

    def getTail(self) -> Block:
        return self[self.getTailID()]

    def syncWithLedger(self, ledger) -> None:
        mainChain = self.findMainChain()
        TxOnMainChain = []
        TxIDOnMainChain = set()
        for blockID in mainChain:
            TxOnMainChain += self[blockID].transactions
            TxIDOnMainChain = TxIDOnMainChain.union(self[blockID].transactionIDs)

        for txID in ledger.keys():
            # Remove the transaction in ledger that is NOT on main chain
            if txID not in TxIDOnMainChain:
                del ledger[txID]


        hasChange = True
        while hasChange:
            hasChange = False
            for tx in TxOnMainChain:
                if tx.id not in ledger.keys() and {item["inTransactionID"] for item in tx.inTransactions}.issubset(set(ledger.keys())):
                    ledger.addNewTransaction(tx)


    def visualize(self):
        """
        Visualization of blockchain branching.
        """
        if CAN_VISUALIZE:
            try:
                visualizeBlockChain(self)
            except Exception as e:
                console.error("Failed to visualize Blockchain object. No image output. Exception Detail: \n[red]{}[/red]".format(e))
        else:
            console.warning("Blockchain.visualize() is called, but not executed since we can't import the visual tools.")
