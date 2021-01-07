class OP_Exception(Exception):
    def __init__(self, msg):
        super(OP_Exception, self).__init__(msg)

class OP_Value_Exception(OP_Exception):
    def __init__(self, msg="OP Script only accept Dec or Hex input as constant"):
        super(OP_Value_Exception, self).__init__(msg)

class OP_Unexpect_Line_Exception(OP_Exception):
    def __init__(self, line):
        super(OP_Unexpect_Line_Exception, self).__init__("OP Script receives unrecognized line: {}".format(line))

class OP_Verify_Fail(OP_Exception):
    def __init__(self):
        super(OP_Verify_Fail, self).__init__("OP_VERIFY find the top of stack is 0.")

class OP_Runtime_Exception(OP_Exception):
    def __init__(self, msg="OP Script raise Exception while running. Try add OP_PRINT in your script to debug."):
        super(OP_Runtime_Exception, self).__init__(msg)