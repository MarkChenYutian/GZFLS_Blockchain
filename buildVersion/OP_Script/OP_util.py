"""
This File has written functions that helps you to write a RSA encryption process.

All the functions are tested and works properly

############################################################
###### YOU SHOULD NOT CHANGE THE CONTENT OF THIS FILE ######
############################################################
"""

import pickle

def encryptInt(message: int, publicKey: int, n: int):
    assert message < n, "The input message is bigger than the selected n. This will lead to incorrect result" \
                        " even if you have correct implementation. Change to a smaller message or a bigger n."
    """ WRITE YOUR CODE BELOW """

    encryptMsg = (message ** publicKey) % n

    """ WRITE YOUR CODE ABOVE """
    return encryptMsg

def decryptInt(message: int, privateKey: int, n: int):
    assert message < n, "The input message is bigger than the selected n. This will lead to incorrect result" \
                        " even if you have correct implementation. Change to a smaller message or a bigger n."
    """ WRITE YOUR CODE BELOW """

    decryptMsg = (message ** privateKey) % n

    """ WRITE YOUR CODE ABOVE """
    return decryptMsg

################################# YOU SHOULD NOT MODIFY FUNCTIONS BELOW ###################################

def encryptObject(msg_object: object, publicKey: int, n: int):
    return [encryptInt(token, publicKey, n) for token in longMsgIterator(msg_object)]

def decryptObject(msg_list: list, privateKey: int, n: int):
    token_combiner = tokensCombiner()
    for token in msg_list: token_combiner.addToken(token, privateKey, n)
    return convertIntegerToObject(token_combiner.getNum())


############################# YOU SHOULD NOT READ & MODIFY FUNCTIONS BELOW ################################

def convertObjectToInteger(obj: object):
    return int.from_bytes(pickle.dumps(obj), byteorder="little")

def convertIntegerToObject(integer: int):
    max_len, curr_len = 1024 ** 3, 64
    while curr_len < max_len:
        try:
            resObject = pickle.loads(integer.to_bytes(curr_len, byteorder='little'))
            break
        except OverflowError as e:
            curr_len = curr_len ** 2
    return resObject


class longMsgIterator:
    def __init__(self, msg: object):
        self.message = msg
        self.msgInt = convertObjectToInteger(msg)

    def __iter__(self): return self

    def __next__(self):
        if self.msgInt == 0: raise StopIteration
        token = self.msgInt % 100000
        self.msgInt -= token
        if self.msgInt > 100000: self.msgInt = self.msgInt // 100000
        return token

class tokensCombiner:
    def __init__(self):
        self.num = 0
        self.pow = 0
    def addToken(self, token, privateKey:int, n:int, token_size=5):
        self.num += decryptInt(token, privateKey=privateKey, n=n) * (10 ** self.pow)
        self.pow += token_size
    def getNum(self): return self.num