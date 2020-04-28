import sys, shlex, operator
from constants import * 

#  TO TAKE THE TOKEN LIST AND GENERATE AN ABSTRACT SYNTAX TREE WHICH WILL BE A BINARY TREE
#  WILL READ  { LINE_NO, COL_NO,  TOKEN_TYPE, VALUE } FOR EACH TOKEN

# THE NODE CLASS
class Node():
      def __init__(self, node_type, left = None, right = None, value = None):
            self.node_type  = node_type
            self.left  = left
            self.right = right
            self.value = value

class SyntaxAnalyzer():

      # INITIALIZING THE TRACKING VARIABLES
      def __init__(self):
      
            self.TK_NAME         = 0
            self.TK_RIGHT_ASSOC  = 1
            self.TK_IS_BINARY    = 2
            self.TK_IS_UNARY     = 3
            self.TK_PRECEDENCE   = 4
            self.TK_NODE         = 5
 
            self.input_file = open('OLexicalAnalyzer.txt','r')
            self.outfile = open('OSyntaxAnalyzer.txt','w')

            self.err_line   = None
            self.err_col    = None
            self.tok        = None
            self.tok_text   = None
            self.tok_other  = None

 
      # NODE CLASS FUNCTIONS
      def make_node(self,oper, left, right = None):
            return Node(oper, left, right)
      
      def make_leaf(self,oper, n):
            return Node(oper, value = n)



      # ERROR MESSAGE DISPLAYER
      def error(self,msg):
            print("(%d, %d) %s" % (int(self.err_line), int(self.err_col), msg))
            exit(1)

      # NEXT TOKEN SCANNER
      def gettok(self):
            line = self.input_file.readline()
            if len(line) == 0:
                  self.error("empty line")
            line_list = shlex.split(line, False, False)
            self.err_line = line_list[0]
            self.err_col  = line_list[1]
            self.tok_text = line_list[2]
            self.tok = SYMB_TOKEN.get(self.tok_text)
            if self.tok == None:
                  self.error("Unknown token %s" % (self.tok_text))
            self.tok_other = None
            if self.tok in [INT, IDENT, STR]:
                  self.tok_other = line_list[3]

      def expect(self,msg, s):
            if self.tok == s:
                  self.gettok()
            else:
                  self.error("%s: Expecting '%s', found '%s'" % (msg, TOKENS[s][self.TK_NAME], TOKENS[self.tok][self.TK_NAME]))


      # THE EXPRESSING NODE GRAMMAR PARSING
      def expr(self, p):
            x = None
            if self.tok == LPAR:
                  x = self.paren_expr()
            elif self.tok in [SUB, ADD]:
                  op = (NEG if self.tok == SUB else ADD)
                  self.gettok()
                  node = self.expr(TOKENS[NEG][self.TK_PRECEDENCE])
                  x = (self.make_node(ND_NEG, node) if op == self.NEG else node)
            elif self.tok == NOT:
                  self.gettok()
                  x = self.make_node(ND_NOT, self.expr(TOKENS[NOT][self.TK_PRECEDENCE]))
            elif self.tok == IDENT:
                  x = self.make_leaf(ND_IDENT, self.tok_other)
                  self.gettok()
            elif self.tok == INT:
                  x = self.make_leaf(ND_INT, self.tok_other)
                  self.gettok()
            else:
                  self.error("Expecting a primary, found: %s" % (TOKENS[self.tok][self.TK_NAME]))
            
            
            while TOKENS[self.tok][self.TK_IS_BINARY] and TOKENS[self.tok][self.TK_PRECEDENCE] >= p:
                  op = self.tok
                  self.gettok()
                  q = TOKENS[op][self.TK_PRECEDENCE]
                  if not TOKENS[op][self.TK_RIGHT_ASSOC]:
                        q += 1
                  node = self.expr(q)
                  x = self.make_node(TOKENS[op][self.TK_NODE], x, node)
            return x
 

      # THE PARENTHESES NODE GRAMMAR PARSER
      def paren_expr(self):
            self.expect("paren_expr", LPAR)
            node = self.expr(0)
            self.expect("paren_expr", RPAR)
            return node


      def stmt(self):
            t = None
            if self.tok == IF:
                  self.gettok()
                  e = self.paren_expr()
                  s = self.stmt()
                  s2 = None
                  if self.tok == ELSE:
                        self.gettok()
                        s2 = self.stmt()
                  t = self.make_node(ND_IF, e, self.make_node(ND_IF, s, s2))
            
            elif self.tok == PUTC:
                  self.gettok()
                  e = self.paren_expr()
                  t = self.make_node(ND_PRTC, e)
                  self.expect("Putc", SEMI)
            
            elif self.tok == PRINT:
                  self.gettok()
                  self.expect("Print", LPAR)
                  while True:
                        if self.tok == STR:
                              e = self.make_node(ND_PRTS, self.make_leaf(ND_STR, self.tok_other))
                              self.gettok()
                        else:
                              e = self.make_node(ND_PRTI, self.expr(0))
                        t = self.make_node(ND_SEQ, t, e)
                        if self.tok != COMMA:
                              break
                        self.gettok()
                  self.expect("Print", RPAR)
                  self.expect("Print", SEMI)
            
            elif self.tok == SEMI:
                  self.gettok()

            elif self.tok == IDENT:
                  v = self.make_leaf(ND_IDENT, self.tok_other)
                  self.gettok()
                  self.expect("assign", ASS)
                  e = self.expr(0)
                  t = self.make_node(ND_ASS, v, e)
                  self.expect("assign", SEMI)

            elif self.tok == WHILE:
                  self.gettok()
                  e = self.paren_expr()
                  s = self.stmt()
                  t = self.make_node(ND_WHILE, e, s)

            elif self.tok == LBRA:
                  self.gettok()
                  while self.tok != RBRA and self.tok != EOI:
                        t = self.make_node(ND_SEQ, t, self.stmt())
                  self.expect("Lbrace", RBRA)

            elif self.tok == EOI:
                  pass

            else:
                  self.error("Expecting start of statement, found: %s" % (TOKENS[self.tok][self.TK_NAME]))
            return t
 
      def parse(self):
            t = None
            self.gettok()
            while True:
                  t = self.make_node(ND_SEQ, t, self.stmt())
                  if self.tok == EOI or t == None:
                        break
            return t
      
      def prt_ast(self,t):
            if t == None:
                  print(";",file=self.outfile)
            else:
                  print("%-14s" % (DISPLAY_NODES[t.node_type]), end='',file=self.outfile)
                  if t.node_type in [ND_IDENT, ND_INT]:
                        print("%s" % (t.value),file=self.outfile)
                  elif t.node_type == ND_STR:
                        print("%s" %(t.value),file=self.outfile)
                  else:
                        print("",file=self.outfile)
                        self.prt_ast(t.left)
                        self.prt_ast(t.right)
      
      def build_ast(self):
            self.prt_ast(self.parse())
            self.input_file.close()
            self.outfile.close()



if __name__=='__main__':
      analyzer =  SyntaxAnalyzer()
      analyzer.build_ast()
