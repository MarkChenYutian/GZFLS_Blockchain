"""
This File contains the OP_Factory class, which will load the script from .opscript file, fill in the Parameters, and then
return a list of String as the OP_Script.
"""

class OP_Factory:
    def __init__(self):
        pass

    def create(self, OP_Type, *parameters):
        """
        :param OP_Type: The OP Type, currently only accept tx2pbh
        :param parameters: several parameters that will feed in the template to create an OP Script.
        :return: a list of strings, as 'OP Script'
        """

        OP_script = []
        if OP_Type == 'tx2pbh':
            with open("./OP_Script/tx2pubkeyhash.opscript","r") as OP_Template:
                OP_lines = OP_Template.read().strip().split('\n')
            for line in OP_lines:
                if line[:11] == "OP_TEMPLATE":
                    index = int(line.split(" ")[-1])
                    OP_script.append(parameters[index])     # Load Parameters into OP Template
                else:
                    OP_script.append(line)                  # Load normal line into OP Template
        return OP_script