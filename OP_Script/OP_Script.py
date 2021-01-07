"""
The OP_Script class is the object that will load the OP Script and execute it.
I will introduce the grammar of OP Script here.
There are three types of things in an OP Script File - Command, Value, and Comment.
* Command always start with "OP"
* Comment always start with "#"
* If a line is not command or comment, it will be treated as a value - push in the the stack directly as a string.

Note that Empty line is NOT allowed. (Or an empty string will be pushed into the stack.)

When you create an OP_Script Object, you will load the script from a file. To run this script, use the 'run(*args)' 
function of the OP_Script to execute the script line by line.

* How to Load parameters into the Stack?
    When we are using the OP_Script.run() function, we can pass multiple parameters into it.
    The first parameter will have an index of 0, second will have an index of 1, ...
    When you want to push first parameter into the stack, use OP_IN 0. When executing OP_IN 0, the first 
    parameter will be pushed into the stack.
"""
import hashlib
import pickle
from OP_Exception import *
from OP_util import *

def OP_EQUAL(stack):
    if stack.pop() == stack.pop(): stack.append(1)
    else: stack.append(0)

def OP_VERIFY(stack):
    if stack.pop() == 0: raise OP_Verify_Fail()

def OP_RETURN(stack):
    raise OP_Verify_Fail()

def OP_SHA256(stack):
    stack.append(int(hashlib.sha256(pickle.dumps(stack.pop())).hexdigest(), 16))

def OP_CHECKSIG(stack):
    """
    stack = [signature, publickey, result]
    if decrypt(signature, publickey) == result - push 1
    else - push 0
    """
    signature = stack.pop()
    assert type(signature) == tuple, "OP_CHECKSIG Function Expect to receive a tuple of tokens as signature, but get {}".format(type(signature))
    pubKey = stack.pop()
    assert type(signature) == tuple, "OP_CHECKSIG Function Expect to receive a tuple as public key, but get {}".format(type(pubKey))
    try:
        msg = decryptObject(signature, *pubKey)
    except:
        raise OP_Runtime_Exception("OP_CHECKSIG Fail: decryptObject(signature, *pubKey) failed to decrypt signature.")
    stack.append(msg)
    OP_EQUAL(stack)

OP_Code = dict()
OP_Code["OP_ADD"] = lambda stack: stack.append(stack.pop() + stack.pop())
OP_Code["OP_DUP"] = lambda stack: stack.append(stack[-1])
OP_Code["OP_PRINT"] = lambda stack: print("["+"\n".join(list(map(str, stack[::-1]))) + "]")    # This is used to help you debug your OP Script
OP_Code["OP_CONVHEX"] = lambda stack: stack.append(int(stack.pop(), 16))
OP_Code["OP_CONVDEC"] = lambda stack: stack.append(hex(stack.pop()))
OP_Code["OP_POP"] = lambda stack: stack.pop()
OP_Code["OP_EQUAL"] = OP_EQUAL
OP_Code["OP_VERIFY"] = OP_VERIFY
OP_Code["OP_RETURN"] = OP_RETURN
OP_Code["OP_SHA256"] = OP_SHA256
OP_Code["OP_CHECKSIG"] = OP_CHECKSIG


class OP_Script:
    def __init__(self, path):
        self.version = "1.0.0"
        self.stack = []
        self.para = []
        self.script = None
        self.currLine = 0

        with open(path, "r") as scriptFile:
            self.script = self.parseScript(scriptFile.read())

    @staticmethod
    def parseScript(script: str):
        code_lines = script.split("\n")
        return code_lines

    def run(self, *args, debug=False):
        self.para = args
        while self.currLine < len(self.script):
            self._exec(self.script[self.currLine])
            if debug and self.script[self.currLine][0] != "#":
                print("Line {} | {}".format(self.currLine, self.script[self.currLine]))
                OP_Code["OP_PRINT"](self.stack)
                print()
            self.currLine += 1
        # for line in self.script: self._exec(line)
        print("OP_EXEC FINISH")
        return True
    
    def loadPara(self, paraIndex):
        try:
            self.stack.append(self.para[paraIndex])
        except IndexError:
            raise OP_Value_Exception("The line OP_IN_{0} requires #{0} parameter, but there are only {1} parameters given.".format(paraIndex, len(self.para)))

    def _exec(self, line):
        if len(self.stack) == 100: print("\033[1;33mOP_SCRIPT WARNING: Stack size exceeds 100, are you making an Infinite Loop?")
        elif len(self.stack) > 500: raise OverflowError("Stack size over 500. OP_Script Terminated.")

        if line[:2] != "OP" and line[:1] != "#":
            try:self.stack.append(eval(line))
            except: self.stack.append(line)
        elif line[:6] == "OP_IN ":
            paraNum = int(line[6:])
            self.loadPara(paraNum)
        elif line[:7] == "OP_JUMP":
            if self.stack.pop() == 0:
                print("OP_JUMP TO {}".format(line[12:]))
                self.currLine = int(line[12:]) - 1
        elif line[:2] == "OP":
            try:
                OP_Code[line](self.stack)
            except KeyError:
                raise OP_Unexpect_Line_Exception(line)


if __name__ == '__main__':
    # msg = hashlib.sha3_256("testMsg".encode('ascii')).hexdigest()
    # msg = 4be7dceb544d12d1816034f664a13762bb0d0dd3b4f2c2aed78ef02552ddf17a
    a = ["testMsg"]
    msg = OP_Code['OP_SHA256'](a)
    private, public, n = (142729, 59513, 351073)
    signature = encryptObject(a[-1], private, n)

    test = OP_Script("TX2PUBKEY.opscript")
    # test.run(tuple(signature), (public, n))
    test.run(10, 13, 23)
