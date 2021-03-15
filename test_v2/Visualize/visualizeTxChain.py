import uuid
from graphviz import Digraph
from Utility.richConsole import console


def visualizeTransactionChain(ledger):
    G = Digraph(comment="Visualization of Transaction Flow in Ledger.", format="png")
    G.node("ROOT", label="COINBASE", shape="box")
    colorBar = colorDistributor(ledger)
    for txID in ledger.keys():
        visualizeTransaction(G, ledger[txID], colorBar, ledger)
    showGraph(G)


def colorDistributor(ledger):
    stat = ledger.getBalanceStat()
    colorBar = dict()
    H, S, V = 0, 0.4, 0.8
    for pubKey in stat:
        colorBar[pubKey] = "{} {} {}".format(H, S, V)
        H += 1 / len(stat)
    return colorBar


def visualizeTransaction(G: Digraph, transaction, colorBar, ledger):
    if transaction.isCoinBase:
        G.node(transaction.id,
               label="Transaction ID: \\l" + transaction.id,
               shape="box",
               style="filled",
               color=colorBar[transaction.outTransactions[0]["pubKey"]])
        tempID = transaction.id + "-0"
        G.node(tempID,
               str(transaction.outTransactions[0]["amount"]),
               shape="oval",
               color=colorBar[transaction.outTransactions[0]["pubKey"]],
               style="filled")
        G.edge("ROOT", transaction.id)
        G.edge(transaction.id, tempID)
    else:
        preID = transaction.inTransactions[0]["inTransactionID"]
        preIndex = transaction.inTransactions[0]["inTransactionIndex"]
        G.node(transaction.id,
               label="Transaction ID: \\l" + transaction.id,
               shape="box",
               style="filled",
               color=colorBar[ledger[preID].outTransactions[preIndex]["pubKey"]])
        for inItem in transaction.inTransactions:
            inTxID = inItem["inTransactionID"]
            inTxIndex = inItem["inTransactionIndex"]
            G.edge(inTxID + "-" + str(inTxIndex), transaction.id)
        for index, outItem in enumerate(transaction.outTransactions):
            G.node(transaction.id + "-" + str(index), str(outItem["amount"]),
                   shape="oval",
                   color=colorBar[transaction.outTransactions[index]["pubKey"]],
                   style="filled")
            G.edge(transaction.id, transaction.id + "-" + str(index))


def showGraph(G, name="visualizeLedger"):
    name += "_" + str(uuid.uuid4()) + ".gv"
    G.save("./Storage/" + name)
    console.info("Visualization Rendering. Graphviz source code is stored in Storage/{}".format(name))
    G.render("/Storage/" + name)
    G.view()
