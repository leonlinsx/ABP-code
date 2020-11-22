# References
# https://github.com/itayabu/nand2tetris/tree/master/ex10
# https://github.com/saikumarm4/Nand2Tetris/blob/master/10/Lexical.py
# https://github.com/kronosapiens/nand2tetris/blob/master/projects/10/JackAnalyzer.py

import re
from collections import deque

class JackTokenizer:
    """
    Removes all comments and white space from input stream
    Breaks it into Jack language tokens, as specified by Jack grammar
    Jack grammar from pdf pg 17
    https://www.csie.ntu.edu.tw/~cyy/courses/introCS/14fall/lectures/handouts/lec14_compilerI.pdf

    We're trying to tokenise every "important" item so can convert to VM
    e.g. 300 becomes integerConstant 300 in the stack so that we can further convert it in compiler
    """

    def __init__(self, jack_file_name):
        """
        Opens input file/stream and gets ready to tokenize
        """
        self.tokens = self.load_file(jack_file_name)
        self.curr_token = None
        self.token_type = None
        self.keywords = self.keyword_set()
        self.symbols = self.symbol_set()
        self.tokens = self.tokenise(self.tokens)
        # self.tokens = self.symbol_replace(self.tokens)

    #######
    ### API

    def has_more_tokens(self):
        """
        Do we have more tokens in the input?
        :return boolean:
        """
        return self.tokens

    def advance(self):
        """
        Gets the next token from the input and makes it current token
        Should only be called if has_more_tokens is true
        :return None:
        """
        self.curr_token = self.tokens.popleft()  # unsure if pop or popleft; think popleft for 1st elem

        return self.curr_token

    def curr_token_type(self):
        """
        :return type of current token - keyword, symbol, identifier etc:
        """
        return self.token_type

    def key_word(self):
        """
        Should only be called when token_type is keyword
        :return keyword which is current token:
        """
        pass

    def symbol(self):
        """
        Should only be called when token_type is symbol
        :return character which is the current token:
        """
        return self.curr_token

    def identifier(self):
        """
        Should only be called when token_type is identifier
        :return identifier which is the current token:
        :rtype str:
        """
        return self.curr_token

    def int_val(self):
        """
        Should only be called when token_type is int_const
        :return integer value which is the current token:
        :rtype int:
        """
        return int(self.curr_token)

    def string_val(self):
        """
        Should only be called when token_type is stringConstant
        :return string value of the current token without double quotes:
        :rtype str:
        """
        return self.curr_token

    def peek(self):
        """
        returns the next token but doesn't pop it
        :return:
        """
        if self.has_more_tokens():
            return self.tokens[0]
        else:
            return "PEEK ERROR"

    def double_peek(self):
        """
        returns the next next token but doesn't pop it
        unsure why this was needed; dont think it's used
        :return:
        """
        if self.has_more_tokens():
            return self.tokens[1]
        else:
            return "DOUBLE PEEK ERROR"

    def get_token(self):
        """
        returns type of current token
        :return:
        """
        return self.curr_token[0]

    def get_value(self):
        """
        returns current token value
        :return:
        """
        return self.curr_token[1]

    ### END API
    ###########

    def load_file(self, jack_file_name):
        """
        opens a jack file and returns a string of all non-comment words
        didn't want to use deque since have to parse later for regex
        as a reminder, deques are initialised left to right
        :param jack_file_name:
        :return string:
        """
        with open(jack_file_name, "r") as f:
            contents = f.read() # reminder that read() reads whole file
        # splits contents on newline, strips whitespace before/after, removes any endofline comments
        contents = [line.strip().split("//")[0] for line in contents.split("\n")]
        # handle multiline comments
        is_comment = False
        for i, line in enumerate(contents):
            start, end = line[:2], line[-2:]
            if start == "/*":
                is_comment = True

            # erase comment lines
            if is_comment:
                contents[i] = ""

            # check for end of multiline comment, has to be after the erase
            if start == "*/" or end == "*/":
                is_comment = False
        # for each word in each line in contents, put into a list
        # word refers to anything separated by spaces, will still have to split later with regex
        words = []
        for line in contents:
            line_words = [word for word in line.split() if word]
            words.extend(line_words)

        return ' '.join(words)

    def tokenise(self, word_string):
        """
        uses regex to tokenize every word in a word stack
        :param word_string:
        :return tokenized word stack:
        """
        # want to match only the keyword, and not any text before/after
        # e.g. method fraction foo matches only method
        keywords_regex = "(?!\w)|".join(self.keywords) + "(?!\w)"
        # match a single symbol
        # symbols_regex = r"[\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~]"
        symbols_regex = r"[" + re.escape("|".join(self.symbols)) + "]"
        # match a digit one to unlimited times
        integers_regex = r"\d+"
        # match anything between double quotes, except another double quote or newline
        # note the r'' instead or r""
        strings_regex = r'"[^"\n]*"'
        # match any word character one to unlimited times
        identifiers_regex = r"[\w]+"

        # need to separate everything that's a token, can't just split on spaces
        # e.g. name; becomes name ; -> two tokens
        r = re.compile(keywords_regex + "|" + symbols_regex + "|" + integers_regex + "|"
                                + strings_regex + "|" + identifiers_regex)

        # this splits all the tokens up into one elem in a list
        split_word_stack = r.findall(word_string)

        # the word here is the value of the token
        # so we insert the token type in front of the value for use later
        # e.g. 300 becomes integerConstant 300 in the stack
        tokenised = deque()
        for word in split_word_stack:
            # appending a tuple
            if re.match(keywords_regex, word):
                tokenised.append(("keyword", word))
                self.token_type = "keyword"
            elif re.match(symbols_regex, word):
                tokenised.append(("symbol", word))
                self.token_type = "symbol"
            elif re.match(integers_regex, word):
                tokenised.append(("integerConstant", word))
                self.token_type = "integerConstant"
            elif re.match(strings_regex, word):
                tokenised.append(("stringConstant", word[1:-1]))  # strings without the ""
                self.token_type = "stringConstant"
            else:
                tokenised.append(("identifier", word))
                self.token_type = "identifier"

        return tokenised

    # def symbol_replace(self, word_stack):
    #     """
    #     replaces special symbols in Jack < > " &
    #     the word stack has already been converted to token_type - value pairs per above tokenise()
    #     here we get the pairs for all of the tokens e.g. integerConstant 300
    #     and only replace the values for the special symbols; all else remains same
    #     :return word stack with special symbols replaced:
    #     """
    #     sym_replaced = deque()
    #     for pair in word_stack:
    #         token, value = pair
    #         if value == "<":
    #             sym_replaced.append((token, "&lt;"))
    #         elif value == ">":
    #             sym_replaced.append((token, "&gt;"))
    #         elif value == '"':
    #             sym_replaced.append((token, "&quot;"))
    #         elif value == "&":
    #             sym_replaced.append((token, "&amp;"))
    #         else:  # leave all others alone
    #             sym_replaced.append((token, value))
    #
    #     return sym_replaced

    # unsure why set rather than list, think it's for faster testing
    def keyword_set(self):
        return {"class", "constructor", "function", "method", "field", "static",
                "var", "int", "char", "boolean", "void", "true", "false", "null",
                "this", "let", "do", "if", "else", "while", "return"}

    # unsure why set rather than list, think it's for faster testing
    def symbol_set(self):
        return {"{", "}", "(", ")", "[", "]", ".", ",", ";",
               "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"}
