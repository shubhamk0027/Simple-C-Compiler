"""
      EBNF..................................
      stmt_list           =   {stmt} ;
      stmt                =   ';'
                          | Identifier '=' expr ';'
                          | 'while' paren_expr stmt
                          | 'if' paren_expr stmt ['else' stmt]
                          | 'print' '(' prt_list ')' ';'
                          | 'putc' paren_expr ';'
                          | '{' stmt_list '}'
                          ;
      paren_expr          =   '(' expr ')' ;
      prt_list            =   (string | expr) {',' (String | expr)} ;
      expr                =   and_expr            {'||' and_expr} ;
      and_expr            =   equality_expr       {'&&' equality_expr} ;
      equality_expr       =   relational_expr     [('==' | '!=') relational_expr] ;
      relational_expr     =   addition_expr       [('<' | '<=' | '>' | '>=') addition_expr] ;
      addition_expr       =   multiplication_expr {('+' | '-') multiplication_expr} ;
      multiplication_expr =   primary             {('*' | '/' | '%') primary } ;
      primary             =   Identifier
                              | Integer
                              | '(' expr ')'
                              | ('+' | '-' | '!') primary
                              ;

NODES:
      Identifier String Integer Sequence If Prtc Prts Prti While Assign Negate Not Multiply Divide Mod
      Add Subtract Less LessEqual Greater GreaterEqual Equal NotEqual And Or

NON TERMINAL NODES:
      FOR BINARY OPERATORS:
            like - Multiply Divide Mod Add Subtract Less LessEqual Greater GreaterEqual Equal NotEqual And Or
            =>(Operator expression expression)
      FOR UNARY OPERATORS:
            like - NOT NEG
            =>(Operator expression ;)

"""


##############################################################################################
##############################################################################################
##############################################################################################

# BINARY OPERATORS LIKE | AND & ARE NOT HANDLED
# MULTI LINE COMMENTS NOT SINGLE LINE COMMENTS
# only INT OR STRING without any keyword
# WHILE AND IF
# print( "something",something)

TOKEN_LIST = [
      "End_of_input", 
      "Op_multiply", 
      "Op_divide", 
      "Op_mod", 
      "Op_add", 
      "Op_subtract",
      "Op_negate", 
      "Op_not", 
      "Op_less", 
      "Op_lessequal", 
      "Op_greater", 
      "Op_greaterequal",
      "Op_equal", 
      "Op_notequal", 
      "Op_assign", 
      "Op_and", 
      "Op_or", 
      "Keyword_if",
      "Keyword_else", 
      "Keyword_while", 
      "Keyword_print", 
      "Keyword_putc", 
      "LeftParen",
      "RightParen", 
      "LeftBrace", 
      "RightBrace", 
      "Semicolon", 
      "Comma", 
      "Identifier",
      "Integer", 
      "String"
]

# ASSIGNING INDEX TO ALL THE TOKENS
EOI, MUL, DIV, MOD, ADD, SUB, NEG, NOT, LES, LEQ, GTR, \
GEQ, EQ, NEQ, ASS, AND, OR, IF, ELSE, WHILE, PRINT,       \
PUTC, LPAR, RPAR, LBRA, RBRA, SEMI, COMMA, IDENT,          \
INT, STR = range(31)
 
SYMBOLS = { 
      '{': LBRA, 
      '}': RBRA, 
      '(': LPAR, 
      ')': RPAR, 
      '+': ADD, 
      '-': SUB,
      '*': MUL, 
      '%': MOD, 
      ';': SEMI, 
      ',': COMMA 
}
# LOGICAL OPERATORS ARE HANDLED SEPARATELY 
KEYWORDS = {
      'if': IF, 
      'else': ELSE, 
      'print': PRINT, 
      'putc': PUTC, 
      'while': WHILE
}

##############################################################################################
##############################################################################################
##############################################################################################

# NODES OF THE SYNTAX TREE

ND_IDENT, ND_STR, ND_INT, ND_SEQ, ND_IF, ND_PRTC, ND_PRTS, ND_PRTI, ND_WHILE, \
ND_ASS, ND_NEG, ND_NOT, ND_MUL, ND_DIV, ND_MOD, ND_ADD, ND_SUB, ND_LES, ND_LEQ,     \
ND_GTR, ND_GEQ, ND_EQ, ND_NEQ, ND_AND, ND_OR = range(25)

# 25 NODES
DISPLAY_NODES = [
    "Identifier", "String", "Integer", "Sequence", "If", "Prtc", "Prts", "Prti", "While", 
    "Assign", "Negate", "Not", "Multiply", "Divide", "Mod", "Add","Subtract", "Less", "LessEqual", 
    "Greater", "GreaterEqual", "Equal", "NotEqual", "And", "Or"]

# NON TERMINAL NODES (FOR OPERATORS BASICALLY )
# Multiply Divide Mod Add Subtract Less LessEqual Greater GreaterEqual Equal NotEqual And Or

TOKENS = [
    ["EOI"             , False, False, False, -1, -1        ],
    ["*"               , False, True,  False, 13, ND_MUL    ],
    ["/"               , False, True,  False, 13, ND_DIV    ],
    ["%"               , False, True,  False, 13, ND_MOD    ],
    ["+"               , False, True,  False, 12, ND_ADD    ],
    ["-"               , False, True,  False, 12, ND_SUB    ],
    ["-"               , False, False, True,  14, ND_NEG    ],
    ["!"               , False, False, True,  14, ND_NOT    ],
    ["<"               , False, True,  False, 10, ND_LES    ],
    ["<="              , False, True,  False, 10, ND_LEQ    ],
    [">"               , False, True,  False, 10, ND_GTR    ],
    [">="              , False, True,  False, 10, ND_GEQ    ],
    ["=="              , False, True,  False,  9, ND_EQ     ],
    ["!="              , False, True,  False,  9, ND_NEQ    ],
    ["="               , False, False, False, -1, ND_ASS    ],
    ["&&"              , False, True,  False,  5, ND_AND    ],
    ["||"              , False, True,  False,  4, ND_OR     ],
    ["if"              , False, False, False, -1, ND_IF     ],
    ["else"            , False, False, False, -1, -1        ],
    ["while"           , False, False, False, -1, ND_WHILE  ],
    ["print"           , False, False, False, -1, -1        ],
    ["putc"            , False, False, False, -1, -1        ],
    ["("               , False, False, False, -1, -1        ],
    [")"               , False, False, False, -1, -1        ],
    ["{"               , False, False, False, -1, -1        ],
    ["}"               , False, False, False, -1, -1        ],
    [";"               , False, False, False, -1, -1        ],
    [","               , False, False, False, -1, -1        ],
    ["Ident"           , False, False, False, -1, ND_IDENT  ],
    ["Integer literal" , False, False, False, -1, ND_INT    ],
    ["String literal"  , False, False, False, -1, ND_STR    ]
]
 
SYMB_TOKEN = {
      "End_of_input"   :  EOI,     "Op_multiply"    : MUL,
      "Op_divide"      :  DIV,     "Op_mod"         : MOD,
      "Op_add"         :  ADD,     "Op_subtract"    : SUB,
      "Op_negate"      :  NEG,     "Op_not"         : NOT,
      "Op_less"        :  LES,     "Op_lessequal"   : LEQ,
      "Op_greater"     :  GTR,     "Op_greaterequal": GEQ,
      "Op_equal"       :  EQ,      "Op_notequal"    : NEQ,
      "Op_assign"      :  ASS,     "Op_and"         : AND,
      "Op_or"          :  OR,      "Keyword_if"     : IF,
      "Keyword_else"   :  ELSE,    "Keyword_while"  : WHILE,
      "Keyword_print"  :  PRINT,   "Keyword_putc"   : PUTC,
      "LeftParen"      :  LPAR,    "RightParen"     : RPAR,
      "LeftBrace"      :  LBRA,    "RightBrace"     : RBRA,
      "Semicolon"      :  SEMI,    "Comma"          : COMMA,
      "Identifier"     :  IDENT,   "Integer"        : INT,
      "String"         :  STR
}

SYMB_NODE = {
      "Identifier"  : ND_IDENT,    "String"      : ND_STR,
      "Integer"     : ND_INT,      "Sequence"    : ND_SEQ,
      "If"          : ND_IF,       "Prtc"        : ND_PRTC,
      "Prts"        : ND_PRTS,     "Prti"        : ND_PRTI,
      "While"       : ND_WHILE,    "Assign"      : ND_ASS,
      "Negate"      : ND_NEG,      "Not"         : ND_NOT,
      "Multiply"    : ND_MUL,      "Divide"      : ND_DIV,
      "Mod"         : ND_MOD,      "Add"         : ND_ADD,
      "Subtract"    : ND_SUB,      "Less"        : ND_LES,
      "LessEqual"   : ND_LEQ,      "Greater"     : ND_GTR,
      "GreaterEqual": ND_GEQ,      "Equal"       : ND_NEQ,
      "NotEqual"    : ND_NEQ,      "And"         : ND_AND,
      "Or"          : ND_OR
}

##############################################################################################
##############################################################################################
##############################################################################################

OP_FETCH, OP_STORE, OP_PUSH, OP_ADD, OP_SUB, OP_MUL, OP_DIV, OP_MOD, OP_LT, OP_GT, OP_LE, OP_GE, OP_EQ, OP_NE, OP_AND, OP_OR, OP_NEG, OP_NOT, \
OP_JMP, OP_JZ, OP_PRTC, OP_PRTS, OP_PRTI, OP_HALT = range(24)

OPERATORS = {
      ND_LES: OP_LT,
      ND_GTR: OP_GT,
      ND_LEQ: OP_LE,
      ND_GEQ: OP_GE,
      ND_EQ:  OP_EQ,
      ND_NEQ: OP_NE,
      ND_AND: OP_AND,
      ND_OR:  OP_OR,
      ND_SUB: OP_SUB,
      ND_ADD: OP_ADD,
      ND_DIV: OP_DIV,
      ND_MUL: OP_MUL,
      ND_MOD: OP_MOD
}

UNARY_OPERATORS = {
      ND_NEG: NEG, 
      ND_NOT: NOT
}


##############################################################################################
##############################################################################################
##############################################################################################

STR_OP = {
    "fetch": OP_FETCH,
    "store": OP_STORE,
    "push":  OP_PUSH,
    "add":   OP_ADD,
    "sub":   OP_SUB,
    "mul":   OP_MUL,
    "div":   OP_DIV,
    "mod":   OP_MOD,
    "lt":    OP_LT,
    "gt":    OP_GT,
    "le":    OP_LE,
    "ge":    OP_GE,
    "eq":    OP_EQ,
    "ne":    OP_NE,
    "and":   OP_AND,
    "or":    OP_OR,
    "not":   OP_NOT,
    "neg":   OP_NEG,
    "jmp":   OP_JMP,
    "jz":    OP_JZ,
    "prtc":  OP_PRTC,
    "prts":  OP_PRTS,
    "prti":  OP_PRTI,
    "halt":  OP_HALT
}
