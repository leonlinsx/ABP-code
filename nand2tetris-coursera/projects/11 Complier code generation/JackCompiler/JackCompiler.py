# References
# https://github.com/itayabu/nand2tetris/tree/master/ex10
# https://github.com/saikumarm4/Nand2Tetris/blob/master/10/Lexical.py
# https://github.com/kronosapiens/nand2tetris/blob/master/projects/10/JackAnalyzer.py

import sys
import os
import CompilationEngine

class JackCompiler:
    """
    For each source Jack file, the compiler creates a JackTokenizer object in order to process the input.
    And it also creates an output vm file.

    once we do this set up the compiler can go on to use symbol table, compilation engine, and VM Writer
    in order to generate the VM code and write it into the output file, the VM file
    i.e. compiler is the main class to call other classes

    The proposed implementation is based on morphing the syntax analyzer built in the previous project
    into a the full-scale compiler.
    In particular, we propose to gradually replace the software modules that generate XML output
    with software modules that generate VM code.
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
                    comp = CompilationEngine.CompilationEngine(user_input + file, user_input + file_name + ".vm")
                    comp.compile_class()

        # if input is a single file, can just parse it
        elif os.path.isfile(user_input):
            # temporarily remove the extension so we can add .jack and .xml at the end
            user_input = user_input.split(".")[0]
            comp = CompilationEngine.CompilationEngine(user_input + ".jack", user_input + ".vm")
            comp.compile_class()

        else:
            raise Exception("Input is invalid, try again")


if __name__ == "__main__":

    user_input = sys.argv[1]
    JackCompiler(user_input)