import ast, inspect
from test2 import test
from test1 import main

print(ast.dump(ast.parse(inspect.getsource(test))))
print()
print(ast.dump(ast.parse(inspect.getsource(main))))

def removeVarName(astString):
    pass