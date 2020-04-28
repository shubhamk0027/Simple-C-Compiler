from constants import *
import sys, struct, shlex
# USING THE PREDEFINED PYTHON LIBRARY FOR PERFORMING THE BASIC OPERATIONS LIKE ADD..
import operator   


# THE NODE OF BINARY AST
## IN AST, IDENTIFIER, INTEGER, and STRING, are terminal nodes
class Node:
      def __init__(self, node_type, left = None, right = None, value = None):
            self.node_type  = node_type
            self.left  = left
            self.right = right
            self.value = value

def make_node(oper, left, right = None):
      return Node(oper, left, right)

def make_leaf(oper, n):
      return Node(oper, value = n)



## INPUT THE FLATTENED ABSTRACT SYNTAX TREE GENERATED
## FOR PERFORMING THE BASIC OPERATIONS USING PYTHON OPEATOR LIBRARY

# OUTPUT FORMAT:
      # NUMBER OF VARIABLES
      # NUMBER OF STRING LITERALS
      # ALL STRING LITERALS
      # ASSEMBLY CODES
      # .....
      # ASSEMBLY CODES

# REGISTER VARAIBLES: [32 BIT VARS]
      # sp: the stack pointer - points to the next top of stack. The stack is a 32-bit integer array.
      # pc: the program counter - points to the current instruction to be performed. The code is an array of bytes.

# INSTRUCTIONS: 

      # fetch [index],       READ var at index in Data Array 
      # store [index],       STORE 32 BIT VAR AT index 
      # push n               PUSH 32 BIT VAR 
      # jmp (distance) addr  JUMP BY DISTANCE
      # jz (distance) addr   JUMP IF 0
      # halt 

      # WITH PUSH AND POP
            # add sub mul div mod lt gt le ge eq ne and or [generatl operations]
            # neg not [unary operations]

      # ptrc PRINT CHARACTER
      # prti PRINT INTEGER
      # prts PRINT STRING


class AssemblyCodeGenerator():

      # INITIALIZING THE TRACKING VARAIBLES
      def __init__(self):

            self.input_file  = open('OSyntaxAnalyzer.txt','r')
            self.outfile =  open('OCodeGenerator.txt','w')

            # FOR SIMULATING A BYTE MEMORY 
            self.code        = bytearray()      # AN ARRAY OF BYTES (TO STORE VARS BY BTYES)
            self.word_size   = 4 # 32 bits
            self.globals     = {}               # storing integers as name:value
            self.globals_n   = 0                # number of integers
            self.string_pool = {}               # storing strings  as name:value
            self.string_n    = 0                # number of strings

      # ERROR MESSAGE DISPLAYER
      def error(self,msg):
            print("%s" % (msg))
            exit(1)

      # INTEGER AS PACKED BINARY DATA AND RETURN BYTE ARRAY
      def int_to_bytes(self,val):
            return struct.pack("<i", val)

      # PACKED BINARY DATA BACK TO INTEGER AND RETURN BYTE ARRAY
      def bytes_to_int(self,bstr):
            return struct.unpack("<i", bstr)

      # ADD THE BYTES TO THE BYTE ARRAY
      def emit_byte(self,x):
            self.code.append(x)
      
      # ADD THE WORD TO BYTE ARRAY 
      def emit_word(self,x):
            s = self.int_to_bytes(x)
            for x in s:
                  self.code.append(x)

      # OVER WRITING THE BYTES
      def emit_word_at(self,at, n):
            self.code[at:at+self.word_size] = self.int_to_bytes(n)


      def hole(self):
            t = len(self.code)
            self.emit_word(0)
            return t
      
      # STORE AND FETCH INTEGERS
      def fetch_var_offset(self,name):
            n = self.globals.get(name, None)
            if n == None:
                  self.globals[name] = self.globals_n
                  n = self.globals_n
                  self.globals_n += 1
            return n
      
      # STORE AND FETCH STRINGS
      def fetch_string_offset(self,the_string):
            n = self.string_pool.get(the_string, None)
            if n == None:
                  self.string_pool[the_string] = self.string_n
                  n = self.string_n
                  self.string_n += 1
            return n
 
      def code_gen(self,x):
            if x == None: return
            elif x.node_type == ND_IDENT:
                  self.emit_byte(OP_FETCH)                  # FETCH
                  n = self.fetch_var_offset(x.value)        # 
                  self.emit_word(n)                         # [INDEX] 
            elif x.node_type == ND_INT:
                  self.emit_byte(OP_PUSH)                   # PUSH   
                  self.emit_word(x.value)                   # [INDEX]      
            elif x.node_type == ND_STR:
                  self.emit_byte(OP_PUSH)                   # PUSH
                  n = self.fetch_string_offset(x.value)     # 
                  self.emit_word(n)                         # [INDEX]
            elif x.node_type == ND_ASS:
                  n = self.fetch_var_offset(x.left.value)   # ASSIGN N
                  self.code_gen(x.right)                    # SOLVE RIGHT
                  self.emit_byte(OP_STORE)                  # STORE
                  self.emit_word(n)                         # N
            elif x.node_type == ND_IF:
                  self.code_gen(x.left)                     # expr
                  self.emit_byte(OP_JZ)                     # if false, jump
                  p1 = self.hole()                          # make room for jump dest
                  self.code_gen(x.right.left)               # if true statements
                  if (x.right.right != None):
                        self.emit_byte(OP_JMP)              # jump over else statements
                        p2 = self.hole()
                  self.emit_word_at(p1, len(self.code) - p1)
                  if (x.right.right != None):
                        self.code_gen(x.right.right)        # else statements
                        self.emit_word_at(p2, len(self.code) - p2)
            elif x.node_type == ND_WHILE:
                  p1 = len(self.code)
                  self.code_gen(x.left)
                  self.emit_byte(OP_JZ)
                  p2 = self.hole()
                  self.code_gen(x.right)
                  self.emit_byte(OP_JMP)                       # jump back to the top
                  self.emit_word(p1 - len(self.code))
                  self.emit_word_at(p2, len(self.code) - p2)
            elif x.node_type == ND_SEQ:                        
                  self.code_gen(x.left)
                  self.code_gen(x.right)
            elif x.node_type == ND_PRTC:                        # OP_PRTC
                  self.code_gen(x.left)
                  self.emit_byte(OP_PRTC)
            elif x.node_type == ND_PRTI:                        # OP_PRTI
                  self.code_gen(x.left)
                  self.emit_byte(OP_PRTI)
            elif x.node_type == ND_PRTS:                        # OP_PRTS  
                  self.code_gen(x.left)
                  self.emit_byte(OP_PRTS)
            elif x.node_type in OPERATORS:                      
                  self.code_gen(x.left)
                  self.code_gen(x.right)
                  self.emit_byte(OPERATORS[x.node_type])
            elif x.node_type in UNARY_OPERATORS:
                  self.code_gen(x.left)
                  self.emit_byte(UNARY_OPERATORS[x.node_type])
            else:
                  self.error("error in code generator - found %d, expecting operator" % (x.node_type))
 
      def code_finish(self):
            self.emit_byte(OP_HALT)

      def list_code(self):
            print("Datasize: %d Strings: %d" % (len(self.globals), len(self.string_pool)),file=self.outfile)
            for k in sorted(self.string_pool, key=self.string_pool.get):
                  print(k,file=self.outfile)
            pc = 0
            while pc < len(self.code):
                  print("%4d " % (pc), end='',file=self.outfile)
                  op = self.code[pc]
                  pc += 1
                  if op == OP_FETCH:
                        x = self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                        print("fetch [%d]" % (x),file=self.outfile);
                        pc += self.word_size
                  elif op == OP_STORE:
                        x = self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                        print("store [%d]" % (x),file=self.outfile);
                        pc += self.word_size
                  elif op == OP_PUSH:
                        x = self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                        print("push  %d" % (x),file=self.outfile);
                        pc += self.word_size
                  elif op == OP_ADD:   print("add",file=self.outfile)
                  elif op == OP_SUB:   print("sub",file=self.outfile)
                  elif op == OP_MUL:   print("mul",file=self.outfile)
                  elif op == OP_DIV:   print("div",file=self.outfile)
                  elif op == OP_MOD:   print("mod",file=self.outfile)
                  elif op == OP_LT:    print("lt",file=self.outfile)
                  elif op == OP_GT:    print("gt",file=self.outfile)
                  elif op == OP_LE:    print("le",file=self.outfile)
                  elif op == OP_GE:    print("ge",file=self.outfile)
                  elif op == OP_EQ:    print("eq",file=self.outfile)
                  elif op == OP_NE:    print("ne",file=self.outfile)
                  elif op == OP_AND:   print("and",file=self.outfile)
                  elif op == OP_OR:    print("or",file=self.outfile)
                  elif op == OP_NEG:   print("neg",file=self.outfile)
                  elif op == OP_NOT:   print("not",file=self.outfile)
                  elif op == OP_JMP:
                        x = self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                        print("jmp    (%d) %d" % (x, pc + x),file=self.outfile);
                        pc += self.word_size
                  elif op == OP_JZ:
                        x = self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                        print("jz     (%d) %d" % (x, pc + x),file=self.outfile);
                        pc += self.word_size
                  elif op == OP_PRTC:  print("prtc",file=self.outfile)
                  elif op == OP_PRTI:  print("prti",file=self.outfile)
                  elif op == OP_PRTS:  print("prts",file=self.outfile)
                  elif op == OP_HALT:  print("halt",file=self.outfile)
                  else: self.error("list_code: Unknown opcode %d", (op));
            

      def load_ast(self):
            line = self.input_file.readline()
            line_list = shlex.split(line, False, False)
            text = line_list[0]
            if text == ";":
                  return None
            node_type = SYMB_NODE[text]
            if len(line_list) > 1:
                  value = line_list[1]
                  if value.isdigit():
                        value = int(value)
                  return make_leaf(node_type, value)
            
            left = self.load_ast()
            right = self.load_ast()
            return make_node(node_type, left, right)
            

      def generate(self):
            ast = self.load_ast()
            self.code_gen(ast)
            self.code_finish()
            self.list_code()
            self.input_file.close()
            self.outfile.close()




if __name__=='__main__':
      codeGenerator = AssemblyCodeGenerator();
      codeGenerator.generate()
 
