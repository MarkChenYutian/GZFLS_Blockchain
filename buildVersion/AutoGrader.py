"""
Since some of you tried to PASS the Autograder test by identifying test case directly instead of finishing an implementation,
we will only provide Obfuscated Python File for Autograder.py from then on.

We know that giving such autograder will makes it harder for you to debug the program, but we have to do so.
"""

import datetime
import util
from Transaction import *
from Ledger import *
from Block import *
from RSA_func import generateMyKeys
from MerkelTree import MerkelTree

class AutoGrader:
    def __init__(self):
        self.version = "1.3.0"

    @staticmethod
    def getKeys():
        private,public,n = generateMyKeys()
        return [(private,n),(public,n)]

    def run(self):
        print("Autograder Start @ {}\nV {} By Mark \nIf you have any problem with Autograder, "
              "ask on the WeChat group directly\n--------------------------".format(datetime.datetime.now(), self.version))
        print("Setting Test Environment ...", end="", flush=False)

        WARNING_Count = 0

        ################ Setup Basic Tests ##################

        PASS = "\033[1;32m[Pass]  |"
        FATAL = "\033[1;31m[Fatal] |"
        WARNING = "\033[1;33m[Warn]  |"
        INFO = "\033[1;34m[Info]  |"

        print("\rTest Case 1. Create Ledger and RSA_keys to setup test environment")
        try:
            test_Ledger = Ledger()
            print(PASS + "\033[0;;m Ledger is created.")
        except Exception as e:
            print(FATAL + "\033[0;;m We failed to create a Ledger Object. \nAutograder Terminated.")
            raise e

        names = ["A", "B", "C", "D", "E"]
        try:
            RSA_keys = {name: self.getKeys() for name in names}
            print(PASS + "\033[0;;m RSA Keys Created.")
        except Exception as e:
            print(FATAL + "\033[0;;m We failed to create RSA Keys. Do NOT modify the given RSA_func.py file. "
                          "Autograder Terminated.\n"
                          "Detailed Exception Showed Above.")
            raise e

        try:
            balance = test_Ledger.getBalanceStat()
            assert str(type(balance)) == "<class 'dict'>"
            print(PASS + "\033[0;;m Ledger.getBalanceStat() Function returns a dictionary.")
        except AssertionError:
            WARNING_Count += 1
            print(WARNING + "\033[0;;m Ledger.getBalanceStat() function does NOT return a dictionary, instead, it "
                            "returns an object with type {}. Since we need this function for test cases below, "
                            "the cases below may raise Exceptions due to this. \nAutograder will continue to run.".format(type(balance)))
        except Exception as e:
            print(FATAL + "\033[0;;m Exception raised when running Ledger.getBalanceStat function.\n"
                          "Autograder Terminated.")
            raise e

        try:
            print(INFO + "\033[0;;m Testing Signature & Decryption Process ...", flush=True, end="")
            msg = Transaction(test_Ledger, 50, (0, 0), (0, 0), RSA_keys["A"][1], isCoinBase=True)
            signature = signSignature(msg, RSA_keys["A"][1])
            decrypt_result = decryptSignature(signature, RSA_keys["A"][0])
            assert decrypt_result == msg.getTxn()
            print("\r"+PASS+"\033[0;;m signSignature & decryptSignature functions are working as expected.")
        except AssertionError:
            WARNING_Count += 1
            print("\r"+WARNING+"\033[0;;m Result of Signature decryption doesn't match the original message's hash.\n"
                               "Incorrect implementation of Signature function may cause problems in test cases below.\n"
                               "Autograder will continue to run.")
        except Exception as e:
            print("\r" + FATAL + "\033[0;;m Unexpected Exception is raised when signSignature & decryptSignature is called.\n"
                                 "Autograder Terminated")
            raise e


        #####################################################

        ############# Transaction from COINBASE ##############
        print("Test Case 2. Creating Simple Transactions between Users")
        try:
            for name in names:
                newTransaction = Transaction(test_Ledger, 50, (0, 0), (0, 0), RSA_keys[name][1], isCoinBase=True)
                test_Ledger.addTransaction(newTransaction)

            if len(test_Ledger) != len(names):
                WARNING_Count += 1
                print(
                    WARNING + "\033[0;;m Some (All) of the Transactions from COINBASE failed to add into the ledger. "
                              "This may cause by improper validation in Ledger.addTransaction. \nAutograder will "
                              "continue to run.")
            else:
                print(PASS + "\033[0;;m Transaction from COINBASE is accepted.")
        except Exception as e:
            print(FATAL + "\033[0;;m Exception raised when adding transactions from COINBASE to the ledger. "
                          "Autograder Terminated.\n"
                          "Detailed Exception is raised Above.")
            raise e

        ######################################################

        ############ Transactions between Users ##############

        try:
            print(INFO + "\033[0;;m Creating Transactions between people ...", end="", flush=True)
            # A -- 40 --> B
            newTransaction = Transaction(test_Ledger, 40, RSA_keys["A"][1], RSA_keys["A"][0], RSA_keys["B"][1])
            test_Ledger.addTransaction(newTransaction)

            # B -- 10 --> C
            newTransaction = Transaction(test_Ledger, 10, RSA_keys["B"][1], RSA_keys["B"][0], RSA_keys["C"][1])
            test_Ledger.addTransaction(newTransaction)

            # C -- 30 --> A
            newTransaction = Transaction(test_Ledger, 30, RSA_keys["C"][1], RSA_keys["C"][0], RSA_keys["A"][1])
            test_Ledger.addTransaction(newTransaction)

            # B -- 20 --> D
            newTransaction = Transaction(test_Ledger, 20, RSA_keys["B"][1], RSA_keys["B"][0], RSA_keys["D"][1])
            test_Ledger.addTransaction(newTransaction)

            assert len(set(test_Ledger.getBalanceStat().values()) - {40, 60, 30, 70, 50}) == 0
            print("\r"+PASS + "\033[0;;m Basic Transaction between Peoples are processed correctly.")
        except Exception as e:
            print("\r"+FATAL + "\033[0;;m The valid transactions between people are blocked by the ledger. Autograder Terminated.\n"
                          "Detailed Exceptions is raised.")
            raise e

        ######################################################

        ########## Malicious Transaction Test ################

        print("Test Case 3. Malicious Transaction Test")

        # CASE 1 | A --- [10 x] 20 ---> B

        try:
            print(INFO + "\033[0;;m Creating a Malicious Transaction A --- [10 x] 20 ---> B ...", end="", flush=True)
            newTransaction = Transaction(test_Ledger, 10, RSA_keys["A"][1], RSA_keys["A"][0], RSA_keys["B"][1])
            for index in range(len(newTransaction.outTransaction)):
                if newTransaction.outTransaction[index][0] == 10:
                    newTransaction.outTransaction[index][0] = 20
            test_Ledger.addTransaction(newTransaction)
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger accept the invalid transaction OR didn't raise any exception for an "
                            "invalid input. Check your implementation on addTransaction(...). "
                            "Remember to raise TransactionNotBalanceError when the input transaction is not balanced.\n"
                            "Autograder will continue to run.")
        except TranactionNotBalanceError:
            print("\r" + PASS + "\033[0;;m Ledger detect the modified Transaction and raise TransactionNotBalanceError as expected.")
        except BlockchainError as e:
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger detect the modified Transaction but raise {} instead of TransactionNotBalanceError.".format(type(e)))
        except Exception as e:
            print("\r" + FATAL + "\033[0;;m When we are trying to add a malicious modified transaction into the ledger, "
                          "Unexpected Exception is raised. Check whether your program raise the "
                          "TransactionNotBalanceError or other exceptions.\n"
                          "Autograder Terminated.\n"
                          "Detailed Exception is raised.")
            raise e

        # CASE 2 | A(E) - - - 20 ---> B

        try:
            print(INFO + "\033[0;;m Creating a Malicious Transaction A(E) - - - 20 ---> B ...", end="", flush=True)
            newTransaction = Transaction(test_Ledger, 10, RSA_keys["E"][1], RSA_keys["A"][0], RSA_keys["B"][1])
            test_Ledger.addTransaction(newTransaction)
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger accept the invalid transaction that use E's money as input "
                                    "but created by A.\n"
                                    "Autograder will continue to run.")
        except TransactionSignatureError:
            print("\r" + PASS + "\033[0;;m Ledger detect the signature created by A is invalid and raise TransactionSignatureError as expected.")
        except BlockchainError as e:
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger detect the modified Transaction but raise {} instead of TransactionSignatureError.".format(type(e)))
        except Exception as e:
            print("\r" + FATAL + "\033[0;;m When we are trying to add a malicious modified transaction into the ledger, "
                          "Unexpected Exception is raised. Check whether your program raise the "
                          "TransactionSignatureError or other exceptions.\n"
                          "Autograder Terminated.\n"
                          "Detailed Exception is raised.")
            raise e

        # CASE 3 | A --- 20 + [create from nowhere] 10 ---> B

        try:
            print(INFO + "\033[0;;m Creating a Malicious Transaction A --- 20 + [create from nowhere] 10 ---> B ...", end="", flush=True)
            newTransaction = Transaction(test_Ledger, 10, RSA_keys["A"][1], RSA_keys["A"][0], RSA_keys["B"][1])
            newTransaction.addInputTransaction(11090429, 0, (2003, 2002, 2000, 1999))
            test_Ledger.addTransaction(newTransaction)
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger accept the invalid transaction that use a fake (and not-exist) "
                                    "inTransaction entry created by A.\n"
                                    "Autograder will continue to run.")
        except TransactionInNotExist:
            print("\r" + PASS + "\033[0;;m Ledger detect that the input transaction of the new transaction is invalid"
                                " and raise TransactionInNotExist as expected.")
        except BlockchainError as e:
            WARNING_Count += 1
            print("\r" + WARNING + "\033[0;;m Ledger detect the modified Transaction but raise {} instead of TransactionInNotExist.".format(type(e)))
        except Exception as e:
            print("\r" + FATAL + "\033[0;;m When we are trying to add a malicious modified transaction into the ledger, "
                          "Unexpected Exception is raised. Check whether your program raise the "
                          "TransactionInNotExist or other exceptions.\n"
                          "Autograder Terminated.\n"
                          "Detailed Exception is raised.")
            raise e

        # CASE 4 | Check whether the attempt to add invalid transactions into ledger will lead to change on balance

        try:
            assert len(set(test_Ledger.getBalanceStat().values()) - {40, 60, 30, 70, 50}) == 0
            print(PASS + "\033[0;;m Attempt to add invalid transactions does NOT change the balance in ledger.")
        except AssertionError as e:
            WARNING_Count += 1
            print(WARNING + "\033[0;;m Adding invalid transactions into the ledger cause the ledger balance change.\n"\
                            "Probably because - 1. The invalid transaction in previous test case is accepted by the ledger\n"\
                            "2. The sequence to modify the 'isUsed' state in ledger and validate input transaction is incorrect.\n"\
                            "Autograder will continue to run.")
        except Exception as e:
            print(FATAL + "\033[0;;m Fail to check balance of ledger after attempt to add invalid transactions into the ledger. Detailed exceptions are raised.\n"
            "Autograder terminated.")
            raise e
        ####################### Block Test ########################
        print("Test Case 4. Block Test")

        DIFFICULTY = 5

        # Create More Transactions to test the block
        for _ in range(2):
            for name in names:
                newTransaction = Transaction(test_Ledger,25,(0,0),(0,0),RSA_keys [name] [1],isCoinBase=True)
                test_Ledger.addTransaction(newTransaction)

        # Trivial Block Test
        print(INFO + "\033[0;;m Creating a trivial block with difficulty = {}...".format(DIFFICULTY), end="")
        try:
            testTxs = [test_Ledger[tx] for tx in test_Ledger]
            testTxs = testTxs[:16]
            testBlock1 = Block("f" * 64, DIFFICULTY, 0, testTxs)
            print("\r" + PASS + "\033[0;;m Create a single block successfully")
        except Exception as e:
            print("\r" + FATAL + "\033[0;;m Failed to create a new block.\nAutograder Terminated.")
            raise e

        # Test New Block Hash Value
        try:
            testBlock1Hash = util.hashObject(testBlock1)
            if testBlock1Hash[:DIFFICULTY] == "0" * DIFFICULTY:
                print(PASS + "\033[0;;m The created block pass the Difficulty Test with Hash value {}".format(testBlock1Hash))
        except NameError:
            WARNING_Count += 1
            print(WARNING + "\033[0;;m Since the Block is not created in prev case, Autograder will skip this case.\n"
                            "Autograder Continue to Run.")
        except Exception as e:
            print(FATAL + "\033[0;;m Unexpected Exception Raised. \nAutograder Terminated.")
            raise e

        # Test Merkel Tree
        try:
            testTree = MerkelTree(["tx1", "tx2", "tx3", "tx4", "tx5", "tx6", "tx7", "tx8"])

            assert testTree.root == 'a0e4f2fc684c076060cb332359794de449eca07b281fc6b2da02e76e9f9ca6db'
            print(PASS + "\033[0;;m Merkel Tree Root is correct.")
        except AssertionError:
            WARNING_Count += 1
            print(WARNING + "\033[0;;m Merkel Tree Root is calculated without exception, but is different from expected result.\n"
                            "Your Merkel Tree root is {}\nAutograder will continue to run.".format(testTree.root))
        except Exception as e:
            print(FATAL + "\033[0;;m Unexpected Exception Raised. \nAutograder Terminated.")
            raise e

        ######################################################

        print("\n--------- Autograder Terminated without Exception -----------")

        if WARNING_Count == 0:
            print("\n\n\033[32mCongratulation! You passed All the tests with 0 Warning and 0 Error.\033[0;;m \n\n")
        else:
            print("\n\n\033[33mThough the implementation does NOT have FATAL ERROR, there is (are) {} Warning(s). "
                  "Running through the autograder does NOT mean your implementation is correct since there are Warnings."
                  "You should debug on your implementation to solve all Warnings. File Ledger.txt is exported in the working directory to help you debug.\033[0;;m \n\n".format(WARNING_Count))

        if (input("Press 'y' if you want to export the Ledger in Ledger.txt file: ").lower() == "y"):
            test_Ledger.exportFile()

if __name__ == '__main__':
    test = AutoGrader()
    test.run()
