import sys, struct
from constants import *


class VirtualMachineInterpreter():

      def __init__(self):
            self.input_file  = open('OCodeGenerator.txt','r')
            self.outfile =  open('output.txt','w')
            self.code        = bytearray()
            self.string_pool = []
            self.word_size   = 4

      def error(self,msg):
            print("%s" % (msg))
            exit(1)
 
      def int_to_bytes(self,val):
            return struct.pack("<i", val)
            
      def bytes_to_int(self,bstr):
            return struct.unpack("<i", bstr)
            
      def emit_byte(self,x):
            self.code.append(x)

      def emit_word(self,x):
            s = self.int_to_bytes(x)
            for x in s:
                  self.code.append(x)

      def run_vm(self):
            data_size = self.load_code()
            stack = [0 for i in range(data_size + 1)]
            pc = 0
            while True:
                  op = self.code[pc]
                  pc += 1
                  if op == OP_FETCH:
                        stack.append(stack[self.bytes_to_int(self.code[pc:pc+self.word_size])[0]]);
                        pc += self.word_size
                  elif op == OP_STORE:
                        stack[self.bytes_to_int(self.code[pc:pc+self.word_size])[0]] = stack.pop();
                        pc += self.word_size
                  elif op == OP_PUSH:
                        stack.append(self.bytes_to_int(self.code[pc:pc+self.word_size])[0]);
                        pc += self.word_size
                  elif op == OP_ADD:   stack[-2] += stack[-1]; stack.pop()
                  elif op == OP_SUB:   stack[-2] -= stack[-1]; stack.pop()
                  elif op == OP_MUL:   stack[-2] *= stack[-1]; stack.pop()
                  # use C like division semantics
                  elif op == OP_DIV:   stack[-2] = int(float(stack[-2]) / stack[-1]); stack.pop()
                  elif op == OP_MOD:   stack[-2] = int(float(stack[-2]) % stack[-1]); stack.pop()
                  elif op == OP_LT:    stack[-2] = stack[-2] <  stack[-1]; stack.pop()
                  elif op == OP_GT:    stack[-2] = stack[-2] >  stack[-1]; stack.pop()
                  elif op == OP_LE:    stack[-2] = stack[-2] <= stack[-1]; stack.pop()
                  elif op == OP_GE:    stack[-2] = stack[-2] >= stack[-1]; stack.pop()
                  elif op == OP_EQ:    stack[-2] = stack[-2] == stack[-1]; stack.pop()
                  elif op == OP_NE:    stack[-2] = stack[-2] != stack[-1]; stack.pop()
                  elif op == OP_AND:   stack[-2] = stack[-2] and stack[-1]; stack.pop()
                  elif op == OP_OR:    stack[-2] = stack[-2] or  stack[-1]; stack.pop()
                  elif op == OP_NEG:   stack[-1] = -stack[-1]
                  elif op == OP_NOT:   stack[-1] = not stack[-1]
                  elif op == OP_JMP:   pc += self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                  elif op == OP_JZ:
                        if stack.pop():
                              pc += self.word_size
                        else:
                              pc += self.bytes_to_int(self.code[pc:pc+self.word_size])[0]
                  elif op == OP_PRTC:  print("%c" % (stack[-1]), end='',file=self.outfile); stack.pop()
                  elif op == OP_PRTS:  print("%s" % (self.string_pool[stack[-1]]), end='',file=self.outfile); stack.pop()
                  elif op == OP_PRTI:  print("%d" % (stack[-1]), end='',file=self.outfile); stack.pop()
                  elif op == OP_HALT:  break
            self.input_file.close()
            self.outfile.close()

      def str_trans(self,srce):
            dest = ""
            i = 0
            while i < len(srce):
                  if srce[i] == '\\' and i + 1 < len(srce):
                        if srce[i + 1] == 'n':
                              dest += '\n'
                              i += 2
                        elif srce[i + 1] == '\\':
                              dest += '\\'
                              i += 2
                  else:
                        dest += srce[i]
                        i += 1
            return dest
            
      def load_code(self):
            line = self.input_file.readline()
            if len(line) == 0:
                  self.error("empty line")
            line_list = line.split()
            data_size = int(line_list[1])
            n_strings = int(line_list[3])
            for i in range(n_strings):
                  self.string_pool.append(self.str_trans(self.input_file.readline().strip('"\n')))
            while True:
                  line = self.input_file.readline()
                  if len(line) == 0: 
                        break
                  line_list = line.split()
                  offset = int(line_list[0])
                  instr  = line_list[1]
                  opcode = STR_OP.get(instr)
                  if opcode == None:
                        self.error("Unknown instruction %s at %d" % (instr, offset))
                  self.emit_byte(opcode)
                  if opcode in [OP_JMP, OP_JZ]:
                        p = int(line_list[3])
                        self.emit_word(p - (offset + 1))
                  elif opcode == OP_PUSH:
                        value = int(line_list[2])
                        self.emit_word(value)
                  elif opcode in [OP_FETCH, OP_STORE]:
                        value = int(line_list[2].strip('[]'))
                        self.emit_word(value)
            return data_size

if __name__ == '__main__':
      vmi = VirtualMachineInterpreter()
      vmi.run_vm()
