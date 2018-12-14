import ply.yacc as yacc
from analizadorLexicoRuby import tokens
import re
import codecs
import os
import sys

#prog = ''

precedence = (
    ('left','EXPO'),
    ('left','NE'),
    ('left','PLUS'),
    ('left','MINUS'),
    ('left','TIMES'),
    ('left','DIVIDE'),
    ('left','MODULO'),
    ('right','EQUALS'),
    ('left','LPAREN'),
    ('left','RPAREN'),
)

def p_PROGRAM(p):
    '''
    PROGRAM : {}
    '''.format("start")

def p_start(p):
    '''
    start : asign
    | ifstament
    | forstament
    '''


def p_ifstament(p):
    '''
    ifstament : if logical ending ifcode ending end
    '''

def p_ifcode(p):
    '''
    ifcode : puts IDENTIFICADOR
    | puts INTEGER
    | puts FLOAT
    | puts STRING
    | puts CHARACTER
    | ifstament
    | forstament
    | puts expression
    | ifcodecs
    '''
    
def p_ifcodecs(p):
    '''
    ifcodecs : puts IDENTIFICADOR
    | puts INTEGER
    | puts FLOAT
    | puts STRING
    | puts CHARACTER
    | puts expression
    '''

def p_logical(p):
    '''
    logical : var LT var
    | var GT var
    | var LE var
    | var GE var
    | var EQ var
    | var NE var
    | var NOT var
    '''

def p_var(p):
    '''
    var : IDENTIFICADOR
    | INTEGER
    | FLOAT
    | STRING
    | true
    | false
    '''

def p_forstament(p):
    '''
    forstament : for IDENTIFICADOR in INTEGER PERIODOUBLE INTEGER doptional ending ifcode ending end
    '''
    
def p_doptional(p):
    '''
    doptional : do
    | blank
    '''

def p_ending(p):
    '''
    ending : blank
    '''

def p_eblank(p):
    '''
    eblank : \r\n
    | blank
    '''

def p_blank(p):
    '''
    blank :
    '''

#Asignacion tipos de variable o id = += -= *= /= %= **= expresion
def p_asign(p):
    '''
    asign : idtype asigntypes expression
    '''
#Tipos identificador, variableglobal, variableinstantanea, variableclase
def p_idtype(p):
    '''
    idtype : IDENTIFICADOR
    | VAR_GLOBAL
    | VAR_INSTANT
    | VAR_CLASS
    '''
#Tipos de asignacion
def p_asigntypes(p):
    '''
    asigntypes : EQUALS
    | PLUSEQUAL
    | MINUSEQUAL
    | TIMESEQUAL
    | DIVEQUAL
    | MODEQUAL
    | EXPEQUAL
    '''

def p_expression_plus(p):
    'expression : expression PLUS term'

def p_expression_minus(p):
    'expression : expression MINUS term'

def p_expression_term(p):
    'expression : term'

def p_term_times(p):
    'term : term TIMES factor'

def p_term_div(p):
    'term : term DIVIDE factor'
    
def p_term_exponent(p):
    'term : term EXPO factor'

def p_term_factor(p):
    'term : factor'

#Simbolos + - u epsilon(blank)
def p_asignsimbol(p):
    '''
    asignsimbol : PLUS
    | MINUS
    | blank
    '''

def p_factor_num(p):
    '''
    factor : asignsimbol INTEGER
           | asignsimbol FLOAT
    '''
def p_factor_stringorchar(p):
    '''
    factor : STRING
    '''

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'


def p_factor_expr_error(p):
    'asign : idtype asigntypes error ending'


def p_error(p):
    if p:
        print("Error de Sintaxis!  Valor:{} Linea:{} Tipo:{}".format(str(p.value), str(p.lineno - 1), str(p.type)))
        parser.errok()
    else:
        print('Error de Sintaxis! de cierre! {}'.format(str(parser.token())))

#op = "" 
# Seleccionar archivo
def searchFile(d):
    ficher = []
    numberFile = ''
    answer = False
    cont = 1
    print ("LISTA DE ARCHIVOS:")
    for base, dirs, files in os.walk(d):
        ficher.append(files)
        
    for file in files:
        print (str(cont) + ". " + file)
        cont = cont + 1
    #print('\nFORMAS')    
    #print("a. Estructura FOR")
    #print("b. Estructura IF")
    #print("c. Variable")
    while answer == False:
       numberFile = input('\nArchivo?: ')
       #op = input("Evaluar?:")
       #if op == 'a':
        #   prog = 'forstruct'
       #if op == 'b':
        #   prog = 'ifstruct'
       #if op == 'c':
        #  prog = 'asign'
       for file in files:
           if file == files[int(numberFile)-1]:
               answer = True
               break
    print ("Has escogido \"%s\" \n" %files[int(numberFile)-1])
    return files[int(numberFile)-1]

parser = yacc.yacc()
def syntax(item):
    #for item in data.splitlines():
     #   if item:
    parser.parse(item)           

#Leer archivo directo
rp = True
while rp:
    directory = 'test/'
    file = searchFile(directory)
    test = directory + file
    fp = codecs.open(test, "r", "ansi")
    st = str(fp.read())
    print("Codigo:\r\n{}".format(st))
    syntax(st)
    rs = input("Continuar Y/N: <\\")
    if rs == 'Y' or rs == 'y':
        rp = True
    elif rs == 'N' or rs == 'n':
        rp = False
    else:
        rp = False
    fp.close()
        
