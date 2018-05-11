from Frame import Frames
from FileParser import FileParser
from Stack import Stack
from ErrCodes import *
from Syntax import Syntax as syntax
import sys


class Interpreter:

    def __init__(self, element_tree):
        self.input = FileParser(element_tree)
        self.frame = Frames()           # Objekt obsahujici ramce
        self.call_stack = Stack()       # Zasobnik volani
        self.data_stack = Stack()       # Datovy zasobnik
        self.label_dict = dict()        # Slovnik, pro ukladani labelu a jejich pozice v kodu
        self.ins_count = 0              # pocitadlo probehnutych instrukci
        self.pc = 1                     # Program counter

    # Hlavni smycka interpretace kodu
    def run_code(self):
        self.input.validate_header()        # Urceni spravosti elementu <program> ve vstupnim XML
        self.get_labels()                   # Scan celeho kodu za ucelem zjisteni existujicich labelu
        while not self.input.end:
            self.INS()
            self.pc += 1
            self.ins_count += 1
            self.input.next_instruction()

    # Vraci pocet maxima promennych (rozsireni STATI)
    def get_vars(self):
        return self.frame.max_var_count

    # Scan celeho kodu za ucelem zjisteni existujicich labelu
    def get_labels(self):
        while not self.input.end:
            order, opcode = self.input.get_ins()
            if opcode == 'LABEL':

                args = self.input.get_args()
                syntax.args_syntax(args)

                if len(args) != 1:
                    raise MyException(ErrCodes.XML_FORMAT)

                if args[0]['type'] != 'label':
                    raise MyException(ErrCodes.OPERAND)

                if self.label_exists(args[0]['value']):
                    raise MyException(ErrCodes.SEMANTIC)

                self.label_dict[args[0]['value']] = self.pc

            self.input.next_instruction()
            self.pc += 1

        self.pc = 1
        self.input.set_ins_iterator()

    # Zjisteni existence labelu
    def label_exists(self, label):
        if label in self.label_dict:
            return True
        return False

    # Interpretace jednotlive instrukce
    def INS(self):
        order, opcode = self.input.get_ins()    # Ziskani operacniho kodu instrukce a jejiho poradi
        args = self.input.get_args()            # Ziskani argumentu instrukce(operandu)

        #DEBUG vypisy
        #print("order : %s  opcode: %s" % (order, opcode))
        #print("args :%s" % args)

        syntax.args_syntax(args)                # Kontrola syntaxe argumentu instrukce

        # Kontrola spravnosti artibutu order u instrukci
        if order != self.pc:
            raise MyException(ErrCodes.XML_FORMAT)

        # Prepinac na jednotlive instrukce
        if opcode == "CLEARS":
            self.CLEARS(args)

        elif opcode == "ADDS":
            self.ADDS(args)

        elif opcode == "SUBS":
            self.SUBS(args)

        elif opcode == "MULS":
            self.MULS(args)

        elif opcode == "IDIVS":
            self.IDIVS(args)

        elif opcode == "LTS":
            self.LTS(args)

        elif opcode == "GTS":
            self.GTS(args)

        elif opcode == "EQS":
            self.EQS(args)

        elif opcode == "ANDS":
            self.ANDS(args)

        elif opcode == "ORS":
            self.ORS(args)

        elif opcode == "NOTS":
            self.NOTS(args)

        elif opcode == "INT2CHARS":
            self.INT2CHARS(args)

        elif opcode == "STRI2INTS":
            self.STRI2INTS(args)

        elif opcode == "JUMPIFEQS":
            self.JUMPIFEQS(args)

        elif opcode == "JUMPIFNEQS":
            self.JUMPIFNEQS(args)

        elif opcode == "INT2FLOAT":
            self.INT2FLOAT(args)

        elif opcode == "FLOAT2INT":
            self.FLOAT2INT(args)

        elif opcode == "MOVE":
            self.MOVE(args)

        elif opcode == "CREATEFRAME":
           self.CREATEFRAME(args)

        elif opcode == "PUSHFRAME":
            self.PUSHFRAME(args)

        elif opcode == "POPFRAME":
            self.POPFRAME(args)

        elif opcode == "DEFVAR":
            self.DEFVAR(args)

        elif opcode == "CALL":
            self.CALL(args)

        elif opcode == "RETURN":
            self.RETURN(args)

        elif opcode == "PUSHS":
            self.PUSHS(args)

        elif opcode == "POPS":
            self.POPS(args)

        elif opcode == "ADD":
            self.ADD(args)

        elif opcode == "SUB":
            self.SUB(args)

        elif opcode == "MUL":
            self.MUL(args)

        elif opcode == "IDIV":
            self.IDIV(args)

        elif opcode == "LT":
            self.LT(args)

        elif opcode == "GT":
            self.GT(args)

        elif opcode == "EQ":
            self.EQ(args)

        elif opcode == "AND":
            self.AND(args)

        elif opcode == "OR":
            self.OR(args)

        elif opcode == "NOT":
            self.NOT(args)

        elif opcode == "INT2CHAR":
            self.INT2CHAR(args)

        elif opcode == "STRI2INT":
            self.STRI2INT(args)

        elif opcode == "READ":
            self.READ(args)

        elif opcode == "WRITE":
            self.WRITE(args)

        elif opcode == "CONCAT":
            self.CONCAT(args)

        elif opcode == "STRLEN":
            self.STRLEN(args)

        elif opcode == "GETCHAR":
            self.GETCHAR(args)

        elif opcode == "SETCHAR":
            self.SETCHAR(args)

        elif opcode == "TYPE":
            self.TYPE(args)

        elif opcode == "LABEL":
            #Labely uz byly zjisteny a zkontrolovany
            pass
        elif opcode == "JUMP":
            self.JUMP(args)

        elif opcode == "JUMPIFEQ":
            self.JUMPIFEQ(args)

        elif opcode == "JUMPIFNEQ":
            self.JUMPIFNEQ(args)

        elif opcode == "DPRINT":
            self.DPRINT(args)

        elif opcode == "BREAK":
            self.BREAK(args)

        else: #neznamy operacni kod
            raise MyException(ErrCodes.LEX_SYNTAX)

    ############### Implementace jednotlivych instrukci ###################
    #######################################################################

    def CLEARS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)

        self.data_stack.clear()

    def ADDS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if not self.comp_arit_types(symb_1['type'], symb_2['type']):
            raise MyException(ErrCodes.SEMANTIC)


        item = dict()
        item['type'] = symb_2['type']
        item['value'] = symb_1['value'] + symb_2['value']

        self.data_stack.push(item)

    def SUBS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if not self.comp_arit_types(symb_1['type'], symb_2['type']):
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = symb_1['value'] - symb_2['value']
        item['type'] = symb_2['type']

        self.data_stack.push(item)

    def MULS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if not self.comp_arit_types(symb_1['type'], symb_2['type']):
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = symb_1['value'] * symb_2['value']
        item['type'] = symb_2['type']

        self.data_stack.push(item)

    def IDIVS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if not self.comp_arit_types(symb_1['type'], symb_2['type']):
            raise MyException(ErrCodes.SEMANTIC)

        if symb_2['value'] == 0:
            raise MyException(ErrCodes.ZERO_DIVISION)

        item = dict()
        item['value'] = symb_1['value'] / symb_2['value']
        item['type'] = symb_2['type']

        self.data_stack.push(item)

    def LTS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != symb_2['type']:
            raise MyException(ErrCodes.SEMANTIC)


        item = dict()
        item['value'] = symb_1['value'] < symb_2['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def GTS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != symb_2['type']:
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = symb_1['value'] > symb_2['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def EQS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != symb_2['type']:
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = symb_2['value'] == symb_1['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def ANDS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != 'bool' or symb_2['type'] != 'bool':
            raise MyException(ErrCodes.SEMANTIC)



        item = dict()
        item['value'] = symb_2['value'] and symb_1['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def ORS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != 'bool' or symb_2['type'] != 'bool':
            raise MyException(ErrCodes.SEMANTIC)


        item = dict()
        item['value'] = symb_2['value'] or symb_1['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def NOTS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != 'bool':
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = not symb_1['value']
        item['type'] = 'bool'

        self.data_stack.push(item)

    def INT2CHARS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = chr(symb_1['value'])
        item['type'] = 'string'

        self.data_stack.push(item)

    def STRI2INTS(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_2['type'] != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        if symb_1['type'] != 'string':
            raise MyException(ErrCodes.SEMANTIC)

        item = dict()
        item['value'] = ord(symb_1['value'][symb_2['value']])
        item['type'] = 'int'

        self.data_stack.push(item)

    def JUMPIFEQS(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != symb_2['type']:
            raise MyException(ErrCodes.SEMANTIC)

        if symb_1['value'] == symb_2['value']:
            if not self.label_exists(label):
                raise MyException(ErrCodes.SEMANTIC)
            self.input.set_ins_iterator(self.label_dict[label]-1)
            self.pc = self.label_dict[label] - 1

    def JUMPIFNEQS(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']
        try:
            symb_2 = self.data_stack.pop()
            symb_1 = self.data_stack.pop()
        except IndexError:
            raise MyException(ErrCodes.MISSING_VALUE)

        if symb_1['type'] != symb_2['type']:
            raise MyException(ErrCodes.SEMANTIC)

        if symb_1['value'] != symb_2['value']:
            if not self.label_exists(label):
                raise MyException(ErrCodes.SEMANTIC)
            self.input.set_ins_iterator(self.label_dict[label]-1)
            self.pc = self.label_dict[label] - 1


    def INT2FLOAT(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])
        s1_data_type, s1_value = self.SYMB(args[1])

        if s1_data_type != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, float(s1_value), 'float')

    def FLOAT2INT(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])
        s1_data_type, s1_value = self.SYMB(args[1])

        if s1_data_type != 'float':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, int(s1_value), 'int')

    def MOVE(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])       # 1. argument
        s1_data_type, s1_value = self.SYMB(args[1])

        self.frame.update_var(dest_frame, dest_var_name, s1_value, s1_data_type)

    def CREATEFRAME(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        self.frame.create_frame()

    def PUSHFRAME(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        self.frame.push_frame()

    def POPFRAME(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)

        self.frame.pop_frame()

    def DEFVAR(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        frame, var_name = self.VAR(args[0])
        self.frame.add_var(frame, var_name)

    def CALL(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']

        if not self.label_exists(label):
            raise MyException(ErrCodes.SEMANTIC)

        self.call_stack.push(self.pc + 1)
        self.input.set_ins_iterator(self.label_dict[label]-1)
        self.pc = self.label_dict[label] - 1

    def RETURN(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)

        if self.call_stack.isEmpty():
            raise MyException(ErrCodes.MISSING_VALUE)

        jump_to = self.call_stack.pop()
        self.input.set_ins_iterator(jump_to - 1)
        self.pc = jump_to - 1



    def PUSHS(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        s1_data_type, s1_value = self.SYMB(args[0])

        item = dict()
        item['type'] = s1_data_type
        item['value'] = s1_value

        self.data_stack.push(item)


    def POPS(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if self.data_stack.peek() is None:
            raise MyException(ErrCodes.MISSING_VALUE)

        frame, var_name = self.VAR(args[0])

        item = self.data_stack.pop()

        self.frame.update_var(frame, var_name, item['value'], item['type'])


    def ADD(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if not self.comp_arit_types(s1_data_type, s2_data_type):
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value + s2_value, s1_data_type)

    def SUB(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if not self.comp_arit_types(s1_data_type, s2_data_type):
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value - s2_value, s1_data_type)

    def MUL(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if not self.comp_arit_types(s1_data_type, s2_data_type):
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value * s2_value, s1_data_type)

    def IDIV(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if not self.comp_arit_types(s1_data_type, s2_data_type):
            raise MyException(ErrCodes.SEMANTIC)
        if s2_value == 0:
            raise MyException(ErrCodes.ZERO_DIVISION)

        if s1_data_type == 'int':
            self.frame.update_var(dest_frame, dest_var_name, int(s1_value / s2_value), s1_data_type)
        else:
            self.frame.update_var(dest_frame, dest_var_name, s1_value / s2_value, s1_data_type)

    def LT(self,args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != s2_data_type:
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value < s2_value, 'bool')


    def GT(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != s2_data_type:
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value > s2_value, 'bool')

    def EQ(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != s2_data_type:
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value == s2_value, 'bool')

    def AND(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != 'bool' or s2_data_type != 'bool':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value and s2_value, 'bool')



    def OR(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != 'bool' or s2_data_type != 'bool':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value or s2_value, 'bool')

    def NOT(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])
        s1_data_type, s1_value = self.SYMB(args[1])
        if s1_data_type != 'bool':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, not s1_value, 'bool')

    def INT2CHAR(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])
        s1_data_type, s1_value = self.SYMB(args[1])

        if s1_data_type != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        try:
            res = chr(s1_value)
        except ValueError:
            raise MyException(ErrCodes.STRING)

        self.frame.update_var(dest_frame, dest_var_name, res, 'string')

    def STRI2INT(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != 'string' or s2_data_type != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        try:
            res = ord(s1_value[s2_value])
        except IndexError:
            raise MyException(ErrCodes.STRING)

        self.frame.update_var(dest_frame, dest_var_name, res, 'int')

    def READ(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])

        if args[1]['type'] != 'type':
            raise MyException(ErrCodes.OPERAND)

        try:
            user_input = input()
        except EOFError:
            user_input = None

        if args[1]['value'] == 'int':
            try:
                user_input = int(user_input)
            except ValueError:
                user_input = 0

        elif args[1]['value'] == 'float':
            try:
                user_input = float(user_input)
            except ValueError:
                user_input = 0.0

        elif args[1]['value'] == 'bool':
            if user_input.isalpha():
                if user_input.lower() == 'true':
                    user_input = True
                else:
                    user_input = False
            else:
                user_input = False
        else: #string
            if user_input is None:
                user_input = ""

        self.frame.update_var(dest_frame, dest_var_name, user_input, args[1]['value'])

    def WRITE(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        s_type, s_value = self.SYMB(args[0])

        if s_type == 'float':
            print(float.hex(s_value))
        elif s_type == 'bool':
            if s_value == True:
                print('true')
            else:
                print('false')
        else:
            print(str(s_value))

    def CONCAT(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != 'string' or s2_data_type != 'string':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, s1_value + s2_value, 'string')

    def STRLEN(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])
        s1_data_type, s1_value = self.SYMB(args[1])

        if s1_data_type != 'string':
            raise MyException(ErrCodes.SEMANTIC)

        self.frame.update_var(dest_frame, dest_var_name, len(s1_value), 'int')

    def GETCHAR(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        if s1_data_type != 'string' or s2_data_type != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        try:
            res = s1_value[s2_value]
        except IndexError:
            raise MyException(ErrCodes.STRING)

        self.frame.update_var(dest_frame, dest_var_name, res, 'string')

    def SETCHAR(self, args):
        dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type = self.VAR_SYMB_SYMB(args)

        variable = self.frame.get_var(dest_frame, dest_var_name)

        if variable.data_type != 'string':
            raise MyException(ErrCodes.SEMANTIC)

        if s1_data_type != 'int':
            raise MyException(ErrCodes.SEMANTIC)

        if s2_data_type != 'string':
            raise MyException(ErrCodes.SEMANTIC)

        if s2_value == '':
            raise MyException(ErrCodes.STRING)

        str_list = list(variable.value)

        try:
            str_list[s1_value] = s2_value[0]
        except IndexError:
            raise MyException(ErrCodes.STRING)

        str = "".join(str_list)
        self.frame.update_var(dest_frame, dest_var_name, str, 'string')


    def TYPE(self, args):
        if len(args) != 2:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])

        if args[1]['type'] == 'var':
            s_frame, s_var_name = self.VAR(args[1])
            s_var = self.frame.get_var(s_frame, s_var_name)
            s_type = s_var.data_type
        else:
            s_type, s_value = self.CONST(args[1])

        if s_type is None:
            self.frame.update_var(dest_frame, dest_var_name, '', 'string')
        else:
            self.frame.update_var(dest_frame, dest_var_name, s_type, 'string')

    def JUMP(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']

        if not self.label_exists(label):
            raise MyException(ErrCodes.SEMANTIC)

        self.input.set_ins_iterator(self.label_dict[label]-1)
        self.pc = self.label_dict[label] - 1

    def JUMPIFEQ(self, args):
        if len(args) != 3:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']

        s1_type, s1_value = self.SYMB(args[1])
        s2_type, s2_value = self.SYMB(args[2])

        if s1_type != s2_type:
            raise MyException(ErrCodes.OPERAND)

        if s1_value == s2_value:
            if not self.label_exists(label):
                raise MyException(ErrCodes.SEMANTIC)
            self.input.set_ins_iterator(self.label_dict[label]-1)
            self.pc = self.label_dict[label] - 1

    def JUMPIFNEQ(self, args):
        if len(args) != 3:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] != 'label':
            raise MyException(ErrCodes.OPERAND)

        label = args[0]['value']

        s1_type, s1_value = self.SYMB(args[1])
        s2_type, s2_value = self.SYMB(args[2])

        if s1_type != s2_type:
            raise MyException(ErrCodes.OPERAND)

        if s1_value != s2_value:
            if not self.label_exists(label):
                raise MyException(ErrCodes.SEMANTIC)

            self.input.set_ins_iterator(self.label_dict[label]-1)
            self.pc = self.label_dict[label]-1

    def DPRINT(self, args):
        if len(args) != 1:
            raise MyException(ErrCodes.XML_FORMAT)

        if args[0]['type'] == 'var':
            s_frame, s_var_name = self.VAR(args[0])
            s_var = self.frame.get_var(s_frame, s_var_name)
            s_value = s_var.value
        else:
            s_type, s_value = self.CONST(args[0])

        sys.stderr.write(str(s_value) + '\n')

    def BREAK(self, args):
        if len(args) != 0:
            raise MyException(ErrCodes.XML_FORMAT)
        sys.stderr.write('----------------<BREAK>---------------------\n')
        sys.stderr.write('Pozice v kodu: ' + str(self.pc) + '\n')
        sys.stderr.write('Pocet vykonanych instrukci: ' + str(self.ins_count+1) + '\n')
        self.frame.print_vars()
        sys.stderr.write('----------------</BREAK>---------------------\n')


    #########################################################################
    #################### Konec interpretovanych instrukci ###################

    # Rozhazi typy a hodnoty argumentu do promennych
    # Pouze pro instrukce s VAR SYMB SYMB operandy
    def VAR_SYMB_SYMB(self,args):
        if len(args) != 3:
            raise MyException(ErrCodes.XML_FORMAT)

        dest_frame, dest_var_name = self.VAR(args[0])

        s1_data_type, s1_value = self.SYMB(args[1])
        s2_data_type, s2_value = self.SYMB(args[2])

        return dest_frame, dest_var_name, s1_value, s2_value, s1_data_type, s2_data_type

    # Ziskani typu a hodnoty z SYMB argumentu instrukce
    def SYMB(self, arg):
        if arg['type'] == 'var':
            s_frame, s_var_name = self.VAR(arg)
            s_var = self.frame.get_var(s_frame, s_var_name)
            s_value = s_var.value
            if s_value is None:
                raise MyException(ErrCodes.MISSING_VALUE)
            s_type = s_var.data_type
        else:
            s_type, s_value = self.CONST(arg)

        return s_type, s_value

    # Ziskani framu a nazvu promenne z VAR argumentu instrukce
    def VAR(self, arg):
        if arg['type'] != 'var':
            raise MyException(ErrCodes.OPERAND)

        frame, var_name = syntax.eval_var_string(arg['value'])
        return frame, var_name

    # Ziskani typu a hodnoty z SYMB argumentu instrukce, ktery neni VAR, ale konstanta
    def CONST(self, arg):
        return arg['type'], arg['value']

    # Porovnani aritmetickych typu
    def comp_arit_types(self, type1, type2):
        if type1 == type2 and type1 in ['int', 'float']:
            return True
        else:
            return False