import sys
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b01100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR  = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
CALL = 0b01010000
RET = 0b00010001
INT = 0b01010010 
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001
JGE = 0b01011010
NOP = 0b00000000
HLT = 0b00000001 
LDI = 0b10000010
LD  = 0b10000011
ST  = 0b10000100
PUSH = 0b01000101
POP = 0b01000110
PRN = 0b01000111
PRA = 0b01001000
SP = 7
ALU = 'alu'

class CPU:
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.bt = {PRN: self.handle_prn,POP: self.handle_pop,PUSH: self.handle_push,LDI: self.handle_ldi,ADD: self.alu,
        MUL: self.alu,SUB: self.alu,DIV: self.alu,MOD: self.alu,INC: self.alu,DEC: self.alu,CMP: self.alu,AND: self.alu,
        OR: self.alu,NOT: self.alu,XOR: self.alu,SHL: self.alu,SHR: self.alu}
        self.reg[SP] = 0xf4
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, value):
        self.ram[address] = value
    def load(self, progname):
        address = 0
        with open('./examples/' + progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()  # lose whitespace
                if line == '':
                    continue
                val = int(line, 2) # LS-8 uses base 2!
                self.ram_write(address, val)
                address += 1

    def alu(self, op, reg_a = None, reg_b = None):
        """ALU operations."""
        if op == ADD:
            self.pc += 3
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.pc += 3
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.pc += 3
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == DIV:
            self.pc += 3
            self.reg[reg_a] = self.reg[reg_a] / self.reg[reg_b]
        elif op == MOD:
            self.pc += 3
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == INC:
            self.pc += 2
            self.reg[reg_a] += 1
        elif op == DEC:
            self.pc += 2
            self.reg[reg_b] -= 1
        elif op == CMP:
            self.pc += 3
            if self.reg[reg_a] < self.reg[reg_b]:
                self.reg[reg_a] = self.reg[reg_a]
        elif op == AND:
            self.pc += 3
            self.reg[reg_a] & self.reg[reg_b]
        elif op == NOT:
            self.pc += 2
            ~self.reg[reg_a]
        elif op == OR:
            self.pc += 3
            self.reg[reg_a] | self.reg[reg_b]
        elif op == XOR:
            self.pc += 3
            self.reg[reg_a] ^ self.reg[reg_b]
        elif op == SHL:
            self.pc += 3
            self.reg[reg_a] << self.reg[reg_b]
        elif op == SHR:
            self.pc += 3
            self.reg[reg_a] >> self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """Handy function to print out the CPU state. You might want to call this from run() if you need help debugging."""
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    
    #handlers
    def handle_ldi(self, op, register, value):
        self.reg[register] = value
        self.pc +=3
        return 
    def handle_prn(self, op, register, val = None):
        self.pc += 2
        return print(self.reg[register])
    def handle_push(self, op, value, val = None):
        self.reg[SP] -= 1
        reg_val = self.reg[value]
        self.ram[self.reg[SP]] = reg_val
        self.pc += 2
        return 
    def handle_pop(self, op, register, val = None):
        val = self.ram[self.reg[SP]]
        self.reg[register] = val
        self.reg[SP] +=1
        self.pc += 2
        return 

    def run(self):
        """Run the CPU."""
        halted, self.pc = False, 0
        while not halted:
            IR = self.ram[self.pc]
            if IR == HLT:
                halted = True
                sys.exit(1)
            elif IR in self.bt:
                self.bt[IR](IR, self.ram[self.pc+1], self.ram[self.pc+2])
            else: 
                print('unsupported instruction!')
