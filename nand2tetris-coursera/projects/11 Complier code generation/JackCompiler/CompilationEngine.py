# References
# https://github.com/itayabu/nand2tetris/tree/master/ex10
# https://github.com/saikumarm4/Nand2Tetris/blob/master/10/Lexical.py
# https://github.com/kronosapiens/nand2tetris/blob/master/projects/10/JackAnalyzer.py

import JackTokenizer
import SymbolTable
import VMwriter

class CompilationEngine:

    def __init__(self, input_file, output_file):
        """
        creates new compilation engine with given input and output
        It gets its input from a JackTokenizer and emits its parsed structure into an output file/stream.

        e.g. integerConstant 300 to push constant 1

        The output is generated by a series of compilexxx() routines,
        one for every syntactic element xxx of the Jack grammar.

        The contract between these routines is that each compilexxx() routine should
        read the syntactic construct xxx from the input, advance() the tokenizer
        exactly beyond xxx, and output the parsing of xxx.

        Thus, compilexxx()may only be called if indeed xxx is the next syntactic
        element of the input.
        :param input:
        :param output:
        """
        # init tokenizer with input, VMwriter with output, and symboltable no args
        self.tokenizer = JackTokenizer.JackTokenizer(input_file)
        self.vm_writer = VMwriter.VMWriter(output_file)
        self.symbol_table = SymbolTable.SymbolTable()

        # keep track of class name e.g. Main and subroutine name e.g. Main.main
        self.class_name = ""
        self.sub_name = ""

        # initialise expression sets
        self.binary_op = self.binary_op()
        self.unary_op = self.unary_op()
        self.keyword_constant = self.keyword_constant()

        # deprecated since not writing to XML but to VM
        # self.parsed_rules = []  # used for keeping track of open and close <> statements
        # self.indent = ""
        # self.output_file = open(output_file, "w")

    ###########################
    ### Program structure / API

    def compile_class(self):
        """
        a class begins with a keyword class,
        then we have a class name, which as you will see later on is an identifier.
        Then we have curly left paren { which begins the definition of the class.
        Then we may have zero or more declarations of either fields or static variables.
        So all together we call this class classVarDec.
        And then we may have zero or more subroutine declarations followed a right curly bracket }

        i.e. structure is
        "class" className "{" classVarDec* subroutineDec* "}" in the high level code

        We want to translate that to VM code, which means all the "class", {, } etc get read but not written
        :return:
        """
        self.advance()  # get class keyword
        self.class_name = self.advance()[1]  # get class name; reminder the tokens are a (type, value) tuple

        self.advance()  # get { symbol
        # need to check if have any classVarDec
        # unsure if if, try while? think the course assumes only one class per file
        while self.exist_class_var_dec():
            self.compile_class_var_dec()
        # see if any subroutines
        while self.exist_subroutine():
            self.compile_subroutine_dec()
        self.advance()  # get } symbol
        self.vm_writer.close()

    def exist_class_var_dec(self):
        """
        checking if next value is field or static var, which are the only two types of class vars
        :return boolean:
        """
        return self.next_value_is("field") or self.next_value_is("static")

    def compile_class_var_dec(self):
        """
        compiles field or static declaration
        :return:
        """
        # as long as next value is field or static
        while self.exist_class_var_dec():
            self.write_class_var_dec()

    def write_class_var_dec(self):
        """
        classVarDec is structured like:
        ("static" | "field") type varName ("," varName)* ";"
        e.g. field int x, y;

        Note this is just the declaration, we're creating the symbol table and not writing to .vm yet
        :return:
        """
        kind = self.advance()[1]  # get field or static; reminder token is a tuple of (tokenType value)
        type = self.advance()[1]  # get var type
        name = self.advance()[1]  # get var name
        self.symbol_table.define(name, type, kind)  # creates entry in the symbol table

        # if next value is , implies still more var names after it
        while self.next_value_is(","):
            self.advance()  # get ,
            name = self.advance()[1]  # get var name
            self.symbol_table.define(name, type, kind)
        self.advance()  # get ;

    def exist_subroutine(self):
        """
        if constructor, function, or method
        :return boolean:
        """
        return self.next_value_is("constructor") or self.next_value_is("function") or self.next_value_is("method")

    def compile_subroutine_dec(self):
        """
        compiles a constructor, function, or method
        subroutine declaration structure is:
        ("constructor"|"function"|"method") ("void"|type) subroutineName "(" parameterList ")" subroutineBody

        Note this is just the declaration, we're creating the symbol table and not writing to .vm yet
        :return:
        """
        func_type = self.advance()[1]  # get subroutine; reminder it's stored as tuple
        self.advance()  # get subroutine return type / class name
        self.sub_name = self.class_name + "." + self.advance()[1]  # get and make subroutine name; e.g Main.main
        self.symbol_table.start_subroutine(self.sub_name)  # creates new symbol table for subroutine
        self.symbol_table.set_scope(self.sub_name)  # change scope to subroutine / the subroutine symbol dict

        self.advance()  # get (
        self.compile_parameter_list(func_type)
        self.advance()  # get )
        self.compile_subroutine_body(func_type)

    def compile_parameter_list(self, function_type):
        """
        Methods are called using method(...), or variable.method(...)
        The first version calls method passing the current object.
        Think this.method(...), except that Jack doesn't allow access to the this variable.

        Functions and constructors are called using
        ClassName.function(...)

        So, if it doesn't have a ".", this is a method call.
        If it has a ".", you need to see if the symbol on the left is a variable. If it is, this is a method call.
        Otherwise, this is function (or constructor) call.
        compiles zero or more parameter lists, excluding enclosing ()
        :return:
        """
        # Note that for subroutines (methods) we’ll always need a “this” entry,
        # with kind “argument”, # “0”. The type depends on the class name
        # reminder define takes a name, type, and kind
        # unsure why "self" and not class name
        if function_type == "method":
            self.symbol_table.define("this", "self", "arg")
        while self.exist_parameter():
            self.write_parameter()

    def exist_parameter(self):
        """

        :return boolean:
        """
        return not self.next_token_is("symbol")

    def write_parameter(self):
        """
        parameter list structure is:
        ( (type varName) ("," type varName)* )? where * is 0 or more times, ? is 0 or 1 times
        :return:
        """
        type = self.advance()[1]  # get parameter type; I think this should be same as class name?
        name = self.advance()[1]  # get var name
        # e.g. these two above get Point other within method int distance (Point other) {} when declaring a function
        self.symbol_table.define(name, type, "arg")
        if self.next_value_is(","):
            self.advance()  # get ,
        # note that we get the , after since the while loop above will pick the next parameter, if any

    def compile_subroutine_body(self, function_type):
        """
        subroutine body structure is:
        "{" varDec* statements "}"

        Note this declares the vars but also starts writing to .vm
        e.g. function main 0
        :return:
        """
        self.advance()  # get {
        while self.exist_var_dec():
            self.compile_var_dec()  # get varDec* and compile the symbol table

        # after we've compiled symbol table, we can write the first line e.g. function main 0
        # note the line is before the {statements}, but we needed to find out how many nVars
        nVars = self.symbol_table.var_count("var")

        self.vm_writer.write_function(self.sub_name, nVars)  # writes to .vm
        self.load_pointer(function_type)
        self.compile_statements()  # get statements and writes to .vm
        self.advance()  # get }

        self.symbol_table.set_scope("global")  # reset the scope after subroutine done

    def exist_var_dec(self):
        """

        :return boolean:
        """
        return self.next_value_is("var")

    def compile_var_dec(self):
        """
        var declaration structure is:
        "var" type varName ("," varName)* ";"
        :return:
        """
        kind = self.advance()[1]  # get var
        type = self.advance()[1]  # get var type
        name = self.advance()[1]  # get var name
        self.symbol_table.define(name, type, kind)

        while self.next_value_is(","):
            self.advance()  # get ,
            name = self.advance()[1]  # get var name
            self.symbol_table.define(name, type, kind)
        self.advance()  # get ;

    def load_pointer(self, function_type):
        """
        when compiling a method: vm code must set base of "this" segment to argument 0
        when compiling a constructor: vm code must allocate block of memory,
        and set base of "this" segment to new base address
        reminder that pointer 0 accesses this; 1 accesses that
        :param function_type:
        :return:
        """
        if function_type == "method":
            self.vm_writer.write_push("argument", 0)  # we push the value of argument index 0 to stack
            self.vm_writer.write_pop("pointer", 0)  # we pop the value into pointer index 0
        if function_type == "constructor":
            global_vars = self.symbol_table.class_var_count("field")  # unsure why no count static
            self.vm_writer.write_push("constant", global_vars)  # we push the number of global vars to stack
            self.vm_writer.write_call("Memory.alloc", 1)  # OS function to allocate space for new object with (size)
            self.vm_writer.write_pop("pointer", 0)  # anchors this at base address
            # e.g. constructor Point new(int x, int y) becomes:
            # push 2
            # call Memory.alloc 1
            # pop pointer 0

    ### End program structure
    #########################

    #########################
    ### Statements

    def compile_statements(self):
        """
        compiles sequence of statements, not including the enclosing {}
        statements can appear 0 or more times
        are either let, if, while, do, return
        :return:
        """
        while self.exist_statement():
            if self.next_value_is("let"):
                self.compile_let()
            elif self.next_value_is("if"):
                self.compile_if()
            elif self.next_value_is("while"):
                self.compile_while()
            elif self.next_value_is("do"):
                self.compile_do()
            elif self.next_value_is("return"):
                self.compile_return()

    def exist_statement(self):
        """

        :return boolean:
        """
        return self.next_value_is("let") or self.next_value_is("if") or self.next_value_is("while") \
            or self.next_value_is("do") or self.next_value_is("return")

    def compile_let(self):
        """
        structure is:
        "let" varName ("[" expression "]")? "=" expression ";"
        :return:
        """
        is_array = False
        self.advance()  # get let
        name = self.advance()[1]  # get var name

        if self.next_value_is("["):  # case of varName [expression]; only 0 or 1 times
            is_array = True
            self.compile_array_index(name)

        self.advance()  # get =
        self.compile_expression()  # get expression
        if is_array:
            # temp 0 is the value of expression
            # top stack value is RAM address of arr[expression]
            # allows us to use pointer 1 and that 0 safely w/o array crash
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)
        else:
            self.write_pop(name) # Note this is the CE write_push, which adds on to VMwriter write_push
        self.advance()  # get ;

    def compile_if(self):
        """
        if statement with 0 or 1 else statements
        structure is:
        "if" "(" expression ")" "{" statements "}" ("else" "{" statements "}")?

        We generate code that computes the value of the expression and puts it on the stack,
        then we negate whatever we computed.
        If the result is true, we go to label L1. If the result is false, we go to label L2.
        :return:
        """
        self.advance()  # get if
        self.advance()  # get (
        self.compile_expression()
        self.advance()  # get )

        # need to generate unique labels for VM
        if_counter = str(self.symbol_table.if_Counter)
        self.symbol_table.if_Counter += 1

        self.vm_writer.write_if("IF_TRUE" + if_counter)
        self.vm_writer.write_goto("IF_FALSE" + if_counter)  # if false, go to IF_FALSE label below
        self.vm_writer.write_label("IF_TRUE" + if_counter)

        # unsure, think something wrong here
        # seems the error was in their file and the compiler
        # their compiler code doesn't work :/
        self.advance()  # get {
        self.compile_statements()
        self.advance()  # get }

        if self.next_value_is("else"):
            self.vm_writer.write_goto("IF_END" + if_counter)
            self.vm_writer.write_label("IF_FALSE" + if_counter)
            self.advance()  # get else
            self.advance()  # get {
            self.compile_statements()
            self.advance()  # get }
            self.vm_writer.write_label("IF_END" + if_counter)

        else:
            self.vm_writer.write_label("IF_FALSE" + if_counter)

    def compile_while(self):
        """
        structure is:
        "while" "(" expression ")" "{" statements "}"

        In VM, the implementation negates it first for easier flow
        I generate this flow chart, which begins once again with negating the expression.
        If the result is true, I get out of the while.
        If the result is false, It means that the expression is true and therefore I go into the while
        and I execute the statements and then I go back to reevaluate the expression and so on and so forth.

        :return:
        """
        # need to generate unique labels for VM
        while_counter = str(self.symbol_table.while_counter)
        self.symbol_table.while_counter += 1
        self.vm_writer.write_label("WHILE_EXP" + while_counter)

        self.advance()  # get while
        self.advance()  # get (
        self.compile_expression()
        self.vm_writer.write_arithmetic("not")  # the negation
        self.vm_writer.write_if("WHILE_END" + while_counter)
        self.advance()  # get )

        self.advance()  # get {
        self.compile_statements()
        self.vm_writer.write_goto("WHILE_EXP" + while_counter)
        self.vm_writer.write_label("WHILE_END" + while_counter)
        self.advance()  # get }

    def compile_do(self):
        """
        structure is:
        "do" subroutineCall ";"
        :return:
        """
        self.advance()  # get do
        self.compile_subroutine_call()
        self.vm_writer.write_pop("temp", 0)  # pop temp 0 was needed to pop the unneeded value returned by the do
        self.advance()  # get ;

    def compile_return(self):
        """
        structure is:
        "return" expression? ";"
        :return:
        """
        self.advance()  # get return
        no_return = True
        while self.exist_expression():
            no_return = False
            self.compile_expression()
        if no_return:
            self.vm_writer.write_push("constant", 0)  # if functions don't return anything, contract is to push 0
        self.vm_writer.write_return()
        self.advance()  # get ;

    def exist_expression(self):
        """
        expression has at least one term
        :return boolean:
        """
        return self.exist_term()

    def compile_expression(self):
        """
        structure is:
        term (operator term)*
        :return:
        """
        self.compile_term()
        while self.next_value_in(self.binary_op):
            op = self.advance()[1]  # get operator
            self.compile_term()
            if op == "+":
                self.vm_writer.write_arithmetic("add")
            elif op == "-":
                self.vm_writer.write_arithmetic("sub")
            elif op == "*":  # * and / are the only two functions which require OS
                self.vm_writer.write_call("Math.multiply", 2)
            elif op == "/":
                self.vm_writer.write_call("Math.divide", 2)
            elif op == "|":
                self.vm_writer.write_arithmetic("or")
            elif op == "&":
                self.vm_writer.write_arithmetic("and")
            elif op == "=":
                self.vm_writer.write_arithmetic("eq")
            elif op == "<":
                self.vm_writer.write_arithmetic("lt")
            elif op == ">":
                self.vm_writer.write_arithmetic("gt")
            else:
                print("ERROR in compile_expression")

    def exist_term(self):
        """

        :return boolean:
        """
        # the IDENTIFIER should handle varName and subroutineCall
        return self.next_token_is("integerConstant") or self.next_token_is("stringConstant") \
            or self.next_value_in(self.keyword_constant) or self.next_token_is("identifier") \
            or self.next_value_is("(") or self.next_value_in(self.unary_op)

    def compile_term(self):
        """
        structure is:
        integerConstant | stringConstant | keywordConstant | varName |
        varName "[" expression "]" | subroutineCall | "(" expression ")" | unaryOp term
        :return:
        """

        array = False

        # for codeWrite(exp):
        # e.g. source code x + g(2, y, -z) * 5

        # if exp is a number n:
        # output "push n"
        if self.next_token_is("integerConstant"):
            value = self.advance()[1] # get constant
            self.vm_writer.write_push("constant", value)  # e.g. push constant 5 from integerConstant 5
        elif self.next_token_is("stringConstant"):
            value = self.advance()[1]  # get string
            self.vm_writer.write_push("constant", len(value))
            self.vm_writer.write_call("String.new", 1)  # string constants created using OS constructor String.new(len)
            for letter in value:  # str assignments handled using calls to String.appendChar(c)
                self.vm_writer.write_push("constant", ord(letter))
                self.vm_writer.write_call("String.appendChar", 2)
        elif self.next_value_in(self.keyword_constant):
            value = self.advance()[1]  # get keyword constant
            if value == "this":
                self.vm_writer.write_push("pointer", 0)
            else:
                self.vm_writer.write_push("constant", 0)
                if value == "true":
                    self.vm_writer.write_arithmetic("not")
        elif self.next_token_is("identifier"):
            n_locals = 0
            # className, varName, or subroutine
            name = self.advance()[1]  # get class or var name
            if self.next_value_is("["):  # case of varName[expression]
                array = True
                self.compile_array_index(name)

            if self.next_value_is("("):  # case of (expression)
                n_locals += 1
                self.vm_writer.write_push("pointer", 0)
                self.advance()  # get (
                n_locals += self.compile_expression_list()  # need to get the number of vars in the (expression)
                self.advance()  # get )
                self.vm_writer.write_call(self.class_name + "." + name, n_locals)  # e.g. call Math.multiply 2

            # thinks somewhere here when checking scope goes wrong
            elif self.next_value_is("."):  # case of subroutine call
                self.advance()  # get .
                sub_name = self.advance()[1]  # get subroutine name

                # check if in scope
                if name in self.symbol_table.curr_scope or name in self.symbol_table.class_scope:
                    self.write_push(name)  # finds the idx of name within the sub symbol table
                    name = self.symbol_table.type_of(name) + "." + sub_name
                    n_locals += 1
                else:
                    name = name + "." + sub_name

                self.advance()  # get (
                n_locals += self.compile_expression_list()
                self.advance()  # get )
                self.vm_writer.write_call(name, n_locals)

            else:
                if array:
                    self.vm_writer.write_pop("pointer", 1)
                    self.vm_writer.write_push("that", 0)
                elif name in self.symbol_table.curr_scope:
                    if self.symbol_table.kind_of(name) == "var":
                        self.vm_writer.write_push("local", self.symbol_table.index_of(name))
                    elif self.symbol_table.kind_of(name) == "arg":
                        self.vm_writer.write_push("argument", self.symbol_table.index_of(name))
                else:
                    if self.symbol_table.kind_of(name) == "static":
                        self.vm_writer.write_push("static", self.symbol_table.index_of(name))
                    elif self.symbol_table.kind_of(name) == "field":
                        self.vm_writer.write_push("this", self.symbol_table.index_of(name))
                    else:
                        print("ERROR in CE compile_term_else")

        elif self.next_value_is("("):
            self.advance()  # get (
            self.compile_expression()
            self.advance()  # get )

        # if exp is "op exp" e.g. -z
        # codeWrite(exp)
        # output "op"
        elif self.next_value_in(self.unary_op):
            op = self.advance()[1]  # get unary operator
            self.compile_term()
            if op == "-":  # these are the only two cases where you have to write again after the first term
                self.vm_writer.write_arithmetic("neg")
            elif op == "~":
                self.vm_writer.write_arithmetic("not")

    def compile_subroutine_call(self):
        """
        structure is:
        subroutineName "(" expressionList ")" |
        (className|varName) "." subroutineName "(" expressionList ")"
        :return:
        """

        n_locals = 0

        first_name = self.advance()[1]  # get class/subroutine/var name; reminder tokens are a tuple
        if self.next_value_is("."):  # case of className.subroutineName
            self.advance()  # get .
            last_name = self.advance()[1]  # get subroutine name
            # if subroutine already in scopes
            if first_name in self.symbol_table.curr_scope or first_name in self.symbol_table.class_scope:
                # Note this is the CE write_push, which adds on to VMwriter write_push
                # e.g. push local 5 where 5 is the index associated with the name in the symbol table
                self.write_push(first_name)
                # the type here is the class/subroutine name I think?
                full_name = self.symbol_table.type_of(first_name) + "." + last_name
                n_locals += 1
            else:
                full_name = first_name + "." + last_name

        else:
            self.vm_writer.write_push("pointer", 0)
            n_locals += 1
            full_name = self.class_name + "." + first_name

        # now we're starting at same point in above structure
        self.advance()  # get (
        n_locals += self.compile_expression_list()
        self.vm_writer.write_call(full_name, n_locals)  # e.g. call factorial 1
        self.advance()  # get )

    def compile_expression_list(self):
        """
        structure is:
        (expression ("," expression)* )?

        returns the number of elems in the (expression) e.g. (2 + (3 + 4)) returns 3
        :return int:
        """
        counter = 0
        if self.exist_expression():
            self.compile_expression()
            counter += 1
        while self.next_value_is(","):  # multiple expressions
            self.advance()  # get ,
            self.compile_expression()
            counter += 1
        return counter

    def write_array(self):
        """
        for [expression] cases
        :return:
        """
        self.advance()  # get [
        self.compile_expression()
        self.advance()  # get ]

    def compile_array_index(self, name):
        """
        Reminder 4 kinds: field static argument local(aka var)

        We need to push the base address
        Then push the offset
        Add

        Then these steps come outside of this function:
        And then pop pointer 1, which will store the offsetted address in the THAT pointer
        And then we'll push the value and pop it
        :param name:
        :return:
        """
        self.write_array()
        if name in self.symbol_table.curr_scope:
            if self.symbol_table.kind_of(name) == "var":
                self.vm_writer.write_push("local", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "arg":
                self.vm_writer.write_push("argument", self.symbol_table.index_of(name))
        else:
            if self.symbol_table.kind_of(name) == "static":
                self.vm_writer.write_push("static", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "field":
                self.vm_writer.write_push("this", self.symbol_table.index_of(name))
            else:
                print("ERROR in CE compile_array_index")
        self.vm_writer.write_arithmetic("add")

    def write_push(self, name):
        """
        Reminder 4 kinds: field static argument local(aka var)
        :param name:
        :return:
        """
        if name in self.symbol_table.curr_scope:
            if self.symbol_table.kind_of(name) == "var":
                self.vm_writer.write_push("local", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "arg":
                self.vm_writer.write_push("argument", self.symbol_table.index_of(name))
        else:
            if self.symbol_table.kind_of(name) == "static":
                self.vm_writer.write_push("static", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "field":
                self.vm_writer.write_push("this", self.symbol_table.index_of(name))
            else:
                print("ERROR in CE write_push")

    def write_pop(self, name):
        """
        Reminder 4 kinds: field static argument local(aka var)
        :param name:
        :return:
        """
        if name in self.symbol_table.curr_scope:
            if self.symbol_table.kind_of(name) == "var":
                self.vm_writer.write_pop("local", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "arg":
                self.vm_writer.write_pop("argument", self.symbol_table.index_of(name))
        else:
            if self.symbol_table.kind_of(name) == "static":
                self.vm_writer.write_pop("static", self.symbol_table.index_of(name))
            elif self.symbol_table.kind_of(name) == "field":
                self.vm_writer.write_pop("this", self.symbol_table.index_of(name))
            else:
                print("ERROR in CE write_pop")

    ### End statements
    ##################

    def binary_op(self):
        return {"+", "-", "*", "/", "&", "|", "<", ">", "="}

    def unary_op(self):
        return {"-", "~"}

    def keyword_constant(self):
        return {"true", "false", "null", "this"}

    def advance(self):
        """
        tokenizer.advance() returns the current token
        reminder the token is a tuple of the token type and value e.g. (integerConstant 300)
        :return:
        """
        return self.tokenizer.advance()

    def next_value_in(self, list_of_exp):
        """
        like next_value_is, except only for checking against a list, usually the list of operators
        :param list_of_exp:
        :return boolean:
        """
        token, value = self.tokenizer.peek()
        return value in list_of_exp

    def next_value_is(self, val):
        """
        checks if next value to parse is equal to some condition
        :param val:
        :return boolean:
        """
        token, value = self.tokenizer.peek()
        return value == val

    def next_token_is(self, tok):
        """
        checks if next token to parse is equal to some condition
        :param tok:
        :return boolean:
        """
        token, value = self.tokenizer.peek()
        return token == tok

    def double_peek(self, tok):
        # unsure why this was needed; dont think it's used
        token, value = self.tokenizer.double_peek()
        self.vm_writer.write_arithmetic(token)
        self.vm_writer.write_arithmetic(value)
        return token == tok

    #     deprecated since not writing to XML but to VM
    # def write_nonterminal_start(self, rule):
    #     """
    #     pdf pg 19 https://www.csie.ntu.edu.tw/~cyy/courses/introCS/14fall/lectures/handouts/lec14_compilerI.pdf
    #     non-terminals are everything except (keyword, symbol, constant, or identifier)
    #     If xxx is non-terminal, output:
    #     <xxx>
    #         Recursive code for the body of xxx
    #     </xxx>
    #     :param rule:
    #     :return:
    #     """
    #     self.output_file.write(self.indent + "<" + rule + ">\n")  # e.g. <classVarDec>
    #     self.parsed_rules.append(rule)  # add the rule a list, to pop later for write_nonterminal_end
    #     self.add_indent()
    #
    # def write_nonterminal_end(self):
    #     self.delete_indent()
    #     rule = self.parsed_rules.pop()  # popped from the list created when writing start, LIFO
    #     self.output_file.write(self.indent + "</" + rule + ">\n")  # e.g. </classVarDec>
    #
    # def write_terminal(self, token, value):
    #     """
    #     If xxx is terminal (keyword, symbol, constant, or identifier), output:
    #     <xxx>
    #         xxx value
    #     </xxx>
    #     :param token:
    #     :param value:
    #     :return:
    #     """
    #     self.output_file.write(self.indent + "<" + token + "> " + value + " </" + token + ">\n")
    # def add_indent(self):
    #     """
    #     adds four spaces to indent level
    #     :return:
    #     """
    #     self.indent += "    "
    #
    # def delete_indent(self):
    #     """
    #     removes four spaces to current indent level
    #     :return:
    #     """
    #     self.indent = self.indent[:-4]

