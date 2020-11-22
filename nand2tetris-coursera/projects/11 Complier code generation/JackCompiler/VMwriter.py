# References:
# https://github.com/itayabu/nand2tetris/tree/master/ex11
# https://www.cs.huji.ac.il/course/2002/nand2tet/docs/ch_11_compiler_II.pdf

class VMWriter:
    """
    This class writes VM commands into a file. It encapsulates the VM command syntax.
    """

    def __init__(self, output):
        """
        Creates a new file and prepares it for writing VM commands
        :param output file/stream:
        """
        self.output_file = open(output, "w")

    def write_push(self, segment, index):
        """
        Writes a VM push command e.g. push constant 5
        Segment types pdf pg 97 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
        :param segment (constant, argument, local, static, this, that, pointer, temp):
        :param index (int):
        :return:
        """
        self.output_file.write("push " + segment + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        """
        Writes a VM pop command e.g. pop local 0
        :param segment (constant, argument, local, static, this, that, pointer, temp):
        :param index (int):
        :return:
        """
        self.output_file.write("pop " + segment + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        Arithmetic types pdf pg 94 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
        :param command (add, sub, neg, eq, gt, lt, and, or, not) :
        :return:
        """
        self.output_file.write(command + "\n")

    def write_label(self, label):
        """
        Writes a VM label command e.g. label MAIN_LOOP_START
        :param label:
        :return:
        """
        self.output_file.write("label " + label + "\n")

    def write_goto(self, label):
        """
        Writes a VM goto label command e.g. goto END_PROGRAM
        :param label:
        :return:
        """
        self.output_file.write("goto " + label + "\n")

    def write_if(self, label):
        """
        Writes a VM if-goto label command e.g. if-goto COMPUTE_ELEMENT
        :param label:
        :return:
        """
        self.output_file.write("if-goto " + label + "\n")

    def write_call(self, name, nArgs):
        """
        Writes a VM call command with number of args after e.g. call factorial 1
        :param name:
        :param nArgs:
        :return:
        """
        self.output_file.write("call " + name + " " + str(nArgs) + "\n")

    def write_function(self, name, nLocals):
        """
        Writes a VM function command with number of local args (vars) after e.g. function main 0
        :param name:
        :param nLocals:
        :return:
        """
        self.output_file.write("function " + name + " " + str(nLocals) + "\n")

    def write_return(self):
        """
        Writes a VM return command
        :return:
        """
        self.output_file.write("return\n")

    def close(self):
        """
        closes the output file
        :return:
        """
        self.output_file.close()