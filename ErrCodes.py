# Vlastni vyjimka, specificka pro chyby interpretu
class MyException(Exception):
    def __init__(self, arg1):
        self.arg1 = arg1


class ErrCodes:
    OK = 0                          # OK
    PARAM = 10                      # Parametr
    INPUT_FILE = 11                 # Vstupni soubor
    OUTPUT = 12                     # Vystup
    XML_FORMAT = 31                 # Chyba XML formatu
    LEX_SYNTAX = 32                 # Chyba lexikalni nebo syntakticke analyzy
    SEMANTIC = 52                   # Semanticka chyba
    OPERAND = 53                    # Spatne typy operandu
    NONEXISTENT_VARIABLE = 54       # Pristup k neexistujici promenne (ramec existuje)
    NONEXISTENT_FRAME = 55          # Ramec neexistuje
    MISSING_VALUE = 56              # Chybejici hodnota (v promenne, na datovem zasobniku, nebo v zasobniku volani)
    ZERO_DIVISION = 57              # Deleni nulou
    STRING = 58                     # Chybna prace s retezcem