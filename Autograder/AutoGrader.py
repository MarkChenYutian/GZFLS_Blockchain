import json
import base64

class AutoGrader:
    """
        Autograder that can run cases seperately with flexibility
        Version 2.0.0 By Mark
    """
    def __init__(self, **kwargs):
        with open('config.json', 'r') as config:
            self.cfg = json.load(config)

        if "q" in kwargs and kwargs["q"] < self.cfg['NumCase']:
            self.case = kwargs["q"]
        else:
            self.case = 0
    
    def run(self):
        passNum, warnNum, errorNum = 0, 0, 0
        for case in range(self.case, self.cfg['NumCase']):
            try:
                print("\nCASE {0} - {1}\n----------------------------".format(case, self.cfg['CaseDescription'][str(case)]))
            except:
                print("\nCASE {0}\n----------------------------")
            
            newPass, newWarn, newError = self.runTask(task=case)

            passNum += newPass
            warnNum += newWarn
            errorNum += newError

            print("[PASS - {0} | WARN - {1} | ERROR - {2}]\n----------------------------\n".format(newPass, newWarn, newError))
        print("----------------------------\n")
            
    
    def runTask(self, task=1):
        with open("./test/{}.test".format(task), "r") as taskFile:
            task = base64.decode(taskFile.read())
        print(taskFile)
        return 2, 3, 5
        

if __name__ == "__main__":
    testObj = AutoGrader(q=3)
    testObj.run()