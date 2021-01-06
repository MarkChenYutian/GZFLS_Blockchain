import util


class MerkelTree:
    def __init__(self, transactions):
        """
        self.transactions - a list of transaction object
        self.tree = [
            [nodes in height 8], 
            [nodes in height 7], 
            ..., 
            [node in height 0 (root)]
        ]

                    [self.tree[8][0]]
                        /   \
        [self.tree[7][0]]   [self.tree[7][1]]
            /   \                   /   \
                        ...
        """
        for _ in range(16 - len(transactions)):
            transactions.append("EMPTY PLACEHOLDER")
        self.transactions = transactions    # list<Transaction>
        self.tree = []
        self.root = None
        height0 = [util.hashObject(tx) for tx in self.transactions]
        self.tree.append(height0)

        while (len(self.tree[-1]) > 1):
            newLayer = []
            for index in range(0, len(self.tree[-1]), 2):
                combinedHash = util.hashObject(self.tree[-1][index] + self.tree[-1][index + 1])
                newLayer.append(combinedHash)
            self.tree.append(newLayer)

        self.root = self.tree[-1][0]
    
    def getRelatedNodes(self, index):
        relatedNodes = []
        for height in range(len(self.tree) - 1):
            if index % 2:
                relatedNodes.append(self.tree[height][index - 1])
            else:
                relatedNodes.append(self.tree[height][index + 1])
            index  = index // 2
        return relatedNodes
