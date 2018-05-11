from Frame import GF, TF, LF
from ErrCodes import *
import re


class Syntax:

    # Kontrola spravnosti retezce reprezentujiciho promennou (napr. GF@abc)
    # Vraci jmeno jmeno ramce a jemno promenne
    @staticmethod
    def eval_var_string(string):
        if not ('@' in string):
            raise MyException(ErrCodes.LEX_SYNTAX)
        else:
            frame = string[:2]
            var_name = string[3:]
            if frame not in ["LF", "GF", "TF"]:
                raise MyException(ErrCodes.LEX_SYNTAX)

            frame = Syntax.frame_const(frame)

            if not Syntax.is_valid_id(var_name):
                raise MyException(ErrCodes.LEX_SYNTAX)

            return frame, var_name

    # Konverze stringoveho jmena framu na konstantu definovanou ve Frame.py
    @staticmethod
    def frame_const(frame_str):
            if frame_str == "LF":
                return LF

            elif frame_str == "TF":
                return TF

            else:
                return GF

    # Kontrola spravnosti identifikatoru
    @staticmethod
    def is_valid_id(identifier):
        reg = re.compile('[a-zA-Z_\-$&%*][\w_\-$&%*]*')
        if reg.match(identifier) is not None:
            return True
        else:
            return False

    # Kontrola syntaxe argumentu ziskanych z XML souboru
    @staticmethod
    def args_syntax(args):
        for arg in args:
            if arg['type'] == 'var':
                continue
                # kontrola promennych probiha az pri interpretaci

            if arg['type'] == 'int':
                arg['value'] = Syntax.eval_int(arg['value'])

            elif arg['type'] == 'float':
                arg['value'] = Syntax.eval_float(arg['value'])

            elif arg['type'] == 'string':
                arg['value'] = Syntax.eval_string(arg['value'])

            elif arg['type'] == 'bool':
                arg['value'] = Syntax.eval_bool(arg['value'])

            elif arg['type'] == 'type':
                if arg['value'] not in ['int', 'float', 'bool', 'string']:
                    raise MyException(ErrCodes.LEX_SYNTAX)

            elif arg['type'] == 'label':
                if not Syntax.is_valid_id(arg['value']):
                    raise MyException(ErrCodes.LEX_SYNTAX)

            else:
                raise MyException(ErrCodes.LEX_SYNTAX)

    @staticmethod
    def eval_int(string):
        try:
            return int(string)
        except ValueError:
            raise MyException(ErrCodes.LEX_SYNTAX)

    @staticmethod
    def eval_float(string):
        try:
            return float.fromhex(string)
        except ValueError:
            raise MyException(ErrCodes.LEX_SYNTAX)

    # Kontrola stringu, konverze escape sekvenci na znaky
    @staticmethod
    def eval_string(string):
        if string is None:
            return ''
        index = string.find("\\")
        while index != -1:
            digits = string[index + 1:index + 4]
            if digits.isdigit() and len(digits) == 3:
                partOne = string[0:index] + chr(int(digits))
                partTwo = string[index + 4:]
                string = partOne + partTwo
            else:
                raise MyException(ErrCodes.LEX_SYNTAX)
            old_index = index
            index = string[index + 1:].find("\\")
            if index != -1:
                index += old_index + 1
        return string


    @staticmethod
    def eval_bool(string):
        if string == 'true':
            return True
        elif string == 'false':
            return False
        else:
            raise MyException(ErrCodes.LEX_SYNTAX)