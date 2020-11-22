# References
# https://github.com/itayabu/nand2tetris/tree/master/ex10
# https://github.com/saikumarm4/Nand2Tetris/blob/master/10/Lexical.py
# https://github.com/kronosapiens/nand2tetris/blob/master/projects/10/JackAnalyzer.py

import sys
import os
import JackCompilationEngine

class JackAnalyzer:
    """
    The syntax analyzer takes a source text file and attempts to match it on the language grammar
    If successful, it can generate a parse tree in some structured format, e.g. XML.
    """

    def __init__(self, user_input):
        self.main(user_input)

    def main(self, user_input):
        # Return True if path is an existing directory i.e. if source_file is existing directory
        if os.path.isdir(user_input):
            # add / so easier to concatenate later
            if not user_input.endswith("/"):
                user_input += "/"
            # returns a list containing the names of the entries in the directory given by path
            files = os.listdir(user_input)
            # if the input is a directory, want to check every file in there and convert all .jack files
            for file in files:
                if file.endswith(".jack"):
                    file_name = file.split(".")[0]  # strip the extension
                    comp = JackCompilationEngine.JackCompilationEngine(user_input + file, user_input + file_name + ".xml")
                    comp.compile_class()

        # if input is a single file, can just parse it
        elif os.path.isfile(user_input):
            # temporarily remove the extension so we can add .jack and .xml at the end
            user_input = user_input.split(".")[0]
            comp = JackCompilationEngine.JackCompilationEngine(user_input + ".jack", user_input + ".xml")
            comp.compile_class()

        else:
            raise Exception("Input is invalid, try again")


if __name__ == "__main__":

    user_input = sys.argv[1]
    JackAnalyzer(user_input)