import hashlib
import pickle
from OP_Script.OP_Exception import *

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
    

OP_Code = dict()
OP_Code["OP_ADD"] = lambda stack: stack.append(stack.pop() + stack.pop())
OP_Code["OP_DUP"] = lambda stack: stack.append(stack[-1])
OP_Code["OP_PRINT"] = lambda stack: print(stack)    # This is used to help you debug your OP Script
OP_Code["OP_EQUAL"] = OP_EQUAL
OP_Code["OP_VERIFY"] = OP_VERIFY
OP_Code["OP_RETURN"] = OP_RETURN
OP_Code["OP_SHA256"] = OP_SHA256


class OP_Script:
    def __init__(self, path):
        self.version = "1.0.0"
        self.stack = []
        self.script = None
        with open(path, "r") as scriptFile:
            self.script = self.parseScript(scriptFile.read())

    def parseScript(self, script: str):
        code_lines = script.split("\n")
        return code_lines

    def run(self, *args):
        for arg in args: self._addConst(arg)
        for line in self.script: self._exec(line)

    def _addConst(self, line):
        try:
            self.stack.append(int(line))
        except ValueError:
            try:
                self.stack.append(int(line,16))
            except:
                raise OP_Value_Exception()

    def _exec(self, line):
        if line[:2] != "OP" and line[:1] != "#":
            self._addConst(line)
        elif line[:2] == "OP":
            try:
                OP_Code[line](self.stack)
            except KeyError:
                raise OP_Unexpect_Line_Exception(line)


if __name__ == '__main__':
    test = OP_Script("TX2PUBKEY.opscript")
    test.run("ffffff", "efefef")
