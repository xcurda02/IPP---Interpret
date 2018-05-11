import sys
import argparse
from Interpreter import Interpreter
from ErrCodes import *
from xml.etree import ElementTree as ET
import getopt


def help_txt():

    str = "Program nacte XML reprezentaci programu ze zadaneho souboru a tento program s vyuzitim " \
           "standardniho vstupu a vystupu interpretuje. Vstupni XML reprezentace je napr. generovana" \
           " skriptem parse.php ze zdrojoveho kodu v IPPcode18\n"

    return str


# Parsovani argumentu prikazove radky
def handleArgs():
    parser = argparse.ArgumentParser(add_help=False, description=help_txt())

    requiredNamed = parser.add_argument_group('Povinne argumenty')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='vypsani napovedy')

    requiredNamed.add_argument('--source', action='store', dest='source_file', required='--help' not in sys.argv and '-h' not in sys.argv,
                        help = 'zdrojovy soubor')


    parser.add_argument('--stats', action='store', dest='stats_file', default=None,
                        help = 'vypisovani statistik do souboru')

    parser.add_argument('--insts', action='store_true', default=False, dest='insts',
                        help = 'pocitani instrukci')


    parser.add_argument('--vars', action='store_true', default=False, dest='vars',
                        help = 'pocitani maximalniho poctu inicializovanych promennych')

    for grp in parser._action_groups:
        if grp.title == 'optional arguments':
            grp.title = 'Volitelne argumenty'

    try:
        args = parser.parse_args()
    except SystemExit:
        return None

    if args.stats_file is None and (args.insts is True or args.vars is True):
        parser.error('argument --stats missing')
    return args


def main():
    # Zpracovani argumentu
    args = handleArgs()
    if args is None:
        if '--help' not in sys.argv and '-h' not in sys.argv:
            sys.exit(ErrCodes.PARAM)
        else:
            sys.exit(ErrCodes.OK)

    try:
        file = open(args.source_file,"r")
    except:                         # Chyba vstupniho souboru
        sys.exit(ErrCodes.INPUT_FILE)

    try:
         tree = ET.parse(file)
    except ET.ParseError:           # Chybny format xml
        sys.exit(ErrCodes.XML_FORMAT)

    interpreter = Interpreter(tree) # Vytvoreni objektu interpretu

    # Interpretace
    try:
        interpreter.run_code()
    except MyException as e:        #chyba interpretace
        #print("Exiting with code: %d" % e.arg1)
        sys.exit(e.arg1)

    # rozsireni STATI
    if args.stats_file != None:
        try:
            out_file = open(args.stats_file, 'w')
        except:
            sys.exit(ErrCodes.OUTPUT)

        try:
            optlist, a = getopt.getopt(sys.argv[1:],'',['source=','stats=','insts','vars'])
        except getopt.GetoptError:
            pass

        for opt in optlist:
            if opt[0] == '--insts':
                out_file.write(str(interpreter.ins_count) + '\n')
            if opt[0] == '--vars':
                out_file.write(str(interpreter.get_vars()) + '\n')


    exit(ErrCodes.OK)




if __name__ == "__main__":
    main()
