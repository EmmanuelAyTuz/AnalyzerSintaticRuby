import ply.lex as lex
#import ply.yacc as yacc
import re
import codecs
import os
import sys

#Palabras reservadas
reservada = (
    # Palabras Reservadas de RUBY
    'alias',
    'andp',
    'break',
    'BEGIN',#MAYUSCULA
    'begin',#Minuscula
    'case',
    'class',
    'def',
    'do',
    'else',
    'elsif',
    'END',#MAYUSCULA
    'end',#Minuscula
    'ensure',
    'false',
    'true',
    'for',
    'if',
    'in',
    'module',
    'next',
    'nil',
    'notp',
    'orp',
    'redo',
    'rescue',
    'retry',
    'return',
    'self',
    'super',
    'then',
    'undef',
    'unless',
    'until',
    'when',
    'while',
    'yield',
    'puts',#print by python
)


# Lista de tokens
tokens = reservada + (
    'IDENTIFICADOR',
    # Variables no SE VAN USAR POR AHORA
    'VARLOCAL','VAR_GLOBAL','VAR_INSTANT', 'VAR_CLASS',
    
    # Literales (Identificador, Entero, Flotante, Cadena, Caracter)
    'TYPEID', 'INTEGER', 'FLOAT', 'STRING', 'CHARACTER',

    # Operadores (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'XOR', 'LSHIFT', 'RSHIFT',
    #Extra
    'EXPO',
    
    # OR, AND, NOT son los simbolos |, & !=
    'OR', 'AND', 'NOT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Asignacion (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',
    # Extra
    'EXPEQUAL',

    # Incremento/decrement0 (++,--)
    'INCREMENT', 'DECREMENT',

    # Desreferencia de estructura (->)
    'ARROW',

    # Operador ternario (?)
    'TERNARY',

    # Delimitadores ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Elipsis (...)
    'ELLIPSIS',

    #PERIOD BY FOR?
    'PERIODOUBLE',

    # Identificador
    'FUNC', 'COMDOB'
)


# Funciones
#t_FUNC = r'gets|puts'

def t_puts(t):
    r'puts'
    return t

# Palabras reservadas de RUBY VAMOS A CONVERIR ESTAS A DEFINICIONES
def t_BEGIN(t):
    r'\bBEGIN\b'
    return t

def t_begin(t):
    r'\bbegin\b'
    return t

def t_END(t):
    r'\bEND\b'
    return t

def t_end(t):
    r'end'
    return t
    
def t_alias(t):
    r'\balias\b'
    return t
#Especial 
def t_andp(t):
    r'\band\b'
    return t

def t_break(t):
    r'\bbreak\b'
    return t
 
def t_case(t):
    r'\bcase\b'
    return t
 
def t_class(t):
    r'\bclass\b'
    return t
 
def t_def(t):
    r'\bdef\b'
    return t

def t_defined(t):
    r'\bdefined?\b'
    return t

def t_do(t):
    r'\bdo\b'
    return t

def t_else(t):
    r'\belse\b'
    return t

def t_elsif(t):
    r'\belsif\b'
    return t

def t_ensure(t):
    r'\bensure\b'
    return t


def t_false(t):
    r'\bfalse\b'
    return t

def t_for(t):
    r'\bfor\b'
    return t

def t_if(t):
    r'\bif\b'
    return t

def t_in(t):
    r'\bin\b'
    return t

def t_module(t):
    r'\bmodule\b'
    return t


def t_next(t):
    r'\bnext\b'
    return t

def t_nil(t):
    r'\bnil\b'
    return t
#Especial
def t_notp(t):
    r'\bnot\b'
    return t
#Especial
def t_orp(t):
    r'\bor\b'
    return t

def t_redo(t):
    r'\redo\b'
    return t


def t_rescue(t):
    r'\brescue\b'
    return t

def t_retry(t):
    r'\bretry\b'
    return t

def t_return(t):
    r'\breturn\b'
    return t

def t_self(t):
    r'\bself\b'
    return t

def t_super(t):
    r'\bsuper\b'
    return t


def t_then(t):
    r'\bthen\b'
    return t

def t_true(t):
    r'\btrue\b'
    return t

def t_undef(t):
    r'\bundef\b'
    return t

def t_unless(t):
    r'\bunless\b'
    return t

def t_until(t):
    r'\buntil\b'
    return t


def t_when(t):
    r'\bwhen\b'
    return t

def t_while(t):
    r'\bwhile\b'
    return t

def t_yield(t):
    r'\byield\b'
    return t


# Variables Local, Global, Intantanea y Clase
#t_VARLOCAL = r'_[a-z][a-zA-Z0-9]+'
t_VAR_GLOBAL = r'\$[\w]+'
t_VAR_INSTANT = r'\@[\w]+'
t_VAR_CLASS = r'\@@[\w]+'

# Operador ?
t_TERNARY          = r'\?'

# Operadores regex
t_PLUS             = r'\+'
t_MINUS            = r'\-'
t_TIMES            = r'\*'
t_DIVIDE           = r'\/'
t_MODULO           = r'\%'
t_OR               = r'\|'
t_AND              = r'\&'
t_NOT              = r'\!'
t_XOR              = r'\^'
t_LSHIFT           = r'\<\<'
t_RSHIFT           = r'\>\>'
t_LOR              = r'\|\|'
t_LAND             = r'\&\&'
#t_LNOT             = r'!'
t_LT               = r'\<'
t_GT               = r'\>'
t_LE               = r'\<='
t_GE               = r'\>='
t_EQ               = r'\=='
t_NE               = r'\!='
# Extra
t_EXPO = r'\*\*'

# Operadores de asignacion regex
t_EQUALS           = r'='
t_TIMESEQUAL       = r'\*='
t_DIVEQUAL         = r'/='
t_MODEQUAL         = r'%='
t_PLUSEQUAL        = r'\+='
t_MINUSEQUAL       = r'-='
t_LSHIFTEQUAL      = r'<<='
t_RSHIFTEQUAL      = r'>>='
t_ANDEQUAL         = r'&='
t_OREQUAL          = r'\|='
t_XOREQUAL         = r'\^='
# Extra exponente
t_EXPEQUAL = r'\*\*\='

# Incremento/decremento
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

# ->
t_ARROW            = r'->'

# Delimitadores
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'
t_ELLIPSIS         = r'\.\.\.'
#t_COMDOB = r'\"'
#Especial
t_PERIODOUBLE = r'\.\.'

# Ignorar espacios y tab
t_ignore = ' \t'

# Ignorar Comentarios
t_ignore_COMMENT = r'\#.*'

# Ignorar Saltos de linea
def t_newline(t):
   r'\r\n+'
   t.lexer.lineno += len(t.value)


#ID como definición
#def t_IDENTIFICADOR(t):
#    r'\w+(_\d\w)*'
#    return t

#ID
t_IDENTIFICADOR = r'\w+(_\d\w)*'

# Enteros
t_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Flotantes
t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# Cadena
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Caracteres
t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

# Captura de errores
def t_error(t):
    print ("Caracter ilegal '%s'" %t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


# Prueba de ingreso
def prueba(data):
    analizador = lex.lex()
    analizador.input(data)
    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos))
        print (estado)
        
#Instanciamos el analizador lexico
analizador = lex.lex()

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
    while answer == False:
       numberFile = input('\nArchivo?: ')
       for file in files:
           if file == files[int(numberFile)-1]:
               answer = True
               break
    print ("Has escogido \"%s\" \n" %files[int(numberFile)-1])
    return files[int(numberFile)-1]

#Leer archivo directo
rp = True
while rp:
    directory = 'test/'
    file = searchFile(directory)
    test = directory + file
    fp = codecs.open(test, "r", "ansi")
    st = str(fp.read())
    print("Codigo:\r\n{}".format(st))
    prueba(st)
    rs = input("Continuar Y/N: <\\")
    if rs == 'Y' or rs == 'y':
        rp = True
    elif rs == 'N' or rs == 'n':
        rp = False
    else:
        rp = False
    fp.close()



