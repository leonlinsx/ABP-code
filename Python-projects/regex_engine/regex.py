# jetbrains academy regex engine
# builds a regex engine from scratch without the re module
# includes special metacharacters
# includes 2 deprecated versions
# many solutions on jetbrains don't actually work for all test cases

# compares single chars
def single_char(regex, string):

    if regex == "." and len(string) == 1:
        regex = string
    # if regex exhausted
    if not regex:
        return True
    # elif still have regex, and no string
    elif not string:
        return False
    elif regex == string:
        return True
    else:
        return False

# main matching function
def match(regex, string):
    metachar_list = ["?", "*", "+"]
    regex = regex.strip("\\")

    if not regex:
        return True
    elif not string and regex[0] == "$":
        return True
    elif not string and regex[0] != "$":
        return False
    else:
        # if regex has metachar, call that function
        # excludes cases when metachar was escaped
        # \ is an escape in python too, so need to \\
        if len(regex) > 1 and regex[1] in metachar_list and regex[0] != "\\":
            return metachar(regex, string)
        else:
            # if not metachars, slice both regex and string if first char matches
            if single_char(regex[0], string[0]):
                return match(regex[1:], string[1:])
            else:
                return False

# compares unequal length
def unequal_length(regex, string):

    # checks for case when regex is empty, that always returns true
    if not regex:
        return True
    elif not string:
        return False
    else:
        # if not, then loop through the text slice one at a time until slice ends
        for i in range(len(string)):
            str_slice = string[i:]
            if match(regex, str_slice):
                return True
            else:
                continue
        return False

# add ^ and $ characters
# ^ can occur at the beginning of the regex,
# and it means that the following regex should be matched only at the beginning of the input string.
# $ can occur at the end of the regex,
# and it means that the preceding regex should be matched only at the end of the input string.
def start_end(regex, string):

    # slice out the ^
    if "^" in regex:
        regex = regex[1:]
        return match(regex, string)
    # this works because the match function accounts for $
    elif "$" in regex:
        return unequal_length(regex, string)
    # unnecessary but makes code clearer
    else:
        return unequal_length(regex, string)

# add support for ? * +
def metachar(regex, string):

    # check the second char of regex (not the first)
    if regex[1] == "?":
        return question(regex, string)
    elif regex[1] == "*":
        return mult(regex, string)
    elif regex[1] == "+":
        return plus(regex, string)
    # not needed but error catch
    else:
        return "metachar_error"

# ? matches the preceding character zero times or once
def question(regex, string):

    # if first char matches, slice out regex and word, return recursive
    if single_char(regex[0], string[0]):
        return match(regex[2:], string[1:])
    # if no match, slice out the regex but don't slice the word (zero times)
    else:
        return match(regex[2:], string)

# * matches the preceding character zero or more times;
def mult(regex, string):

    if single_char(regex[0], string[0]):
        # if string about to run out but matched, slice and check rest of regex
        # this is in case regex has more wildcards that could still return true
        if len(string) == 1:
            return match(regex[2:], string)
        else:
            # 3 cases here: 1) regex len > 3 with a wildcard first char e.g. .+c against ooeec
            # because of the wildcard, need to keep regex until regex[2] == string[1],
            # where we slice both regex and word
            if len(regex) >= 3 and regex[0] == "." and len(string) >= 2:
                if regex[2] == string[1]:
                    return match(regex[2:], string[1:])
                else:
                    return match(regex, string[1:])
            # 2) string[1] == string[0], e.g. matching c+text against ccctext
            # in which case slice string by one char to check regex again (once or more times)
            elif single_char(string[0], string[1]):
                return match(regex, string[1:])
            # 3) not equal, e.g. matching c+text against ctext
            # in which case move on with regex
            else:
                return match(regex[2:], string[1:])
    # if no match, slice out the regex but don't slice the word
    else:
        return match(regex[2:], string)

# + matches the preceding character once or more times.
def plus(regex, string):

    if single_char(regex[0], string[0]):
        if len(string) == 1:
            # because + has to match at least once,
            # we need to check the case of regex len >= 3 .+char against string char
            # that returns false, since you need at least two chars in the string
            if len(regex) >= 3 and regex[0] == ".":
                return False
            else:
                return match(regex[2:], string)
        else:
            # 3 cases here: 1) regex len >= 3 with a wildcard first char e.g. .+c against ooeec
            # because of the wildcard, need to keep regex until regex[2] == string[1],
            # where we slice both regex and word
            if len(regex) >= 3 and regex[0] == "." and len(string) >= 2:

                if regex[2] == string[1]:
                    return match(regex[2:], string[1:])
                else:
                    return match(regex, string[1:])
            # 2) string[1] == string[0], e.g. matching c+text against ccctext
            # in which case slice string by one char to check regex again (once or more times)
            elif single_char(string[0], string[1]):
                return match(regex, string[1:])
            # 3) not equal, e.g. matching c+text against ctext
            # in which case move on with regex
            else:
                return match(regex[2:], string[1:])
    # unlike the other meta chars, this has to match >= 1
    else:
        return False

def main():
    regex, text = input("Enter text input split by |").split("|")
    print(start_end(regex, text))

if __name__ == "__main__":
    main()

############################################################################
# deprecated v 2.0
# def match(regex, text):
#     len_re = len(regex)
#     # unsure
#     char = regex[2] if len_re > 2 else ""
#
#     # if regex exhausted, True.
#     if not regex:
#         return True
#     # don't have to take care of $ char case since already sliced out
#     elif not text:
#         return False
#
#     # ? matches the preceding character zero times or once
#     elif len_re > 1 and regex[1] == "?":
#         # if first char matches, slice out regex and word, return recursive
#         if regex[0] == text[0]:
#             return match(regex[2:], text[1:])
#         # if no match, slice out the regex but don't slice the word
#         else:
#             return match(regex[2:], text)
#
#     # * matches the preceding character zero or more times;
#     elif len_re > 1 and regex[1] == "*":
#         # if first char matches, slice out word only, and check again
#         if regex[0] == text[0] or (char and regex[0] == "." and text[0] != regex[2]):
#             return match(regex, text[1:])
#         # if no match, slice out the regex but don't slice the word
#         else:
#             return match(regex[2:], text)
#
#     # + matches the preceding character once or more times.
#     elif len_re > 1 and regex[1] == "+":
#         if not char:
#             return True
#         # if first char matches, true
#         if regex[0] == text[0] or (char and regex[0] == "." and text[0] != regex[2]):
#             return True
#         else:
#             return False
#
#     # . matches anything, so slice out both regex and word
#     elif regex[0] == ".":
#         return match(regex[1:], text[1:])
#     elif regex[0] == text[0]:
#         return match(regex[1:], text[1:])
#     else:
#         return False
#
# # takes a regex and text as str and returns boolean if matches
# # deals with ^ and $ characters, checks if regex or text exhausted
# # calls the match function for other metachars
# def regex_engine(regex, text):
#     # if regex exhausted, True.
#     # if regex not exhausted but text is, False
#     if not regex:
#         return True
#     elif not text:
#         return False
#
#     # ^ can occur at the beginning of the regex,
#     # and it means that the following regex should be matched only at the beginning of the input string.
#     if regex.startswith("^"):
#         # slice out the ^ char up to text length and see if remainder matches
#         # if it does, continue with recursive function
#         if match(regex[1:len(text)], text):
#             regex = regex[1:]
#         else:
#             return False
#
#     # $ can occur at the end of the regex,
#     # and it means that the preceding regex should be matched only at the end of the input string.
#     # not an elif because testing both ^ and $
#     if regex.endswith("$"):
#         # slice out the $ char and see if remainder matches
#         pos_max = max(regex.find('?'), regex.find('*'), regex.find('+'))
#         end_regex = regex[pos_max + 1:]
#         if end_regex[:-1]:
#             return match(end_regex[:-1], text[-len(end_regex[:-1]):])
#         else:
#             return False
#
#     # slice the text off by 1 (if unequal lengths) if haven't matched yet
#     if match(regex, text):
#         return True
#     else:
#         return regex_engine(regex, text[1:])
############################################################################
# deprecated v 1.0
# # compares single characters
# def re_char(regex, char):
#
#     if (regex == char or regex == "" or (regex == "." and len(char) == 1)):
#         return True
#     else:
#         return False
#
# # compares equal length strings
# def re_str_equal(regex, text):
#
#     # check if regex exhausted; if so return true
#     if regex:
#         # if still have regex remaining and text
#         if text:
#             # if chars match, move on to next char in strings, return recursively
#             if re_char(regex[0], text[0]):
#                 regex = regex[1:]
#                 text = text[1:]
#                 return re_str_equal(regex, text)
#             else:
#                 return False
#         # if still have regex remaining but no text, return True if regex is $
#         else:
#             if regex[0] == "$":
#                 return True
#             else:
#                 return False
#     else:
#         return True
#
# # compares unequal length strings
# def re_str_unequal(regex, text):
#     # checks for case when regex is empty, that always returns true
#     if regex:
#         # if not, then loop through the text slice one at a time until slice ends
#         for i in range(len(text)):
#             text_slice = text[i:]
#             if re_str_equal(regex, text_slice):
#                 return True
#             else:
#                 continue
#         return False
#     else:
#         return True
#
# # add ^ and $ characters
# # ^ can occur at the beginning of the regex,
# # and it means that the following regex should be matched only at the beginning of the input string.
# # $ can occur at the end of the regex,
# # and it means that the preceding regex should be matched only at the end of the input string.
# def re_start_end(regex, text):
#     if "^" in regex:
#         regex_slice = regex[1:]
#         return re_str_equal(regex_slice, text) # since it's at beginning, if regex is exhausted it's a match
#     elif "$" in regex:
#         return re_str_unequal(regex, text) # since it's at end, have to slice the text
#     else:
#         return re_str_unequal(regex, text)