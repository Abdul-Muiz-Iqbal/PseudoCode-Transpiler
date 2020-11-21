from re import compile
from sys import argv
from os import system as sh

TEMP_NAME = "temp"

GLOBALS = {}
LOCALS = {}
INDENTATION = 0

def getType(val):
    if val.startswith("\""):
        return "str"
    elif val.isdecimal():
        return "int"
    elif "." in val:
        return "float"
    elif val == "True" or val == "False":
        return "bool"

def psuPrint(args):
    msg = args[0]
    var = args[2]
    if var:
        return (" " * INDENTATION) + f"print({msg} + str({var}))\n"
    else:
        return (" " * INDENTATION) + f"print({msg})\n"

def psuInput(args):
    var1 = args[0]
    var2 = args[2]
    rem = "input(\"\")"

    if var1 and var2:
        if GLOBALS[var1][1] == "int" and GLOBALS[var2][1] == "int":
            rem = "int(input(\"\"))"
        elif GLOBALS[var1][1] == "float" and GLOBALS[var2][1] == "float":
            rem = "float(input(\"\"))"
        elif GLOBALS[var1][1] == "bool" and GLOBALS[var2][1] == "bool":
            rem = "bool(input(\"\"))"
        elif GLOBALS[var1][1] == "str" and GLOBALS[var2][1] == "str":
            rem = "str(input(\"\"))"

        return (" " * INDENTATION) + f"{var1}, {var2} = {rem, rem}\n"
    else:
        if GLOBALS[var1][1] == "int":
            rem = "int(input(\"\"))"
        elif GLOBALS[var1][1] == "float":
            rem = "float(input(\"\"))"
        elif GLOBALS[var1][1] == "bool":
            rem = "bool(input(\"\"))"
        elif GLOBALS[var1][1] == "str":
            rem = "str(input(\"\"))"

        return (" " * INDENTATION) + f"{var1} = {rem}\n"

def psuSet(args):
    name = args[0]
    value = args[1]

    return (" " * INDENTATION) + f"{name} = {value}\n"

def psuIf(args):
    global INDENTATION
    cond = args[0].replace("AND", "and").replace("OR", "or").replace("NOT", "not")
    rem = (" " * INDENTATION) + f"if {cond}:\n"
    INDENTATION += 4
    return rem

def psuElseIf(args):
    global INDENTATION
    cond = args[0].replace("AND", "and").replace("OR", "or").replace("NOT", "not")
    rem = (" " * (INDENTATION - 4)) + f"elif {cond}:\n"
    return rem

def psuElse(_):
    global INDENTATION
    rem = (" " * (INDENTATION - 4)) + f"else:\n"
    return rem

def psuEndIf(_):
    global INDENTATION
    INDENTATION -= 4
    return ""

def psuFor(args):
    global INDENTATION
    temp = args[0].split("=")
    var = temp[0].strip()
    frm = int(temp[1].strip())
    to = int(args[1]) + 1
    rem = (" " * INDENTATION) + f"for {var} in range({frm}, {to}):\n"
    INDENTATION += 4
    return rem

def psuNext(args):
    global INDENTATION
    INDENTATION -= 4
    return ""

KEYWORDS = {
    "SET"   : r"^SET\s+([A-Za-z_][A-Za-z_0-9]*)\s+TO\s+(.*)",
    "PRINT" : r"^PRINT\s+(\".*\")(,\s*([A-Za-z_][A-Za-z_0-9]*))*",
    "OUTPUT": r"^OUTPUT\s+(\".*\")(,\s*([A-Za-z_][A-Za-z_0-9]*))*",
    "INPUT" : r"^INPUT\s+([A-Za-z_][A-Za-z_0-9]*)(,(\s*[A-Za-z_][A-Za-z_0-9]*))*",
    "READ"  : r"^READ\s+([A-Za-z_][A-Za-z_0-9]*)(,(\s*[A-Za-z_][A-Za-z_0-9]*))*",
    "IF"    : r"^IF\s+(.*)\s+THEN",
    "ELSEIF": r"^ELSE\s*IF\s+(.*)\s+THEN",
    "ELSE"  : r"^ELSE",
    "ENDIF" : r"^ENDIF",
    "FOR"   : r"^FOR\s+(.*)\s+TO\s+(.*)",
    "NEXT"  : r"^NEXT\s+(.*)"
}

OPS = {
    ":" : r":",
    "=" : r"^([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.*)",
    "+" : r"\+",
    "-" : r"-",
    "*" : r"\*",
    "/" : r"/",
    ">=": r">=",
    "<=": r"<=",
    "==": r"==",
    "AND": r"AND",
    "OR": r"OR",
    "NOT": r"OR"
}

FUNC = {
    "SET"   : psuSet,
    "PRINT" : psuPrint,
    "OUTPUT": psuPrint,
    "INPUT" : psuInput,
    "READ"  : psuInput,
    "IF"    : psuIf,
    "ELSEIF": psuElseIf,
    "ELSE"  : psuElse,
    "ENDIF" : psuEndIf,
    "FOR"   : psuFor,
    "NEXT"  : psuNext
}

def psuAssign(assignments):
    name = assignments[0].strip()
    value = assignments[1]
    var = compile(r"([A-Za-z_][A-Za-z_0-9]*)")
    GLOBALS[name] = [value, getType(value)]

    return f"{name} = {value}"

OPER = {
    "=" : psuAssign
}

class Transpiler:

    def transpileFile(self, filePath, compile=False):
        transpiled = []

        with open(filePath, "r") as codeFile:
            for line in codeFile.readlines():
                if code := self.transpileLine(line):
                    transpiled.append(code)
        open(f"{TEMP_NAME}.py", "w").close()
        with open(f"{TEMP_NAME}.py", "a") as f:
            f.writelines(transpiled)

        if compile:
            sh(f'cmd /c pyinstaller --onefile {TEMP_NAME}.py')
            sh(f'rm {TEMP_NAME}.py')
            sh(f'cp dist/{TEMP_NAME}.exe .')
            sh(f'rm -r dist')
            sh(f'rm -r build')
            sh(f'rm -r __pycache__')
            sh(f'rm temp.spec')

    def transpileLine(self, line):
        # Is An Inline Keyword
        for keyword in KEYWORDS.keys():
            matches = compile(KEYWORDS[keyword]).match(line.strip())
            if matches:
                return FUNC[keyword](matches.groups()) 
        # OtherWise, It's a Ops Operation
        l = []
        for ln in line.split(":"):
            match = compile(OPS["="]).match(ln.strip())
            if match:
                l.append((" " * INDENTATION) + OPER["="](match.groups()))
        return "; ".join(l) + "\n"

def main():
    """
    $ psu test.psu -p
    $ psu test.psu -c
    $ psu
    """
    t = Transpiler()
    # REPL Mode
    if len(argv) == 1:
        print("PseudoCode REPL Coming Soon...")
    # Transpile Mode
    elif len(argv) == 2:
        file = argv[1]
        t.transpileFile(file)
    elif len(argv) > 2:
        file = argv[1]
        flag = argv[2]
        if flag == "-c":
            t.transpileFile(file, True)
        elif flag == "-p":
            t.transpileFile(file)
        else:
            print("Unknown Flag Found!")

if __name__ == "__main__":
    # TODO:
    # Currently AND OR NOT Are Lower Cased Including Strings Eg: "He AND me"
    # Indentation Bugs May Go Unnoticed During Dev
    # Code Hygiene. Not Be Able To Do: s = sum([1, 2, 3]). Fix: Use GLOBALS = {}
    main()
