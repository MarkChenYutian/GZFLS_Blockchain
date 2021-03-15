from graphviz import Digraph


def visualizeBlockChain(Blockchain) -> None:
    G = Digraph(format="png")
    G.node("0ff", label="ROOT", shape="circle")

    mainChain = set(Blockchain.findMainChain())

    for blockHash in Blockchain.keys():
        if blockHash != "0ff":
            block = Blockchain[blockHash]
            txIDs = "\\n".join(block.transactionIDs)
            if blockHash in mainChain:
                G.node(blockHash, label="Block\\n{}\\nTransaction IDs:\\n\\n{}".format(blockHash, txIDs), shape="box",
                       style="filled", color="green")
            else:
                G.node(blockHash, label="Block\\n{}\\nTransaction IDs:\\n\\n{}".format(blockHash, txIDs), shape="box")

    for blockHash in Blockchain.keys():
        if blockHash != "0ff":
            G.edge(Blockchain[blockHash].prevHash, blockHash, splines="curved")
    showGraph(G)


def showGraph(G: Digraph, name="visualizeBlockchain.gv") -> None:
    G.save("./Storage/" + name)
    G.render("/Storage/" + name)
    G.view()
