'''
based on https://github.com/kronosapiens/nand2tetris/blob/master/projects/06/assembler.py

builds an assembler for the Hack language from nand2tetris https://www.nand2tetris.org/project06

need a command parser, a code to binary translater, and a symbol table

the assembler then uses that together to convert from assembly to machine language

run in terminal with syntax python assembler.py file_name.asm
'''

import sys

class Assembler:
    # takes a parser, code, symbol as defined above
    def __init__(self, parser, code, symbol):
        self.parser = parser
        self.code = code
        self.symbol = symbol
        self.hack = None
        self.ram_address = 16  # R0 to R15 of RAM are taken

    # takes an asm file and assembles it to machine language
    def assemble(self, asm_filename):
        # check file type https://www.tutorialspoint.com/python/assertions_in_python.htm
        assert ".asm" in asm_filename, "Must pass .asm file"
        # use the defined parser passed to Assembler
        # remember that load_file calls reset_file so no need to worry about that
        self.parser.load_file(asm_filename)
        # also open a .hack file to write to
        hack_filename = asm_filename.replace(".asm", ".hack")
        self.hack = open(hack_filename, "w")

        # first pass to build label table
        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.command_type == "L_COMMAND":
                self.write_L(self.parser.symbol)

        # second pass to write to hack
        # have to reset file now
        self.parser.reset_file()
        while self.parser.has_more_commands():
            self.parser.advance()
            if self.parser.command_type == "A_COMMAND":
                self.write_A(self.parser.symbol)
            elif self.parser.command_type == "C_COMMAND":
                self.write_C(self.parser.comp, self.parser.dest, self.parser.jump)
        # close both parser and hack file once done
        self.parser.asm.close()
        self.hack.close()

    # takes a value, which is either non-neg decimal or symbol
    # need to handle both cases
    # writes the full A-instruction with 0 in front to open hack file
    def write_A(self, symbol):
        # see if is value or symbol
        # try and except rather than if statement https://stackoverflow.com/a/3501408/13944490
        # https://docs.python.org/3/tutorial/errors.html
        try:
            int(symbol)
        except ValueError:
            # building the symbol dict on first pass
            if not self.symbol.contains(symbol):
                # get next guaranteed avail ram address and add symbol there
                address = self.create_address(self.ram_address)
                self.symbol.add_entry(symbol, address)
                self.ram_address += 1
            instruction = "0" + self.symbol.get_address(symbol)
        else:
            instruction = "0" + self.create_address(symbol)
        self.write_to_hack(instruction)

    # pdf pg 7 https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf
    # takes a comp, dest, jump, adds 111 in front
    # writes the full C-instruction in binary to open hack file
    def write_C(self, comp, dest, jump):
        instruction = "111" + self.code.comp(comp) + self.code.dest(dest) + self.code.jump(jump)
        self.write_to_hack(instruction)

    # used in the first pass to build the label table 
    # uses the first guaranteed avail address, 
    # which is one more than current instruction num
    def write_L(self, symbol):
        address = self.create_address(self.parser.instruction_num + 1)
        self.symbol.add_entry(symbol, address)

    # takes a decimal number and converts to padded binary representation
    # https://stackoverflow.com/a/34887286/13944490
    # address is 15-bit, since 1st bit is used for A/C instruction
    def create_address(self, address_num):
        return "{0:{fill}15b}".format(int(address_num), fill="0")

    # takes an instruction, writes to open hack file
    def write_to_hack(self, instruction):
        self.hack.write(instruction + "\n")

# Parser breaks the assembly language down into components
# command can be A-command, C-command, or label
class Parser:
    def __init__(self):
        pass

    # loads asm file as read only
    # initialises symbols, command_type
    def load_file(self, asm_filename):
        # https://docs.python.org/3/library/functions.html#open
        self.asm = open(asm_filename, "r")
        self.symbol = None
        self.command_type = None
        self.dest = None
        self.comp = None
        self.jump = None
        self.curr_instruction = None
        self.instruction_num = None
        self.reset_file() 

    # takes the instruction, returns symbol and command type
    def parse_A(self, instruction):
        # A instruction looks like @address
        symbol = instruction[1:]
        command_type = "A_COMMAND"
        return symbol, command_type

    # takes instruction, returns dest, comp, jump, and command type
    # we have 3 symbols to return here rather than just 1
    def parse_C(self, instruction):
        # C instruction looks like dest = comp; jump
        # both dest and jump are optional
        dest, comp, jump = None, None, None
        split_on_semicolon = instruction.split(";")
        # this means there was a ; and a jump
        if len(split_on_semicolon) == 2:
            jump = split_on_semicolon[1]
        split_on_equal = split_on_semicolon[0].split("=")
        # this means there was a + and a dest
        if len(split_on_equal) == 2:
            dest = split_on_equal[0]
            comp = split_on_equal[1]
        else:
            comp = split_on_equal[0]
        command_type = "C_COMMAND"
        return dest, comp, jump, command_type

    # takes instruction, returns symbol and command type
    def parse_label(self, instruction):
        # label looks like (label)
        symbol = instruction[1:-1]
        command_type = "L_COMMAND"
        return symbol, command_type

    # gets current instruction, sets symbols and command types
    # calls next instruction
    # unsure if setting so many vars and not taking/returning is best practic
    # but couldn't figure out how to do otherwise
    def advance(self):
        ci = self.curr_instruction
        # check what type of command
        # increase the instruction num if A or C instruction
        if ci[0] == "@":
            self.symbol, self.command_type = self.parse_A(ci)
            self.instruction_num += 1
        elif ci[0] == "(":
            self.symbol, self.command_type = self.parse_label(ci)
        else:
            self.dest, self.comp, self.jump, self.command_type = self.parse_C(ci)
            self.instruction_num += 1
        self.get_next_instruction()
        return True

    # reads one line only from file and sets current instruction to it
    def get_next_instruction(self):
        # read one line from file https://www.w3schools.com/python/ref_file_readline.asp
        raw_line = self.asm.readline().strip()
        # exclude comments
        line = raw_line.split("//")[0].strip()
        self.curr_instruction = line
        return True 

    # returns boolean if there are more commands in input
    def has_more_commands(self):
        return bool(self.curr_instruction)

    # starts reading file from beginning
    # resets current instruction
    # resets current instruction number
    def reset_file(self):
        # go to start of file
        # https://www.geeksforgeeks.org/python-seek-function/
        self.asm.seek(0, 0)
        # start reading until get to first instruction
        raw_line = self.asm.readline().strip()
        while self.is_not_instruction(raw_line):
            raw_line = self.asm.readline().strip()
        line = raw_line.split("//")[0].strip()
        self.curr_instruction = line
        # init at -1, becomes 0 once first instruction passed later
        self.instruction_num = -1

    # Text beginning with two slashes (//) and ending at the end of the line is considered a comment and is ignored.
    # ignore whitespace and empty lines
    # return boolean
    def is_not_instruction(self, line):
        # we've stripped the line in reset_file
        # so if this line started with X number of spaces and then had //
        # it'd still have been stripped to start with // from index 0
        empty = not line
        comment = line[:2] == "//"
        return empty or comment 

# python3 doesn't need "Code(object)"
# https://www.reddit.com/r/learnpython/comments/4ak38l/what_to_put_inside_the_brackets_when_creating_a/
# Code translates assembly language syntax to binary
# translation tables based on Hack language in nand2tetris
class Code:
    def __init__(self):
        pass
    # pdf pg 7 for translation https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf
    # returns 7 bits
    def comp(self, syntax):
        # dict is string to string, not int
        # other implementations replace 'M' with 'A'
        # was easier for me to understand by just putting all the M values
        comp_dict = {
            '0': '101010',
            '1': '111111',
           '-1': '111010',
            'D': '001100',
            'A': '110000',
           '!D': '001101',
           '!A': '110001',
           '-D': '001111',
           '-A': '110011',
          'D+1': '011111',
          'A+1': '110111',
          'D-1': '001110',
          'A-1': '110010',
          'D+A': '000010',
          'D-A': '010011',
          'A-D': '000111',
          'D&A': '000000',
          'D|A': '010101',
            'M': '110000',
           '!M': '110001',
           '-M': '110011',
          'M+1': '110111',
          'M-1': '110010',
          'D+M': '000010',
          'D-M': '010011',
          'M-D': '000111',
          'D&M': '000000',
          'D|M': '010101'
        }
        # check for the a bit
        if 'M' in syntax:
            a_bit ='1'
        else:
            a_bit = '0'
        # c-bit is the 6 c bits defined in the dict above based on syntax
        c_bit = comp_dict.get(syntax, '000000')
        return a_bit + c_bit

    # pdf pg 8 for translation https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf
    # returns 3 bits
    def dest(self, syntax):
        dest_dict = {
            'M': '001',
            'D': '010',
           'MD': '011',
            'A': '100',
           'AM': '101',
           'AD': '110',
          'AMD': '111'
        }
        # the null value returns zero in our translation,
        # so if we exclude it in our dict and use get,
        # we achieve same effect 
        return dest_dict.get(syntax, '000')

    # returns 3 bits
    def jump(self, syntax):
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }

        return jump_dict.get(syntax, '000')

# symbol dictionary with predefined table and ability to add more symbols
class Symbol:
    def __init__(self):
    # pdf pg 8 https://b1391bd6-da3d-477d-8c01-38cdf774495a.filesusr.com/ugd/44046b_b73759b866b249a0b3a715bf5a18f668.pdf
    # predefined symbols
    # SCREEN is 16384, KBD is 24576 in decimal
        self.symbol_dict = {
             'SP': '000000000000000',
            'LCL': '000000000000001',
            'ARG': '000000000000010',
           'THIS': '000000000000011',
           'THAT': '000000000000100',
             'R0': '000000000000000',
             'R1': '000000000000001',
             'R2': '000000000000010',
             'R3': '000000000000011',
             'R4': '000000000000100',
             'R5': '000000000000101',
             'R6': '000000000000110',
             'R7': '000000000000111',
             'R8': '000000000001000',
             'R9': '000000000001001',
            'R10': '000000000001010',
            'R11': '000000000001011',
            'R12': '000000000001100',
            'R13': '000000000001101',
            'R14': '000000000001110',
            'R15': '000000000001111',
         'SCREEN': '100000000000000',
            'KBD': '110000000000000',
        }
    # takes a symbol (str), adddress (int), adds to symbol table
    # doesn't return anything
    def add_entry(self, symbol, address):
        self.symbol_dict[symbol] = address
    # takes a symbol (str), 
    # returns boolean if symbol table contains symbol
    def contains(self, symbol):
        return symbol in self.symbol_dict
    # takes a symbol (str), returns address (int) associated
    def get_address(self, symbol):
        return self.symbol_dict[symbol]

# https://medium.com/python-features/understanding-if-name-main-in-python-a37a3d4ab0c3
if __name__ == "__main__":
    # https://www.geeksforgeeks.org/how-to-use-sys-argv-in-python/
    asm_filename = sys.argv[1]
    assembler = Assembler(Parser(), Code(), Symbol())
    assembler.assemble(asm_filename)
