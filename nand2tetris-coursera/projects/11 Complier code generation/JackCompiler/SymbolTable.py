# References:
# https://github.com/itayabu/nand2tetris/tree/master/ex11
# https://www.cs.huji.ac.il/course/2002/nand2tet/docs/ch_11_compiler_II.pdf

class SymbolTable:
    """
    A symbol table that associates names with information needed for Jack compilation: type, kind, and
    running index. The symbol table has 2 nested scopes (class/subroutine).

    The following kinds of identifiers may appear:
    Static: Scope: class.
    Field: Scope: class.
    Argument: Scope: subroutine (method/function/constructor).
    Var: Scope: subroutine (method/function/constructor).

    e.g. x may be stored as name:x type:int kind:field index:0
    e.g. pointCount may be stored as name:pointCount type:int field:static index:0

    When compiling code, any identifier not found in the symbol table may be assumed to be
    a subroutine name or a class name.
    """

    def __init__(self):
        """
        Creates a new empty symbol table
        """
        # since we want to associate names with something, makes sense to create a dictionary, which is hashable
        # https://lerner.co.il/2015/04/03/is-it-hashable-fun-and-games-with-hashing-in-python/
        # one for the class table
        self.class_scope = {}
        # one for the subroutine table
        self.subroutine_scope = {}
        # set current scope to be class when starting, will change this to subroutine and back when needed
        self.curr_scope = self.class_scope
        # class initialisation
        self.field_counter = 0
        self.static_counter = 0
        # subroutine initialisation
        self.arg_counter = 0
        self.var_counter = 0
        self.if_Counter = 0
        self.while_counter = 0

    def start_subroutine(self, name):
        """
        This is supposed to start a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)
        But the code seems to create a new entry for that particular var in the subroutine table
        i.e. it erases a single key/value in the subroutine dict rather than the entire dict
        """
        # create a key in the subroutine dict with the key's name
        # we'll associate type/kind/idx to this name later
        # note
        self.subroutine_scope[name] = {}
        self.arg_counter = 0
        self.var_counter = 0
        self.if_Counter = 0
        self.while_counter = 0

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.
        e.g. field int x becomes name:x type:int kind:field #:0, in a dict format x: (int, field, 0)
        :param name:
        :param type:
        :param kind:
        :return:
        """
        # associate the tuple with the name in the class symbol table
        if kind == "field":
            self.class_scope[name] = (type, kind, self.field_counter)
            self.field_counter += 1
        elif kind == "static":
            self.class_scope[name] = (type, kind, self.static_counter)
            self.static_counter += 1
        # associate tuple with the name in current subroutine symbol table
        # note it's curr_scope, not subroutine_scope
        elif kind == "arg":
            self.curr_scope[name] = (type, kind, self.arg_counter)
            self.arg_counter += 1
        elif kind == "var":
            self.curr_scope[name] = (type, kind, self.var_counter)
            self.var_counter += 1
        else:
            print("ERROR in identifier kind")

    def class_var_count(self, kind):
        """
        Returns number of vars of given kind already defined in class global scope
        Useful for when creating a constructor
        Reminder 4 kinds: field static argument local(aka var)
        :param kind:
        :return:
        """
        return len([value for key, value in self.class_scope.items() if value[1] == kind])

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current scope.
        :param kind:
        :return int:
        """
        # check if value[1], idx of kind in the symbol table, is == argument passed
        return len([value for key, value in self.curr_scope.items() if value[1] == kind])

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope dictionary/symbol table.
        Checks class scope if not in current scope
        Returns NONE if the identifier is unknown in any scope
        :param name:
        :return STATIC FIELD ARG VAR NONE:
        """
        # kind is in idx 1
        if name in self.curr_scope:
            return self.curr_scope[name][1]
        # if not found, check global class scope
        elif name in self.class_scope:
            return self.class_scope[name][1]
        else:
            return "NONE"

    def type_of(self, name):
        """
        Returns the type of the named identifier in the current scope.
        :param name:
        :return string:
        """
        # type in idx 0
        if name in self.curr_scope:
            return self.curr_scope[name][0]
        elif name in self.class_scope:
            return self.class_scope[name][0]
        else:
            return "NONE"

    def index_of(self, name):
        """
        Returns the index # assigned to named identifier
        :param name:
        :return int:
        """
        if name in self.curr_scope:
            return self.curr_scope[name][2]
        elif name in self.class_scope:
            return self.class_scope[name][2]
        else:
            return "NONE"

    def set_scope(self, name):
        """
        sets scope to global class or subroutine
        :param name:
        :return:
        """
        if name == "global":
            self.curr_scope = self.class_scope
        else:
            self.curr_scope = self.subroutine_scope[name]