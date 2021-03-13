import os
import uuid
from graphviz import Digraph

def visualizeTransactionChain(ledger):
    G = Digraph(comment="Visualization of Transaction Flow in Ledger.", format="png")
    G.node("ROOT", label="COINBASE", shape="box")
    for txID in ledger.keys():
        visualizeTransaction(G, ledger[txID])
    showGraph(G)

def visualizeTransaction(G: Digraph, transaction):
    G.node(transaction.id, label=transaction.id, shape="box")
    if transaction.isCoinBase:
        tempID = transaction.id + "-0"
        G.node(tempID, str(transaction.outTransactions[0]["amount"]), shape="oval")
        G.edge("ROOT", transaction.id)
        G.edge(transaction.id, tempID)
    else:
        for inItem in transaction.inTransactions:
            inTxID = inItem["inTransactionID"]
            inTxIndex = inItem["inTransactionIndex"]
            G.edge(inTxID + "-" + str(inTxIndex), transaction.id)
        for index, outItem in enumerate(transaction.outTransactions):
            G.node(transaction.id + "-" + str(index), str(outItem["amount"]), shape="oval")
            G.edge(transaction.id, transaction.id + "-" + str(index))



def showGraph(G):
    G.save("./Storage/visualizeLedger.gv")
    print(os.getcwd())
    G.render("/Storage/visualizeLedger.gv")
    G.view()


