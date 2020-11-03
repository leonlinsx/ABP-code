'''
jetbrains academy calculator
calculator class that can take inputs and do math with basic operators
+ - * / (int division) and () are supported
can also store variables by setting with = sign
does not use eval(), works with strings and regex

Other references

https://levelup.gitconnected.com/how-to-write-a-formula-string-parser-in-python-5362210afeab

'''

import sys
import re 
from collections import deque

class Calculator:
    def __init__(self):
        self.var_dict = {}
        
    def main(self):
        while True:
            print("Enter an expression or type /help for help and /exit to exit")
            text = input()
            # handle empty lines
            if not text:
                continue
            # handle commands
            elif text.startswith("/"):
                self.menu_command(text)
            # handle assignment attempt
            elif any(c == "=" for c in text):
                self.var_assign(text)
            # remaining are either single variable or math operations
            else:    
                # handle for any alphabet in text, without equals sign
                if len(text.strip().split(" ")) == 1:
                    self.var_get(text)
                else:
                    try:
                        text = self.clean_text(text)
                        text = self.postfix_conv(text)
                        print(self.postfix_eval(text))
                    except:
                        print("Invalid expression")
    
    def menu_command(self, text):
        # options for user commands, starting with /
        if text == "/exit":
            self.exit()
        elif text == "/help":
            self.help()
        else:
            print("Unknown command")

    def exit(self):
        print("Bye!")
        sys.exit()
    
    def help(self):
        print("The program evaluates a string of expressions with any number of symbols between integers")
        print('The program should print "Invalid expression" in cases when the given expression has an invalid format.')
        print('If a user enters an invalid command, the program must print "Unknown command"\n')
        print("The program also accepts variable assignment")
        print('The program should print "Invalid identifier" if the left part of the assignment is incorrect.') 
        print('If the part after the "=" is wrong then use the "Invalid assignment". First we should check the left side.\n')
        print("The program takes addition (+), subtraction (-), multiplication (*), integer division (/), and parantheses")
        print("The program converts to reverse polish notation in order to evaluate")
        
    def var_assign(self, text):
        # takes a text with any number of equals signs, rejects all with >1 equal sign
        # does variable assignment to object dictionary
        var_list = text.split("=")
        # should only have two vars, one on left and one on right
        if len(var_list) >= 3:
            print("Invalid assignment")
        else:
            # get the left and right vars, stripped of spaces
            left, right = var_list[0].strip(), var_list[1].strip()
            # check left and right
            if any(c.isdigit() for c in left):
                print("Invalid identifier")
            # if it has both digit and alpha
            elif any(c.isdigit() for c in right) and any(c.isalpha() for c in right):
                print("Invalid assignment")
            # if only alpha, check if unknown
            elif right.isalpha():
                if right not in self.var_dict:
                    print("Unknown variable")
                else:
                    self.var_dict[left] = self.var_dict[right]
            else:
                self.var_dict[left] = right
            
    def var_get(self, text):
        # takes a text that does not have equals sign but does have alphabet
        # returns the value associated with the var "key" in dict
        # if combo of num and alpha, invalid
        if any(c.isdigit() for c in text):
            print("Invalid identifier")
        # # if still have space, invalid -> tester doesn't like this error catch
        # elif len(text.split(" ")) > 1:
        #     print("Invalid identifier")
        elif text in self.var_dict:
            print(self.var_dict[text])
        else:
            print("Unknown variable")
    
    def clean_text(self, text):
        # cleans up the input for conversion and returns a clean infix notation with spaces in between 
        # also adds 0 in front to reduce hassle of dealing with negative numbers
        # first, remove all spaces
        text = text.replace(" ", "")
        # while still can find unclean text; use search (anywhere) and not match (start)
        while re.search(r"\+{2,}|\+\-|\-\+|\-{2}", text):
            # any time 2 or more + signs
            text = re.sub(r"\+{2,}", "+", text)
            # any +- occurrence
            text = re.sub(r"\+\-", "-", text)
            # any -+ occurrence
            text = re.sub(r"\-\+", "-", text)
            # any time 2 (and only 2) - signs; leave alone if 1 sign. 
            # i.e. only deals with even number of consecutive - signs
            text = re.sub(r"\-{2}", "+", text)
        
        # add spaces between operators for easier parsing later
        text = text.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").replace("(", " ( ").replace(")", " ) ").replace("  ", " ")
        
        # add 0 in front to make parsing if first num is -ve easier
        if text[0] == "-":
            return "0 " + text
        else:
            return text
    
    # http://www.cs.nthu.edu.tw/~wkhon/ds/ds10/tutorial/tutorial2.pdf
    # https://runestone.academy/runestone/books/published/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    def postfix_conv(self, text):
        # takes a cleaned input string and converts from infix to postfix string
        # create a precedence/priority dictionary; higher precedence takes priority
        precedence = {"(" : 1, "+" : 2, "-" : 2, "*" : 3, "/" : 3}
        # setup the stack, empty result list, and split the (cleaned) input
        op_stack = deque()
        postfix_list = []
        text_list = text.strip().split(" ")

        for text in text_list:
            if text not in ("(", "+", "-", "*", "/", ")"):
                postfix_list.append(text)
            # If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
            elif (not op_stack) or op_stack[-1] == "(":
                op_stack.append(text)
            # If the incoming element is a left parenthesis, push it on the stack.
            elif text == "(":
                op_stack.append(text)
            # If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. 
            # Discard the pair of parentheses.
            elif text == ")":
                top_text = op_stack.pop()
                # since we pop in the loop, it'll pop the left paranthesis as well but not append it
                while top_text != "(":
                    postfix_list.append(top_text)
                    top_text = op_stack.pop()
            else:
                # If the incoming operator has lower or equal precedence than or to the top of the stack, 
                # pop the stack and add operators to the result 
                # until you see an operator that has a smaller precedence or a left parenthesis on the top of the stack; 
                # then add the incoming operator to the stack.
                # can just test list falsy, no need len https://stackoverflow.com/questions/48640251/how-to-peek-front-of-deque-without-popping
                while (op_stack) and (precedence[text] <= precedence[op_stack[-1]]):
                    postfix_list.append(op_stack.pop())
                # this also takes care of case when operator has higher precedence and is pushed immediately
                op_stack.append(text) 
        
        # At the end of the expression, pop the stack and add all operators to the result.        
        while op_stack:
            postfix_list.append(op_stack.pop())
            
        return " ".join(postfix_list)
        
    def postfix_eval(self, text):
        # takes a postfix string and evaluates the expression
        # able to deal with variables as well
        op_stack = deque()
        elem_list = text.split(" ")

        for elem in elem_list:
            # If the incoming element is a number, push it into the stack (the whole number, not a single digit!).
            if elem.isdigit():
                op_stack.append(int(elem))
            # If the incoming element is the name of a variable, push its value into the stack.
            elif elem in self.var_dict.keys():
                op_stack.append(int(self.var_dict[elem]))
            # If the incoming element is an operator, then pop twice to get two numbers and perform the operation; 
            # Note the reverse order num2 and num1
            # push the result on the stack. 
            else:
                num2 = op_stack.pop()
                num1 = op_stack.pop()
                if elem == "+":
                    num3 = num1 + num2 
                elif elem == "-":
                    num3 = num1 - num2
                elif elem == "*":
                    num3 = num1 * num2
                elif elem == "/":
                    num3 = num1 // num2 # test is only integer division
                op_stack.append(num3)
        
        # When the expression ends, the number on the top of the stack is a final result. 
        return op_stack.pop()
        
    def add_sub(self, text):
        # takes a text of integers and operators together, adds them, returns result
        num_sign_list = text.split(" ")
        # convert any variables in the list to ints
        num_sign_list = [self.var_dict[c] if c in self.var_dict else c for c in num_sign_list]
        
        res_list = []
        # add the first number to array, to allow rest of range to work
        # if + sign in front, slice out the operator
        if num_sign_list[0].startswith("+"):
            res_list.append(int(num_sign_list[0][1:]))
        elif num_sign_list[0].startswith("-"):
            res_list.append(int(num_sign_list[0]))
        else: 
            res_list.append(int(num_sign_list[0]))
        
        # parse each operation and number from index 1 onwards
        if len(num_sign_list) >= 3:
            for i in range(1, len(num_sign_list), 2):
                curr_operation, curr_num = num_sign_list[i], int(num_sign_list[i + 1])
                if curr_operation.startswith("+"):
                    res_list.append(curr_num)
                elif curr_operation.startswith("-"):
                    if curr_operation.count("-") % 2 == 1:
                        res_list.append(curr_num * -1)
                    else:
                        res_list.append(curr_num)
            
        return sum(res_list)

    def add_text_list(self, text):
        # takes a text of integers with spaces together, adds them, prints result
        num_list = list(map(int, text.split()))
        print(sum(num_list))
           
calculator = Calculator()
calculator.main()

