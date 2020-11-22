'''
nand2tetris project 7, building a VM translator https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
goal is to build smth that can translate VM language stack arithmetic, push/pop commands into assembly
e.g. from push constant 510 to // push constant 510 @510 D=A

will have:
Parser to parse each VM command into lexical elements
CodeWriter to write assembly code that implements parsed command
Main to drive the process

input .vm file, output .asm file
references:
https://github.com/kronosapiens/nand2tetris/blob/master/projects/07/VMtranslator.py
https://github.com/bgx/nand2tetris/blob/master/src/project07/vmtranslator/vmtranslator.py
https://github.com/mtrazzi/nand2tetris/blob/master/VM_translator/arithmetic.py

bug http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Help-w-Fill-asm-td4026849.html#a4026851
'''

import os
import sys

# Reads a VM command, parses the command into its lexical
# components, and provides convenient access to these components
# Ignores white space and comments
class Parser:

    COMMENT = "//"

    def __init__(self, vm_filename):
        self.vm_filename = vm_filename
        self.vm = open(vm_filename, "r")

        self.curr_instruction = None
        self.next_instruction = None
        self.end_of_file = False
        self.initialise_file()
        # based on the VM language in the course https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view pg 85
        # arithmetic, memory access, branching, function commands
        self.commands_dict = {
            "add": "C_ARITHMETIC",
            "sub": "C_ARITHMETIC",
            "neg": "C_ARITHMETIC",
             "eq": "C_ARITHMETIC",
             "gt": "C_ARITHMETIC",
             "lt": "C_ARITHMETIC",
            "and": "C_ARITHMETIC",
             "or": "C_ARITHMETIC",
            "not": "C_ARITHMETIC",
            "pop": "C_POP",
           "push": "C_PUSH",
          "label": "C_LABEL",
           "goto": "C_GOTO",
        "if-goto": "C_IF",
       "function": "C_FUNCTION",
           "call": "C_CALL",
         "return": "C_RETURN",
        }

    #######
    ### API
    # reads next command from input, makes it curr command
    # should only be called if has_more_commands is true
    def advance(self):
        self.curr_instruction = self.next_instruction
        # not passing line as arg, so it'll default to None and read next line
        self.load_next_instruction()

    # returns boolean of whether more commands in input
    # use @property to define a method that is accessible like an attribute
    @property
    def has_more_commands(self):
        return not self.end_of_file

    # returns constant representing the type of current command
    @property
    def command_type(self):
        # index 0 is the command, have to convert lower just in case
        return self.commands_dict.get(self.curr_instruction[0].lower())

    # returns first arg of current command (constant, local etc) as string
    # for C_ARITHMETIC, command itself is returned (add, sub etc)
    # should not be called if curr command is C_RETURN
    # reminder the format of a command is like "push constant 510"
    @property
    def arg1(self):
        if self.command_type == "C_ARITHMETIC":
            return self.argn(0)
        return self.argn(1)

    # returns second arg of current command (address, number etc) as int
    # should only be called if curr command is C_PUSH, C_POP, C_FUNCTION, C_CALL
    @property
    def arg2(self):
        return self.argn(2)

    ### END API
    ###########

    def initialise_file(self):
        # go to start of file
        # https://www.geeksforgeeks.org/python-seek-function/
        self.vm.seek(0, 0)
        self.load_next_instruction()
        
        # below 8 lines deprecated given next load_next()
        # start reading until get to first instruction
        # line = self.vm.readline().strip()
        # while not self.is_instruction(line):
        #     line = self.vm.readline().strip()
        # don't have to catch any comments here since is_instruction does so
        # line = raw_line.split(Parser.COMMENT)[0].strip()
        # overriding default line None with first line
        # self.load_next_instruction(line)

    def is_instruction(self, line):
        # returns boolean if is instruction, non empty, not comment
        # we've already stripped it, so won't be spaces before //
        return line and line[:2] != Parser.COMMENT

    def load_next_instruction(self, line=None):
        loaded = False
        while not loaded and not self.end_of_file:
            # tell returns current position of file pointer https://www.tutorialspoint.com/python/file_tell.htm
            tell = self.vm.tell()
            line = self.vm.readline().strip()
            if self.is_instruction(line):
                self.next_instruction = line.split(Parser.COMMENT)[0].strip().split()
                loaded = True
            # if position didn't change, it's end of file
            if tell == self.vm.tell():
                self.end_of_file = True

        # below 5 lines deprecated
        # sets the next_instruction variable
        # we default line to None so that it'll usually readline, unless we pass a lin
        # only time we pass a line is in initialise_file
        # line = line if line is not None else self.vm.readline().strip()
        # self.next_instruction = line.split(Parser.COMMENT)[0].strip().split()

    def argn(self, n):
        # instructions are at least one word long, if not that's an empty line
        # returns the nth index of current instruction
        # want a flexible function since instructions can be diff lengths
        if len(self.curr_instruction) >= n + 1:
            return self.curr_instruction[n]
        else:
            return None

    def close(self):
        self.vm.close()

# Generates assembly code from the parsed VM command:
class CodeWriter:

    def __init__(self, asm_filename):
        self.asm = open(asm_filename, "w")
        self.curr_file = None
        # easier code debugging
        self.line_count = 0
        # for labels
        self.bool_count = 0
        # for function calls
        self.call_count = 0
        # need to set SP at start; later tester doesn't do that
        self.write("@256")
        self.write("D=A")
        self.write("@SP")
        self.write("M=D")
        self.write_call("Sys.init", 0)
        # VM mapping pdf pg 97 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
        self.address_dict = {
                "local": "LCL", # RAM[1]
             "argument": "ARG", # RAM[2]
                 "this": "THIS", # RAM[3]
                 "that": "THAT", # RAM[4]
              "pointer": 3, # fixed segment on RAM 3-4; pointer 0 THIS, pointer 1 THAT
                 "temp": 5,  # fixed segment on RAM 5-12
                # RAM 13-15 is general purpose registers
               "static": 16 # from RAM 16-255; stack starts 256-2047
        }

    #######
    ### API
    # need a way to get filename for the static variables
    # e.g. static 5 in Foo.vm translates to @Foo.5
    # takes a vm file and sets curr_file to correct format
    # by taking the last element in the split list, after removing .vm extension
    def set_filename(self, vm_filename):
        self.curr_file = vm_filename.replace(".vm", "").split("/")[-1]

    # Writes to output file the assembly code that implements the arithmetic command
    # https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view pg 110
    # takes a command as str
    def write_arithmetic(self, command):
        # arithmetic uses the "inner" value first i.e. SP - 2
        # neg and not are the only commands that can work directly on top value
        # all others take two values, and have to pop the top value to D as a "holding cell"
        # pop decreases value in SP by 1, moves the A register to that, and sets D
        # then move address to one less to operate on "inner" value
        if command not in ("neg", "not"):
            self.pop_stack_to_D()
            self.write("A=A-1")
        # if is neg or not, we only need to operate on the most recent "outer" value
        # that's at where SP value is, less one
        else:
            self.write("@SP")
            self.write("A=M-1")

        # arithmetric is done on the "inner" value and changes that bit
        # pdf pg 41 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
        if command == "add":
            self.write("M=M+D")
        elif command == "sub":
            self.write("M=M-D")
        elif command == "neg":
            self.write("M=-M")
        elif command in ("eq", "gt", "lt"):
            # we currently have the "right/outer" value in D, and "left/inner" in M
            # if we subtract, and compare the result to 0, we'll know if eq, gt, or lt
            self.write("D=M-D")
            # bool_count to make label unique; label declared below
            self.write(f"@BOOL{self.bool_count}")

            # http://www.unige.ch/medecine/nouspikel/ti99/assembly.htm
            # jumping to instruction line for label (BOOL) due to the @BOOL label above
            # if jumping, go to
            if command == "eq":
                self.write("D;JEQ") # jump if equal zero
            elif command == "gt":
                self.write("D;JGT") # if > 0
            elif command == "lt":
                self.write("D;JLT") # if < 0

            # if we didn't jump to BOOL, set M = 0 for False in the "inner" value address
            # we need to set A again, since @BOOL above reset it
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=0")
            # jump to end, since we don't want to execute the (BOOL) label code
            self.write(f"@ENDBOOL{self.bool_count}")
            self.write("0;JMP")

            # declare label
            # if jumped to BOOL, set M = -1 for True in the "inner" value address
            self.write(f"(BOOL{self.bool_count})")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=-1")

            self.write(f"(ENDBOOL{self.bool_count})")

            self.bool_count += 1

        elif command == "and":
            self.write("M=M&D")
        elif command == "or":
            self.write("M=M|D")
        elif command == "not":
            self.write("M=!M")
        else:
            self.raise_error(command)

    # writes to output file the assembly code that implements given command (C_PUSH or C_POP)
    # takes a command, segment as str, index as int
    def write_push_pop(self, command, segment, index):
        # do all writing to setup the address
        self.map_address(segment, index)
        # push data to top of stack
        if command == "C_PUSH":
            # constant is the only command that uses D=A
            if segment == "constant":
                self.write("D=A")
            # others all set data to value of another register, D=M
            else:
                self.write("D=M")
            # now that we have D, push to stack
            self.push_D_to_stack()
        # pop data from top of stack
        elif command == "C_POP":
            self.write("D=A") # get the address of the segment
            self.write("@R13") # use a general register to store it temporarily
            self.write("M=D")
            self.pop_stack_to_D() # now we get D value from stack
            self.write("@R13") # and go back to get our segment address
            self.write("A=M")
            self.write("M=D") # and can finally set that address to D value
        else:
            self.raise_error(command)

    # label declaration with brackets
    def write_label(self, label):
        self.write(f"({self.curr_file}${label})", code=False)

    # jump to execute the command just after label
    def write_goto(self, label):
        self.write(f"@{self.curr_file}${label}", code=True)
        self.write("0;JMP") # unconditional jump

    # cond = pop the stack
    # if cond, then jump to execute command just after label
    def write_if(self, label):
        self.pop_stack_to_D()
        self.write(f"@{self.curr_file}${label}", code=True)
        self.write("D;JNE") # jump if D (true/false) not equal 0 (false)

    # declare a label for function entry
    # repeat nVars times: push 0; initialise that num of local vars
    def write_function(self, function_name, num_args):
        self.write(f"({function_name})", code=False)

        for _ in range(num_args):
            self.write("D=0")
            self.push_D_to_stack()

    # calls the function, informing that nArgs have been pushed onto stack
    def write_call(self, function_name, num_args):
        # need to first push the return address
        # that uses a label, so need to @label and push address to stack
        ret_add = function_name + " return " + str(self.call_count)
        self.call_count += 1
        self.write("@"+ ret_add)
        self.write("D=A") # getting the address, not the value
        self.push_D_to_stack()

        # now need to push LCL, ARG, THIS, THAT, one after the other onto stack
        for address in ("@LCL", "@ARG", "@THIS", "@THAT"):
            self.write(address)
            self.write("D=M") # getting the value in those, not the address
            self.push_D_to_stack()

        # ARG = SP - 5 - num_args
        self.write("@SP")
        self.write("D=M") # get SP value
        self.write("@" + str(num_args + 5)) # get the value as a constant in A register
        self.write("D=D-A")
        self.write("@ARG")
        self.write("M=D") # set ARG value

        # LCL = SP
        self.write("@SP")
        self.write("D=M")
        self.write("@LCL")
        self.write("M=D") # set LCL value

        # transfer control to called function
        self.write("@" + function_name)
        self.write("0;JMP") # unconditional jump to the function

        # declare label for return address
        self.write(f"({ret_add})", code=False)

    # returns function output
    def write_return(self):
        # use general purpose registers R13 and R14 for temp variables
        endframe = "R13"
        ret = "R14"

        # first create temp variable endframe, where the saved state for called function ends
        # has value LCL
        self.write("@LCL")
        self.write("D=M")
        self.write("@" + endframe)
        self.write("M=D")

        # next create temp variable return, endframe - 5, for where return address is
        self.write("@" + endframe)
        self.write("D=M")
        self.write("@5") # get the value as a constant for math below
        self.write("D=D-A")
        # since endframe value is value of LCL, which is also address of end of stack/where local vars begin
        # the D above also refers to the address for return address
        self.write("A=D")
        self.write("D=M") # get the value in return address saved state
        self.write("@" + ret)
        self.write("M=D") # save value

        # return value from function is popped to where ARG pointer is
        self.pop_stack_to_D()
        self.write("@ARG")
        self.write("A=M") # going to where ARG pointer is
        self.write("M=D") # put the return value in that address

        # reposition SP of the caller; SP = ARG + 1
        self.write("@ARG")
        self.write("D=M")
        self.write("@SP")
        self.write("M=D+1") # SP pointer is ARG address + 1

        # that = endframe - 1
        # this = endframe - 2
        # arg = endframe - 3
        # lcl = endframe - 4
        for address in ("@THAT", "@THIS", "@ARG", "@LCL"):
            self.write("@" + endframe)
            self.write("M=M-1") # decrease by one each time
            self.write("A=M") # go to that endframe - X address
            self.write("D=M") # store the value
            self.write(f"{address}")
            self.write("M=D") # put the value back

        # goto return address in caller's code
        self.write("@" + ret)
        self.write("A=M")
        self.write("0;JMP") # unconditional jump

    # closes the output .asm file
    def close(self):
        self.asm.close()

    ### END API
    ###########

    # takes a str text input, writes it to .asm file with newline
    # line count for debugging purposes
    def write(self, text, code=True):
        self.asm.write(text)
        if code:
            self.asm.write(" // code line " + str(self.line_count))
            self.line_count += 1
        self.asm.write("\n")

    # error catching if argument isn't in predefined list
    def raise_error(self, argument):
        raise ValueError(f"{argument} is an invalid argument")

    # mapping is pdf pg 97 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
    # takes a segment as str e.g. local, constant, this, that
    # also takes an index as int
    # maps to the right RAM segment and writes to .asm file
    def map_address(self, segment, index):
        # get the address if applicable
        address = self.address_dict.get(segment)

        # constant 17 should translate and be written as @17
        if segment == "constant":
            self.write("@" + str(index))
        # static i to @filename.i
        elif segment == "static":
            self.write("@" + self.curr_file + "." + str(index))
        # pointer to @R3 or @R4, depending on index
        elif segment == "pointer":
            self.write("@R" + str(address + int(index)))
        # temp to @R5 - 12, depending on index
        elif segment == "temp":
            self.write("@R" + str(address + int(index)))
        # these addresses in the dict are str e.g. LCL
        # this is just to set up the correct RAM address
        # the data entry comes in later in write_push_pop
        elif segment in ("local", "argument", "this", "that"):
            # go to relevant RAM address based on segment from RAM1 to 4
            self.write("@" + address)
            # set data register to value of the RAM address
            # e.g. if LCL in RAM1 stores base address of LCL starting in 1015
            # then D becomes 1015
            self.write("D=M")
            # using A instruction as a constant, to add to D later
            # e.g. 2
            self.write("@" + str(index))
            # set new RAM address
            # e.g. A is 1015 + 2 = 1017
            self.write("A=D+A")
        else:
            self.raise_error(segment)

    # push data in D register to the stack and increase @SP stack pointer
    # before this, D register has already been set
    # pdf pg 59 https://drive.google.com/file/d/19fe1PeGnggDHymu4LlVY08KmDdhMVRpm/view
    def push_D_to_stack(self):
        # go to SP in RAM[0] and use the value to go to where SP is at
        self.write("@SP")
        self.write("A=M") # go to SP register
        self.write("M=D") # set SP register to D, predefined
        self.write("@SP") # go back to SP in RAM[0] and inc value
        self.write("M=M+1")

    # pop data from stack and decrease @SP value
    def pop_stack_to_D(self):
        # go to SP in RAM[0], get one less than the value
        # one less because SP points to first empty address
        self.write("@SP")
        self.write("M=M-1")
        self.write("A=M") # go to the SP value address after the decrease
        self.write("D=M") # get the data from that address

    # delete? doesn't seem used
    # we need ways to move the @SP pointer, since arithmetric requires it
    # will need to work with the two values in the stack, which are @SP - 1 and @SP - 2
    # set_A is needed to get the address to update to the new value in SP
    # decrease SP value at RAM[0]
    # def decrease_SP(self):
    #     self.write("@SP")
    #     self.write("M=M-1")
    #
    # # increase SP value at RAM[0]
    # def increase_SP(self):
    #     self.write("@SP")
    #     self.write("M=M+1")
    #
    # # set A register to SP value at RAM[0]
    # def set_A_to_stack(self):
    #     self.write("@SP")
    #     self.write("A=M")

class Main:
    def __init__(self, file_path):
        self.asm_file = None
        self.vm_files = []
        self.parse_files(file_path)
        self.cw = CodeWriter(self.asm_file)
        for vm_file in self.vm_files:
            self.translate(vm_file)
        self.cw.close()

    def parse_files(self, file_path):
        if ".vm" in file_path:
            # create new asm file with same name, diff extension
            self.asm_file = file_path.replace(".vm", ".asm")
            self.vm_files.append(file_path)
        else:
            # remove the last / if any, since we want to use os.walk later
            # e.g. parent/dir/ becomes parent/dir and parent/dir/file stays same
            file_path = file_path[:-1] if file_path[-1] == "/" else file_path
            # want to get the last elem to name the file
            # e.g. parent/dir/file becomes parent, dir, file
            path_elements = file_path.split("/")
            # create .asm file with last elem
            # e.g. parent/dir/dir.asm or parent/dir/file/file.asm
            self.asm_file = file_path + "/" + path_elements[-1] + ".asm"
            # os.walk traverses files in the given directory tree
            # returns path, dirs, and files https://www.geeksforgeeks.org/os-walk-python/
            # note that os.walk returns multiple 3-tuples
            for branch in os.walk(file_path):
                dirpath, dirnames, filenames = branch
            # filter takes a function to use and a sequence to be filtered
            # here we're going through all the filenames and seeing if any have .vm extension
            vm_files = filter(lambda x: ".vm" in x, filenames)
            self.vm_files = [file_path + "/" + vm_file for vm_file in vm_files]

    def translate(self, vm_file):
        parser = Parser(vm_file)
        self.cw.set_filename(vm_file)
        # used @property
        while parser.has_more_commands:
            parser.advance()
            self.cw.write("// " + " ".join(parser.curr_instruction), code=False)
            if parser.command_type == "C_ARITHMETIC":
                self.cw.write_arithmetic(parser.arg1)
            elif parser.command_type == "C_PUSH":
                self.cw.write_push_pop("C_PUSH", parser.arg1, parser.arg2)
            elif parser.command_type == "C_POP":
                self.cw.write_push_pop("C_POP", parser.arg1, parser.arg2)
            elif parser.command_type == "C_LABEL":
                self.cw.write_label(parser.arg1)
            elif parser.command_type == "C_GOTO":
                self.cw.write_goto(parser.arg1)
            elif parser.command_type == "C_IF":
                self.cw.write_if(parser.arg1)
            elif parser.command_type == "C_FUNCTION":
                self.cw.write_function(parser.arg1, int(parser.arg2))
            elif parser.command_type == "C_CALL":
                self.cw.write_call(parser.arg1, int(parser.arg2))
            elif parser.command_type == "C_RETURN":
                self.cw.write_return()
        parser.close()
        # don't need infinite loop for the course
        # self.cw.write("(END)")
        # self.cw.write("@END")
        # self.cw.write("0;JMP")

if __name__ == "__main__":

    file_path = sys.argv[1]
    Main(file_path)