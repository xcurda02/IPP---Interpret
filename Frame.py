from Stack import Stack
from ErrCodes import *
import copy
import sys

# Promenna
class Variable:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.data_type = None

# Trida definujici samostatny ramec a operace nad nim
class Frame:
    def __init__(self):
        self.var_array = []

    # Vraci objekt typu Variable
    def get_var(self, var_name):
        for var in self.var_array:
            if var.name == var_name:
                return var
        raise MyException(ErrCodes.NONEXISTENT_VARIABLE)

    # Zjsiteni existence promenne v ramci
    def var_exists(self, var_name):
        for var in self.var_array:
            if var.name == var_name:
                return True
        return False

    # Pridani promenne
    def add_var(self, var_name):
        variable = Variable(var_name)
        self.var_array.append(variable)

    # Aktualizace atributu promenne
    def update_var(self, var_name, value, data_type):
        var = self.get_var(var_name)
        var.value = value
        var.data_type = data_type

    # Vypsani promenne na stderr
    def print_vars(self):
        for var in self.var_array:
            sys.stderr.write("%s: %s," % (var.name, var.value))
        sys.stderr.write('\n')

    def clear(self):
        self.var_array.clear()

    def var_count(self):
        return len(self.var_array)

# Konstanty pro snadnejsi praci s ramcemi, mohlo se to resit jeste slovnikem, ale uz se mi to nechtelo vse predelavat
# i kdyz by to byla elegantnejsi varinta
GF = 0
LF = 1
TF = 2

class Frames:

    # pro usnadneni ipmlementace je vytvoreno pole pro pristup ke vsem pristupnym ramcum
    # LF tedy neni implementovan primo na vrcholu zasobniku, ale chova se tak.
    # Pri pushnuti TF na zasobnik se ve skutecnosti pushne LF na zasobnik
    # a TF presune do LF

    def __init__(self):

        self.frame = [None, None, None]             # Pole ramcu(GF,LF,TF)
        self.frame[GF] = Frame()                    # Vytvoreni GF ramce
        self.var_count = 0                          # Aktualni pocet promennych ve vsch ramcich
        self.max_var_count = 0                      # Maximalni pocet promennych v ramcich

        self.frame_stack = Stack()                  # Zasobnik ramcu

    # Instrukce CREATEFRAME
    def create_frame(self):
        if self.frame[TF] is not None:
            self.var_count -= self.frame[TF].var_count()
            self.max_var_count = max(self.var_count, self.max_var_count)
            self.frame[TF].clear()
            self.frame[TF] = None
        self.frame[TF] = Frame()

    # Instrukce PUSHFRAME
    def push_frame(self):
        if self.frame[TF] is None:
            raise MyException(ErrCodes.NONEXISTENT_FRAME)

        if self.frame[LF] is not None:
            self.frame_stack.push(copy.deepcopy(self.frame[LF]))
            self.frame[LF].clear()
            self.frame[LF] = None

        self.frame[LF] = copy.deepcopy(self.frame[TF])
        self.frame[TF].clear()
        self.frame[TF] = None

    # Instrkce POPFRAME
    def pop_frame(self):
        if self.frame[LF] is None:
            raise MyException(ErrCodes.NONEXISTENT_FRAME)

        if self.frame[TF] is not None:
            self.var_count -= self.frame[TF].var_count()
            self.max_var_count = max(self.var_count, self.max_var_count)
            self.frame[TF].clear()
            self.frame[TF] = None

        self.frame[TF] = copy.deepcopy(self.frame[LF])

        if self.frame_stack.peek() is not None:
            self.frame[LF].clear()
            self.frame[LF] = None
            self.frame[LF] = copy.deepcopy(self.frame_stack.pop())
        else:
            self.frame[LF] = None

    # Ziskani promenne z ramce
    def get_var(self, frame, var_name):

        if self.frame[frame] is None:
            raise MyException(ErrCodes.NONEXISTENT_FRAME)

        return self.frame[frame].get_var(var_name)

    # Pridani promenne
    def add_var(self, frame, var_name):

        if self.frame[frame] is None:
            raise MyException(ErrCodes.NONEXISTENT_FRAME)

        if self.frame[frame].var_exists(var_name):
            self.frame[frame].update_var(var_name, None, None)
        else:
            self.frame[frame].add_var(var_name)
            self.var_count += 1
            self.max_var_count = max(self.max_var_count, self.var_count)

    # Aktualizace promenne
    def update_var(self, frame, var_name, value, data_type):
        if self.frame[frame] is None:
            raise MyException(ErrCodes.NONEXISTENT_FRAME)

        if value is None:
            raise MyException(ErrCodes.MISSING_VALUE)

        self.frame[frame].update_var(var_name, value, data_type)

    # Vypis promennych ve vsech ramcich na stderr
    def print_vars(self):
        if self.frame[TF] is not None:
            sys.stderr.write("TF: ")
            self.frame[TF].print_vars()
        else:
            sys.stderr.write("TF: None\n")

        if self.frame[LF] is not None:
            sys.stderr.write("LF: ")
            self.frame[LF].print_vars()
        else:
            sys.stderr.write("LF: None\n")

        if self.frame[GF] is not None:
            sys.stderr.write("GF: ")
            self.frame[GF].print_vars()
        else:
            sys.stderr.write("GF: None\n")