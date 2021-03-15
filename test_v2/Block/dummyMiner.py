"""
This File defines a dummy miner function, which is only for test purpose.
"""


def dummyMine(blockObj) -> int:
    diff = blockObj.difficulty
    nounce = 0
    while blockObj.hexHash()[:diff] != "0" * diff:
        nounce += 1
        blockObj.nounce = nounce
    return nounce
