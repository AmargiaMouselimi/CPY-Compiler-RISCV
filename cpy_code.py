# Stefas Anastasios-Orestis 4916

# Mouselimi Amalia-Georgia 5074

import sys

symbols = {'+', '-', '*', '%', ':', ',', '=', '(', ')', '{', '}', '!'}
cond = ['==', '<', '>', '!=', '<=', '>=']
keywords = {'main', 'def', '#def' '#int', 'global', 'if', 'elif', 'else', 'while', 'not', 'and', 'or', 'return', 'int',
            'input', 'print'}
# a

ID = []
temp_ID = []
funcID = []
flag_temp_variables = 0
flag_func_names = 0
token = ''
line = 1
helpGlobal = 0

# b
quadList = []
quadCounter = 1
tempCounter = 0

# c
varID = []
scope = []
scopes = []
argList = []
tempList = []
helpList = []
writer = ''
mainList = []


# Lexical Analyzer

def lex():
    situation = 0
    global line, helpGlobal, flag_temp_variables

    lexUnit = ''

    while situation != 10:
        i = f.read(1)
        if situation == 0:
            if i.isspace():
                if i == '\n':
                    line += 1
                situation = 0
            elif i.isalpha():
                lexUnit += i
                situation = 1
            elif i.isdigit():
                lexUnit += i
                situation = 2
            elif i == '<' or i == '>' or i == '=':
                lexUnit += i
                situation = 3
            elif i == '/':
                lexUnit += i
                situation = 4
            elif i == '!':
                lexUnit += i
                situation = 5
            elif i == '#':
                lexUnit += i
                situation = 6
            elif i in symbols:
                lexUnit += i
                return i
            elif i == ':':
                situation = 10
            else:
                if i != '':
                    print("Error! Unknown symbol in line: " + str(line))
                else:
                    raise EOFError("eof")
                exit()
        elif situation == 1:
            if i.isalpha() or i.isdigit() or i == '_':
                lexUnit += i
            elif i.isspace():
                if i == '\n':
                    line += 1
                if lexUnit not in keywords and lexUnit not in ID and lexUnit not in funcID and lexUnit not in symbols \
                        and flag_temp_variables == 0:
                    if flag_func_names == 1:
                        funcID.append(lexUnit)
                    else:
                        ID.append(lexUnit)
                if lexUnit not in keywords and lexUnit not in temp_ID and lexUnit not in funcID \
                        and lexUnit not in symbols and flag_temp_variables == 1:
                    temp_ID.append(lexUnit)
                if lexUnit == 'global':
                    helpGlobal = 1
                situation = 10
            else:
                if lexUnit not in keywords and lexUnit not in ID and lexUnit not in funcID and flag_temp_variables == 0:
                    if flag_func_names == 1:
                        funcID.append(lexUnit)
                    else:
                        ID.append(lexUnit)
                if lexUnit not in keywords and lexUnit not in temp_ID and lexUnit not in funcID and flag_temp_variables == 1:
                    temp_ID.append(lexUnit)
                f.seek(f.tell() - 1)
                situation = 10  # break
        elif situation == 2:
            if i.isdigit():
                lexUnit += i
            elif i.isalpha():
                print("Error! Alphabetic right after digit. Line: " + str(line))
                exit()
            elif i.isspace():
                if i == '\n':
                    line += 1
                num = int(lexUnit)
                if num > 32767 or num < -32767:
                    print("Error! Number out of range in line " + str(line))
                    exit()
                situation = 10
            elif i in symbols:
                f.seek(f.tell() - 1)
                situation = 10
        elif situation == 3:
            if i == '=':
                lexUnit += i
                situation = 10
            elif i.isspace():
                if i == '\n':
                    line += 1
                situation = 10
            else:
                f.seek(f.tell() - 1)
                situation = 10
        elif situation == 4:
            if i == '/':
                lexUnit += i
                situation = 10
            else:
                print("Error! Unknown symbol in line " + str(line) + " Expected (//)")
                exit()
        elif situation == 5:
            if i == '=':
                lexUnit += i
                return "!="
            else:
                print("Error! Unknown symbol in line " + str(line) + " Expected (!=)")
                exit()
        elif situation == 6:
            if i == '{' or i == '}':
                lexUnit += i
                situation = 10
            elif i == 'i':
                lexUnit += i
                situation = 7
            elif i == '#':
                situation = 8
            elif i == 'd':
                lexUnit += i
                situation = 9
            else:
                print("Error! Unknown symbol in line " + str(line))
                exit()
        elif situation == 7:
            if i.isalpha():
                lexUnit += i
            elif i.isspace() and lexUnit == '#int':
                situation = 10
            else:
                print("Error! Unknown symbol(7) in line " + str(line))
                exit()
        elif situation == 8:
            while i != '#':
                i = f.read(1)
            i = f.read(1)
            if i == '#':
                lexUnit = ''
                situation = 0
            else:
                situation = 0
        elif situation == 9:
            if i.isalpha():
                lexUnit += i
            elif i.isspace() and lexUnit == '#def':
                lexUnit = ''
                situation = 11
            else:
                print("Error! Unknown symbol(9) in line " + str(line))
                exit()
        elif situation == 11:
            if i.isalpha():
                lexUnit += i
            elif i.isspace() and lexUnit == 'main':
                situation = 10
            else:
                print("Error! Expected #def main in line " + str(line))
                exit()
    return lexUnit


# Syntax Analyzer

def startRule():
    def_main_part()
    call_main_part()
    print("Syntax Analysis Successful! \n")


def def_main_part():
    global token
    if token == '#int':
        declarations()
    while token == "def":
        def_main_function()


def def_main_function():
    global token, flag_temp_variables, flag_func_names
    if token == "def":
        flag_func_names = 1
        token = lex()
        flag_func_names = 0
        if token in funcID:
            func_name = token
            newScope(func_name)
            entity = Entity.function(func_name, 'func')
            newEntity(entity)
            token = lex()
            if token == '(':
                flag_temp_variables = 1
                token = lex()
                temp_id_list(True)
                flag_temp_variables = 0
                if token == ')':
                    token = lex()
                    if token == ':':
                        token = lex()
                        if token == '#{':
                            token = lex()
                            declarations()  # if declaration succeeds read next token for check globals
                            addArgs(entity)
                            while token == "def":
                                def_nested_function()
                            genQuad('begin_block', func_name, '_', '_')
                            check_globals(False)
                            flag_temp_variables = 1
                            if token != '#}':
                                statements()
                                if token == '#}':
                                    token = lex()
                                    temp_ID.clear()
                                    flag_temp_variables = 0
                                    updateFields(entity)
                                    outputSymbolFile(name)
                                    helpList.extend(scopes)
                                    remScope()
                                else:
                                    print("Error! Missing '#}' in line: " + str(line))
                                    exit()
                            genQuad('end_block', func_name, '_', '_')
                        else:
                            print("Error! Missing '#{' in line: " + str(line))
                            exit()
                    else:
                        print("Error! Missing ':' in line (main_funtion): " + str(line))
                        exit()
                else:
                    print("Error! Missing ')' in line: " + str(line))
                    exit()
            else:
                print("Error! Missing '(' in line: (def_main_function) " + str(line))
                exit()
        else:
            print("Error! Missing function name in line: " + str(line))
            exit()
    else:
        print("Error! Keyword 'def' expected in line: " + str(line))
        exit()


def def_nested_function():
    global token, flag_temp_variables, flag_func_names
    if token == "def":
        flag_func_names = 1
        token = lex()
        nested_func_name = token
        flag_func_names = 0
        if token in funcID:
            func_name = token
            newScope(func_name)
            entity = Entity.function(func_name, 'func')
            newEntity(entity)
            token = lex()
            if token == '(':
                flag_temp_variables = 1
                token = lex()
                temp_id_list(True)
                flag_temp_variables = 0
                if token == ')':
                    token = lex()
                    if token == ':':
                        token = lex()
                        if token == '#{':
                            token = lex()
                            declarations()
                            addArgs(entity)
                            while token == "def":
                                def_nested_function()
                            genQuad('begin_block', nested_func_name, '_', '_')
                            check_globals(False)
                            temp_ID.clear()
                            flag_temp_variables = 1
                            # statements()
                            if token != '#}':
                                statements()  # code_block
                            if token == '#}':
                                flag_temp_variables = 0
                                token = lex()
                                updateFields(entity)
                                outputSymbolFile(name)
                                helpList.extend(scopes)
                                remScope()
                            else:
                                print("Error! Missing '#}' in line: " + str(line))
                                exit()
                            genQuad('end_block', nested_func_name, '_', '_')
                        else:
                            print("Error! Missing '#{' in line: " + str(line))
                    else:
                        print("Error! Missing ':' in line: (def_funtion) " + str(line))
                        exit()
                else:
                    print("Error! Missing ')' in line: " + str(line))
                    exit()
            else:
                print("Error! Missing '(' in line: (def_function)" + str(line))
                exit()
        else:
            print("Error! Missing function name in line: " + str(line))
            exit()
    else:
        print("Error! Keyword 'def' expected in line: (def function) " + str(line))
        exit()


def declarations():
    global token
    while token == "#int":
        token = lex()
        declaration_line()


def declaration_line():
    id_list(False)


def check_globals(isArg):
    global token
    while helpGlobal == 1:
        token = lex()
        global_line(isArg)


def global_line(isArg):
    global helpGlobal
    id_list(isArg)
    helpGlobal = 0


def statement():
    global token
    if token in ID or token in temp_ID or token in funcID or token == "print" or token == "return":
        simple_statement()
    elif token == "if" or token == "elif" or token == "else" or token == "while":
        structured_statement()
    elif token == "\n":
        token = lex()
    else:
        print("Statement Syntax error in line:  " + str(line))
        exit()


def statements():
    global token
    statement()
    while 1:
        if token != '#}':
            statement()
        else:
            break


def simple_statement():
    global token
    if token in ID or token in temp_ID:
        assignment_stat()
    if token == "print":
        print_stat()
    if token == "return":
        return_stat()
    if token in funcID:
        token = lex()
        e = expression()
        genQuad('out', e, '_', '_')


def structured_statement():
    global token
    if token == "if" or token == "elif" or token == "else":
        if_stat()
    if token == "while":
        while_stat()


def assignment_stat():
    global token
    prev = token
    token = lex()
    if token == '=':
        token = lex()
        if token == 'int':
            token = lex()
            if token == '(':
                token = lex()
                if token == 'input':
                    token = lex()
                    if token == '(':
                        token = lex()
                        if token == ')':
                            token = lex()
                            if token == ')':
                                token = lex()
                                genQuad("inp", prev, "_", "_")
                            else:
                                print("Error! Missing ')' in line: " + str(line))
                                exit()
                        else:
                            print("Error! Missing ')' in line: " + str(line))
                            exit()
                    else:
                        print("Error! Missing '(' in line: " + str(line))
                        exit()
                else:
                    print("Error! Keyword 'input' expected in line: " + str(line))
                    exit()
            else:
                print("Error! Missing '(' in line: " + str(line))
                exit()
        else:
            e = expression()
            genQuad('=', e, '_', prev)
    else:
        print("Error! Missing '=' in line: " + str(line))


def print_stat():
    global token
    prevT = token
    token = lex()
    if token == '(':
        token = lex()
        e = expression()
        genQuad('out', e, '_', '_')
        if token == ")":
            token = lex()
        else:
            print("Error! Missing ')' in line: " + str(line))
            exit()
    else:
        print("Error! Missing '(' in line:  " + str(line))
        exit()


def return_stat():
    global token
    prevT = token
    token = lex()
    e = expression()
    genQuad('ret', e, '_', '_')


def if_stat():
    global token
    if token == "else":
        token = lex()
        if token == ':':
            token = lex()
            statements()
            return
        else:
            print("Error!  Missing ':' in line: " + str(line))
            exit()
    else:
        token = lex()
        cond = condition()
        if token == ':':
            backPatch(cond[0], nextQuad())
            token = lex()
            statements()
        else:
            print("Error!  Missing ':' in line: " + str(line))
            exit()
        if_list = makeList(nextQuad())
        genQuad('jump', '_', '_', "_")
        backPatch(cond[1], nextQuad())
    backPatch(if_list, nextQuad())


def while_stat():
    global token
    token = lex()
    before_while = nextQuad()
    cond = condition()
    if token == ':':
        token = lex()
        backPatch(cond[0], nextQuad())
        if token == '#{':
            token = lex()
            statements()
            if token == "#}":
                token = lex()
            else:
                print("Error! Expected '#}' in line: " + str(line))
                exit()
        else:
            print("Error! Expected '#{' in line: " + str(line))
            exit()
        genQuad('jump', '_', '_', before_while)
        backPatch(cond[1], nextQuad())
    else:
        print("Error! WHILE WTF Missing ':' in line: " + str(line))
        exit()


def id_list(isArg):
    global token
    if token in ID:
        if isArg:
            arg = [token, 'cv']
            argList.append(arg)
            parameter = Entity.param(arg[0], 'prm', arg[1], getOffset())
            newEntity(parameter)
        else:
            varID.append(token)
            entity = Entity.var(token, 'var', getOffset())
            newEntity(entity)
        token = lex()
        while token == ',':
            token = lex()
            if token in ID:
                if isArg:
                    arg = [token, 'cv']
                    argList.append(arg)
                    parameter = Entity.param(arg[0], 'prm', arg[1], getOffset())
                    newEntity(parameter)
                else:
                    varID.append(token)
                    entity = Entity.var(token, 'var', getOffset())
                    newEntity(entity)
                token = lex()
            else:
                print("Syntax error in line:  " + str(line))
                exit()
    else:
        if token.isspace():
            token = lex()
            if token == ')':
                return
            else:
                print("Syntax error in line: " + str(line))
                exit()


def temp_id_list(isArg):
    global token
    if token in temp_ID:
        if isArg:
            arg = [token, 'cv']
            argList.append(arg)
            parameter = Entity.param(arg[0], 'prm', arg[1], getOffset())
            newEntity(parameter)
        else:
            varID.append(token)
            entity = Entity.var(token, 'var', getOffset())
            newEntity(entity)
        token = lex()
        while token == ',':
            token = lex()
            if token in temp_ID:
                if isArg:

                    arg = [token, 'cv']
                    argList.append(arg)
                    parameter = Entity.param(arg[0], 'prm', arg[1], getOffset())
                    newEntity(parameter)
                else:
                    varID.append(token)
                    entity = Entity.var(token, 'var', getOffset())
                    newEntity(entity)
                token = lex()
            else:
                print("Syntax error in line: " + str(line))
                exit()
    else:
        if token.isspace():
            token = lex()
            if token == ')':
                return
            else:
                print("Syntax error in line:  " + str(line))
                exit()


def expression():
    global token
    ops = optional_sign()
    t1 = term()
    if ops == "-":
        temp = newTemp()
        genQuad('-', 0, t1, temp)
        t1 = temp
    while token == '+' or token == '-':
        addop = ADD_OP()
        t2 = term()
        w = newTemp()
        genQuad(addop, t1, t2, w)
        t1 = w
    return t1


def term():
    global token
    f1 = factor()
    while token == '*' or token == '//' or token == '%':
        mulop = MUL_OP()
        f2 = factor()
        w = newTemp()
        genQuad(mulop, f1, f2, w)
        f1 = w
    return f1


def factor():
    global token
    if token.isdigit():
        tok = token
        token = lex()
        return tok
    elif token in ID or token in temp_ID:
        preToken = token
        token = lex()
        variable = idtail(preToken)
        return variable
    elif token in funcID:
        func = token
        token = lex()
        f = idtail(func)
        return f
    elif token == '(':
        token = lex()
        e = expression()
        if token == ')':
            token = lex()
            return e
        else:
            print("Error! Missing ')' in line " + str(line))
            exit()
    elif token == "int":
        assignment_stat()
    else:
        print("Error! Missing ID or number in line: " + str(line))


def idtail(fid):
    global token
    if token == "(":
        token = lex()
        actual_par_list()
        w = newTemp()
        genQuad('par', w, 'RET', '_')
        genQuad('call', fid, '_', '_')
        if token == ')':
            token = lex()
        else:
            print("Error! Missing ')' in line. oops  " + str(line))
            exit()
        return w
    return fid


def actual_par_list():
    global token
    if token == ")":
        # w = newTemp()
        # genQuad('par', w, 'RET', '_')
        expression()
        return
    # e = expression()
    # if e.isdigit():
    #     return
    e = expression()
    genQuad('par', e, 'CV', '_')
    entity = Entity.param(e, 'prm', 'CV', getOffset())
    newEntity(entity)
    while token == ',':
        token = lex()
        e = expression()
        genQuad('par', e, 'CV', '_')
        entity = Entity.param(e, 'prm', 'CV', getOffset())
        newEntity(entity)


def condition():
    global token
    Q1 = bool_term()
    condTrue = Q1[0]
    condFalse = Q1[1]
    while token == 'or':
        backPatch(condFalse, nextQuad())
        token = lex()
        Q2 = bool_term()
        condTrue = merge(condTrue, Q2[0])
        condFalse = Q2[1]
    return condTrue, condFalse


def bool_term():
    global token
    R1 = bool_factor()
    boolTrue = R1[0]
    boolFalse = R1[1]
    while token == 'and':
        backPatch(boolTrue, nextQuad())
        token = lex()
        R2 = bool_factor()
        boolTrue = R2[0]
        boolFalse = merge(boolFalse, R2[1])
    return boolTrue, boolFalse


def bool_factor():
    global token
    if token == 'not':
        token = lex()
        B = condition()
        boolfactorT = B[1]
        boolfactorF = B[0]
        if token == ":":
            return boolfactorF, boolfactorT
        else:
            print("Error! Missing ':' in line: " + str(line))
            exit()
    else:
        E1 = expression()
        rel = REL_OP()
        E2 = expression()
        Rtrue = makeList(nextQuad())
        genQuad(rel, E1, E2, "_")
        Rfalse = makeList(nextQuad())
        genQuad("jump", "_", "_", "_")
    return Rtrue, Rfalse


def optional_sign():
    global token
    return ADD_OP()


def call_main_part():
    global token
    if token == "main":
        token = lex()
        genQuad("begin_block", 'main', "_", "_")
        main_function_call()
        genQuad("halt", "_", "_", "_")
        genQuad("end_block", 'main', "_", "_")
        # printList(quadList)
    else:
        print('Error! Keyword "main" expected in line: ' + str(line))
        exit()


def main_function_call():
    global token
    newScope("main")
    entity = Entity.function("main", 'main_func')
    newEntity(entity)
    helpList.extend(scopes)
    declarations()  # if declaration succeeds read next token for check globals
    while 1:
        try:
            statement()
        except EOFError as e:
            return


def ADD_OP():
    global token
    op = token
    if token == '+':
        token = lex()
        return op
    elif token == '-':
        token = lex()
        return op


def MUL_OP():
    global token
    mulop = token
    if token == '*':
        token = lex()
        return mulop
    elif token == '//':
        token = lex()
        return mulop
    elif token == '%':
        token = lex()
        return mulop


def REL_OP():
    global token
    op = token
    if token == '==':
        token = lex()
        return op
    elif token == '<=':
        token = lex()
        return op
    elif token == '>=':
        token = lex()
        return op
    elif token == '>':
        token = lex()
        return op
    elif token == '<':
        token = lex()
        return op
    elif token == '!=':
        token = lex()
        return op
    else:
        print("Error! Missing 'relational operator' in line " + str(line))
        exit()


def printList(l):
    for item in l:
        print(item)


# Intermediate code

def nextQuad():
    global quadCounter
    return quadCounter


def genQuad(op, x, y, z):
    global quadList, quadCounter
    cnt = nextQuad()
    newQuad = [cnt, op, x, y, z]
    quadList.append(newQuad)
    quadCounter += 1
    return newQuad


def newTemp():
    global tempCounter
    global tempList
    temp = 'T_'
    tempCounter += 1
    temp += str(tempCounter)
    tempList += [temp]
    entity = Entity.Temp(temp, 'tmp', getOffset())
    newEntity(entity)
    return temp


def emptyList():
    empty = []
    return empty


def makeList(x):
    make = [x]
    return make


def merge(list1, list2):
    merged = []
    merged += list1 + list2
    return merged


def backPatch(lista, k):
    global quadList
    for i in range(len(lista)):
        for j in range(len(quadList)):
            if lista[i] == quadList[j][0] and quadList[j][4] == '_':
                quadList[j][4] = k
                break


def intFile(file):
    global quadList, writer
    writer = ''
    F = open(file + '.int', 'w')
    for i in range(len(quadList)):
        writer += str(quadList[i][0]) + ' ' + str(quadList[i][1]) + ' ' + str(quadList[i][2]) + ' ' + str(
            quadList[i][3]) + ' ' + str(quadList[i][4]) + '\n'
    F.write(writer + '\n')
    print("Created file : " + file + ".int")
    F.close()


# Symbol Table

class Entity:

    def __init__(self, id, state):
        self.id = id
        self.type = state
        self.scope = -1

    @classmethod
    def var(cls, id, state, offset):
        variable = cls(id, state)
        variable.offset = offset
        return variable

    @classmethod
    def function(cls, id, state):
        func = cls(id, state)
        func.squad = 0
        func.args = []
        func.length = 0
        return func

    @classmethod
    def param(cls, id, state, mode, offset):
        parameter = cls(id, state)
        parameter.mode = mode
        parameter.offset = offset
        return parameter

    @classmethod
    def Temp(cls, id, state, offset):
        temp = cls(id, state)
        temp.offset = offset
        return temp


def newScope(identifier):
    global scopes
    scopes.append([identifier, len(scopes), []])


def remScope():
    global scopes
    if scopes:
        del scopes[-1]


def newEntity(entity):
    global scopes
    if scopes:
        scopes[-1][2].append(entity)


def addArgs(entity):
    entity.args.extend(argList)


def getOffset():
    global scopes
    offset = 12
    if scopes:
        if scopes[-1][2]:
            for ent in scopes[-1][2]:
                if ent.type == 'var' or ent.type == 'tmp' or ent.type == 'prm':
                    offset += 4
        return offset


def updateFields(ent):
    ent.length = getOffset()
    ent.squad = nextQuad()


def outputSymbolFile(file):
    global scopes, writer
    writer = ''
    F = open(file + '.symb', 'a')
    writer += '======================================'
    for scope in reversed(scopes):
        writer += '\nScope ' + str(scope[1]) + '\n'
        for ent in scope[2]:
            if ent.type == 'var':
                writer += ' Variable entity: ' + ent.id + ', offset: ' + str(ent.offset) + '\n'
            elif ent.type == 'tmp':
                writer += ' Temporary variable entity: ' + ent.id + ', offset: ' + str(ent.offset) + '\n'
            elif ent.type == 'prm':
                writer += ' Parameter entity: ' + ent.id + ', mode: ' + str(ent.mode) + ', offset: ' + str(ent.offset) + '\n'
            elif ent.type == 'func':
                writer += ' Function entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', framelength: ' + str(
                    ent.length) + '\n'
            elif ent.type == 'main_func':
                writer += ' Main_Function entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', framelength: ' + str(
                    ent.length) + '\n'
    F.write(writer + '\n')
    F.close()


# Generate Final Code

def search_scope_id(id):
    global helpList
    if helpList:
        for scop in helpList[::-1]:
            for ent in scop[2]:
                if ent.id == id:
                    ent.scope = scop
                    return ent
    print(f"Entity with id {id} not found")
    return None


def printHelpList():
    global helpList
    for scop in helpList[::-1]:
        for ent in scop[2]:
            try:
                print("id: " + ent.id + " type: " + ent.type + ", offset: " + str(ent.offset))
            except AttributeError:
                print("id: " + ent.id + " type: " + ent.type)


def count_function_occurrences():
    value_counts = {}
    functions = set()

    for q in quadList:
        if q[1] == "begin_block" and q[2] != 'main':
            functions.add(q[2])

        value = q[2]
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 0

    # for key, value in value_counts.items():
    #     print(f'{key}: {value}')

    result = {}
    for f in functions:
        if 'main' in f:
            result[f] = 1
    return result


def generateMainList():
    global helpList, mainList
    for scop in helpList:
        for ent in scop[2]:
            if ent.type == "main_func":
                mainList.append(scop)


def remHelp(entityID):
    global helpList
    for scop in helpList:
        for ent in scop[2]:
            if ent.id == entityID:
                helpList.remove(ent)


def generateHelpList():
    global helpList
    temp = []
    for item in reversed(helpList):
        if item not in temp:
            temp.append(item)
    helpList = temp


def gnvlcode(v):
    global writer, helpList
    writer += ' lw $t0, -4($sp) \n'
    level = helpList[-1][1] - v.scope[1]
    for i in range(0, level):
        writer += ' lw $t0,-4($t0)\n'
    writer += ' addi  $t0, $t0, -' + str(v.offset) + '\n'


def loadvr(v, reg):
    global writer, helpList
    if str(v).isdigit():
        writer += ' li ' + str(reg) + ', ' + str(v) + '\n'
    else:
        e = search_scope_id(v)
        if e.scope[1] == helpList[-1][1] and (
                e.type == 'var' or e.type == 'tmp' or e.type == 'prm'):  # scope[1] = len(scope)
            writer += ' lw ' + reg + ', -' + str(e.offset) + '($sp)\n'
        elif e.scope[1] < helpList[-1][1] and (e.type == 'var' or e.type == 'prm'):  #
            gnvlcode(e)
            writer += ' lw ' + reg + ', ($t0)\n'


def storerv(reg, v):
    global helpList, writer
    e = search_scope_id(v)
    if str(v).isdigit():
        writer += ' li ' + str(reg) + ', ' + str(v) + '\n'
    else:
        if e.scope[1] == helpList[-1][1] and (e.type == 'var' or e.type == 'tmp' or e.type == 'prm'):
            writer += ' sw ' + reg + ', -' + str(e.offset) + '($sp)\n'
        elif e.scope[1] < helpList[-1][1] and (e.type == 'var' or e.type == 'prm'):
            gnvlcode(e)
            writer += ' sw ' + reg + ', ($t0)\n'


def produce(file):
    global quadList, writer, helpList, mainList, countFunc
    countFunc = count_function_occurrences()
    generateMainList()
    firstPar = True
    writer = ''
    st = -1
    with open(file + '.asm', 'w') as F:
        writer += ' .data\n'
        writer += ''' str_nl: .asciz "\\n"\n'''
        writer += ' .text\n'
        writer += 'L_0:\n j Lmain\n'
        for q in quadList:
            writer += 'L_' + str(q[0]) + ':\n'

            if q[1] == '=':
                loadvr(q[2], '$t1')
                storerv('$t1', q[4])

            elif q[1] in ['+', '-', '*', '//', '%']:
                loadvr(q[2], '$t1')
                loadvr(q[3], '$t2')

                if q[1] == '+':
                    writer += ' add $t1, $t1, $t2\n'
                elif q[1] == '-':
                    writer += ' sub $t1, $t1, $t2\n'
                elif q[1] == '*':
                    writer += ' mul $t1, $t1, $t2\n'
                elif q[1] == '//':
                    writer += ' div $t1, $t1, $t2\n'
                elif q[1] == '%':
                    writer += ' rem $t1, $t1, $t2\n'
                storerv('$t1', q[4])

            elif q[1] in ['<', '>', '<=', '>=', '!=', '==']:
                loadvr(q[2], '$t1')
                loadvr(q[3], '$t2')

                if q[1] == '<':
                    writer += ' blt $t1, $t2, L_' + str(q[4]) + '\n'
                elif q[1] == '>':
                    writer += ' bgt $t1, $t2, L_' + str(q[4]) + '\n'
                elif q[1] == '<=':
                    writer += ' ble $t1, $t2, L_' + str(q[4]) + '\n'
                elif q[1] == '>=':
                    writer += ' bge $t1, $t2, L_' + str(q[4]) + '\n'
                elif q[1] == '!=':
                    writer += ' bne $t1, $t2, L_' + str(q[4]) + '\n'
                elif q[1] == '==':
                    writer += ' beq $t1, $t2, L_' + str(q[4]) + '\n'

            elif q[1] == 'jump':
                writer += ' j L_' + str(q[4]) + '\n'

            elif q[1] == 'inp':
                writer += ' li $a7, 5 \n ecall \n'
                storerv('$a7', q[2])

            elif q[1] == 'out':
                loadvr(q[2], '$a0')
                writer += ' li $a7, 1\n'
                writer += ' ecall\n'
                writer += ' la $a0, str_nl\n li $a7, 4 \n ecall\n'

            elif q[1] == 'ret':
                loadvr(q[2], '$t1')
                writer += ' lw $t0, -8($sp)\n sw $t1,($t0)\n'

            elif q[1] == 'halt':
                writer += ' li a0, 0\n li a7, 93\n ecall\n'
                break

            elif q[1] == 'begin_block':
                if q[2] == 'main':
                    writer += 'Lmain: \n'
                    writer += ' addi $sp, $sp ' + str(getOffset()) + '\n move $gp, $sp \n'
                    helpList.extend(mainList)
                else:
                    writer += ' sw $ra, -0($sp)\n'

            elif q[1] == 'end_block':
                if q[2] in countFunc:
                    countFunc[q[2]] -= 1
                writer += ' lw $ra ,-0($sp) \n jr $ra\n'
                if q[2] in countFunc and countFunc[q[2]] == 0:
                    remHelp(countFunc[q[2]])

            elif q[1] == 'call':
                if q[2] in countFunc:
                    countFunc[q[2]] -= 1
                st = -1
                e = search_scope_id(q[2])
                if e is None:
                    raise ValueError(f"Entity with id {q[2]} not found in helpList")
                if e.scope[1] == helpList[-1][1]:
                    writer += ' lw $t0, -4($sp)\n sw $t0, -4($fp)\n'
                else:
                    writer += ' sw $t0, -4($fp)\n'
                writer += ' addi $sp, $sp ,' + str(e.length) + '\n jal L_' + str(
                    e.squad) + '\n addi $sp, $sp , -' + str(e.length) + '\n'
                if q[2] in countFunc and countFunc[q[2]] == 0:
                    remHelp(countFunc[q[2]])
                firstPar = True

            elif q[1] == 'par':
                e = search_scope_id(q[2])
                if e is None:
                    raise ValueError(f"Entity with id {q[2]} not found in helpList")

                if firstPar:
                    writer += ' addi $fp, $sp, ' + str(getOffset()) + '\n'
                    firstPar = False
                if st == -1:
                    st = 0
                if q[3] == 'CV':
                    loadvr(q[2], '$t0')
                    writer += ' sw $t0, -' + str(12 + 4 * st) + '($fp)\n'
                    st += 1
                elif q[3] == 'RET':
                    writer += ' addi $t0, $sp, -' + str(e.offset) + '\n'
                    writer += ' sw $t0, -8($fp)\n'
        F.write(writer + "\n")
    print("Created file : " + file + ".asm\n")
    print("Compilation Successful! \n")


f = open(sys.argv[1], encoding="utf8")
name = sys.argv[1].replace(".cpy", '')
F = open(name + ".symb", "w")
token = lex()
startRule()
intFile(name)
generateHelpList()
print("Created file : " + name + ".symb")
produce(name)
