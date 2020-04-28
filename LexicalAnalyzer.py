from constants import *
import sys

################################################################################################################################
#### LEXICAL ANALYZER TO GENERATE THE LIST OF TOKENS FROM THE INPUT PROGRAM w
#### WILL GENERATE  { LINE_NO, COL_NO,  TOKEN_TYPE, VALUE } FOR EACH TOKEN
################################################################################################################################


class LexicalAnalyzer():

      #################### INITALIZING THE TRACKING VARIABLES 
      def __init__(self):
            self.curr_ch = " "                  # CURR CHAR
            self.curr_col = 0                   # CURR COL NO
            self.curr_line = 1                  # CURR LINE NO
            self.input_file = open('input.txt','r')         
            self.outfile = open('OLexicalAnalyzer.txt','w')
            
      ##################### RETURN TOKEN TYPE
      def gettok(self):
            while self.curr_ch.isspace():
                  self.next_ch()
            err_line = self.curr_line
            err_col  = self.curr_col
            if len(self.curr_ch) == 0:    return EOI, err_line, err_col
            elif self.curr_ch == '/':     return self.div_or_cmt(err_line, err_col)
            elif self.curr_ch == '\'':    return self.char_lit(err_line, err_col)
            elif self.curr_ch == '<':     return self.follow('=', LEQ, LES,err_line, err_col)
            elif self.curr_ch == '>':     return self.follow('=', GEQ, GTR,err_line, err_col)
            elif self.curr_ch == '=':     return self.follow('=', EQ,  ASS,err_line, err_col)
            elif self.curr_ch == '!':     return self.follow('=', NEQ, NOT,err_line, err_col)
            elif self.curr_ch == '&':     return self.follow('&', AND, EOI,err_line, err_col)
            elif self.curr_ch == '|':     return self.follow('|', OR,  EOI,err_line, err_col)
            elif self.curr_ch == '"':     return self.string_lit(err_line, err_col)
            elif self.curr_ch in SYMBOLS:
                  sym = SYMBOLS[self.curr_ch]
                  self.next_ch()
                  return sym, err_line, err_col
            else: return self.ident_or_int(err_line, err_col)

      ##################### ERROR MESSAGE DISPLAYER
      def error(self,lno,colno,msg):
            print(lno,colno,msg)
            exit(1)


      ##################### NEXT CHARACTER SCANNER
      def next_ch(self):
            self.curr_ch = self.input_file.read(1)
            self.curr_col += 1
            if self.curr_ch == '\n':
                  self.curr_line += 1
                  self.curr_col = 0
            return self.curr_ch


      ##################### IF NEXT INPUT IS A CHARACTER LITERAL 'a'
      def char_lit(self,err_line, err_col):
            n = ord(self.next_ch())              # skip opening quote
            if self.curr_ch == '\'':
                  self.error(err_line, err_col, "empty character constant")
            elif self.curr_ch == '\\':
                  self.next_ch()
                  if self.curr_ch == 'n':
                        n = 10
                  elif self.curr_ch == '\\':
                        n = ord('\\')
                  else:
                        self.error(err_line, err_col, "unknown escape sequence \\%c" % (self.curr_ch))
            if self.next_ch() != '\'':
                  self.error(err_line, err_col, "multi-character constant")
            self.next_ch()
            return INT, err_line, err_col, n


      #################### IF NEXT INPUT IS A STRING LITERAL
      def string_lit(self,err_line,err_col):
            start= self.curr_ch
            text = ""
            while self.next_ch() != start:
                  if len(self.curr_ch) == 0:
                        self.error(err_line,err_col,"EOF while scanning string literal")
                  if self.curr_ch == '\n':
                        self.error(err_line,err_col,"EOL while scanning string literal")
                  text += self.curr_ch
            self.next_ch()
            return STR, err_line, err_col, text
      

      ##################### IF NEXT TOKEN IS A DIVISION OP OR A COMMENT
      def div_or_cmt(self,err_line,err_col):
            if self.next_ch() != '*':
                  # A DIVISION OPERATOR
                  return DIV, err_line, err_col
            
            # IF A COMMENT, SCAN ALL COMMENTS AND GET NEXT VALID CHARACTER
            self.next_ch()
            while True:
                  if self.curr_ch == '*':
                        if self.next_ch() == '/':
                              self.next_ch()
                        return self.gettok()
                  elif len(self.curr_ch) == 0:  # MAKE SURE COMMENT HAS AN ENDING */
                        self.error(err_line,err_col,"EOF in comment")
                  else:
                        self.next_ch()
 

      ####################### IF NEXT INPUT IS AN IDENTIFIER
      def ident_or_int(self,err_line,err_col):
            is_number = True
            text = ""
            while self.curr_ch.isalnum() or self.curr_ch == '_':
                  text += self.curr_ch
                  if not self.curr_ch.isdigit():
                        is_number = False
                  self.next_ch()
            
            if len(text) == 0:
                  self.error(err_line,err_col,"ident_or_int: unrecognized character: (%d) '%c'" % (ord(self.curr_ch), self.curr_ch))
            
            if text[0].isdigit():
                  if not is_number:
                        self.error(err_line,err_col,"invalid number: %s" % (text))
                  n = int(text)
                  return INT, err_line, err_col, n
            
            if text in KEYWORDS:
                  return KEYWORDS[text], err_line, err_col
            
            return IDENT, err_line, err_col, text
      

      ######################## LOOKAHEAD FOR OPERATORS CAN CAN HAVE 2 CHARACTERS like <=
      def follow(self,expected, ifyes, ifno,err_line,err_col):
            if self.next_ch() == expected:
                  self.next_ch()
                  return ifyes, err_line, err_col
            if ifno == EOI:
                  self.error(err_line,err_col,"follow: unrecognized character: (%d) '%c'" % (ord(self.curr_ch), self.curr_ch))
            return ifno, err_line, err_col
  

      ######################## DRIVER  
      def start_scan(self):
            while True:
                  t = self.gettok()
                  tok  = t[0]
                  line = t[1]
                  col  = t[2]

                  print("%5d  %5d   %-14s" % (line, col, TOKEN_LIST[tok]), end='',file=self.outfile)
                  if tok == INT:          print("   %5d" % (t[3]),file=self.outfile)
                  elif tok == IDENT:      print("  %s" %   (t[3]),file=self.outfile)
                  elif tok == STR:        print('  "%s"' % (t[3]),file=self.outfile)
                  else:                   print("",file=self.outfile)
                  
                  if tok == EOI:
                        break
            self.input_file.close()
            self.outfile.close()
            

######################################################################################## CLASS ENDS
if __name__ == '__main__':
      scanner =  LexicalAnalyzer()
      scanner.start_scan()