import uuid
from graphviz import Digraph
from Utility.richConsole import console


def visualizeBlockChain(Blockchain) -> None:
    G = Digraph(format="png")
    G.node("0ff", label="ROOT", shape="circle")

    mainChain = set(Blockchain.findMainChain())

    for blockHash in Blockchain.keys():
        if blockHash != "0ff":
            block = Blockchain[blockHash]
            txIDs = "\\n".join(block.transactionIDs)
            if blockHash in mainChain:
                G.node(blockHash, label="Block Hash\\n{}\\nTransaction IDs:\\n\\n{}".format(blockHash, txIDs), shape="box",
                       style="filled", color="0.33 0.5 0.8")
            else:
                G.node(blockHash, label="Block\\n{}\\nTransaction IDs:\\n\\n{}".format(blockHash, txIDs), shape="box")

    for blockHash in Blockchain.keys():
        if blockHash != "0ff":
            G.edge(Blockchain[blockHash].prevHash, blockHash, splines="curved")
    showGraph(G)


def showGraph(G, name="visualizeBlockchain"):
    name += "_" + str(uuid.uuid4()) + ".gv"
    G.save("./Storage/" + name)
    console.info("Visualization Rendering. Graphviz source code is stored in Storage/{}".format(name))
    G.render("/Storage/" + name)
    G.view()

