from ErrCodes import *

# Trida pro sbirani a validaci spravnosti dat z XML souboru
class FileParser:

    ins_element = None          # type: Element
    ins_element_list = None     # iterovatelny seznam elementu instrukce

    def __init__(self, element_tree):
        self.root_element = element_tree.getroot()  # type: Element  # Korenovy element XML souboru
        self.arg_iter = 0                           # Pocitadlo argumentu
        self.set_ins_iterator()
        self.end = False                            # konec prochazeni XML souboru

    # Prepnuti iteratoru na dalsi element instrukce
    def next_instruction(self):
        try:
            self.ins_element = next(self.ins_element_list)
        except StopIteration:
            self.end = True

    # Nastaveni iteratoru instrukce na instrukci podle poradi
    def set_ins_iterator(self, position=1):
        self.ins_element_list = self.root_element.iter("instruction")
        try:
            self.ins_element = next(self.ins_element_list)     # instrukce order 1
        except StopIteration:
            self.end = True
        else:
            self.end = False

        while int(self.ins_element.get("order")) != position:
            self.next_instruction()


    # Kontrola hlavicky programu (element <program>)
    def validate_header(self):
        if self.root_element.tag != "program":
            raise MyException(ErrCodes.XML_FORMAT)

        for key in self.root_element.keys():
            if key != "language":
                raise MyException(ErrCodes.XML_FORMAT)

        if self.root_element.get("language") != "IPPcode18":
            raise MyException(ErrCodes.XML_FORMAT)


    # bere argumenty instrukci, vraci list slovniku s argumenty
    def get_args(self):
        args = list(self.ins_element)
        arg_list = []
        i = 1
        for arg in args:

            if int(arg.tag[3]) != i:
                raise MyException(ErrCodes.XML_FORMAT)
            else:
                a = dict()
                a['type'] = arg.get('type')
                a['value'] = arg.text
                arg_list.append(a)
                i += 1

        return arg_list

    # Nacteni jedne instrukce podle aktualni pozice iteratoru, vraci artibuty order a opcode
    def get_ins(self):
        if self.ins_element.tag != "instruction":
            raise MyException(ErrCodes.XML_FORMAT)

        if {"order", "opcode"} != set(self.ins_element.keys()):
            raise MyException(ErrCodes.XML_FORMAT)

        return int(self.ins_element.get("order")), self.ins_element.get("opcode")
