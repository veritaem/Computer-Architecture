import sys
ADD, SUB, MUL, DIV, MOD = 0b10100000, 0b10100001, 0b10100010, 0b10100011, 0b10100100 
INC, DEC, CMP = 0b01100101, 0b01100110, 0b10100111 
AND, NOT, OR, XOR = 0b10101000, 0b01101001, 0b10101010, 0b10101011
SHL, SHR = 0b10101100, 0b10101101
CALL, RET, INT, IRET = 0b01010000, 0b00010001, 0b01010010, 0b00010011
JMP, JEQ, JNE, JGT, JLT, JLE, JGE = 0b01010100, 0b01010101, 0b01010110, 0b01010111, 0b01011000, 0b01011001, 0b01011010
NOP, HLT = 0b00000000, 0b00000001 
LDI, LD, ST, ADDI = 0b10000010, 0b10000011, 0b10000100, 0b11001111
PUSH, POP, PRN, PRA = 0b01000101, 0b01000110, 0b01000111, 0b01001000
SP = 7

class CPU:
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.fl = 0b00000000
        self.pc = 0
        self.bt = {PRN:self.handle_prn, POP:self.handle_pop, PUSH:self.handle_push, LDI:self.handle_ldi, ADD:self.alu,
        MUL:self.alu, SUB:self.alu, DIV:self.alu, MOD:self.alu, INC:self.alu, DEC:self.alu, CMP:self.alu, AND:self.alu,
        OR:self.alu, NOT:self.alu, XOR:self.alu, SHL:self.alu, SHR:self.alu, CALL:self.call, RET:self.ret, JMP:self.handle_jmp,
        JEQ:self.handle_jeq, JNE:self.handle_jne, ADDI:self.handle_addi}
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

    def alu(self, op, reg_a = None, reg_b = None, v = None):
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
            v = self.reg[reg_a] - self.reg[reg_b]
            if v > 0:
                self.fl = 0b00000010
            elif v == 0:
                self.fl = 0b00000001
            else:
                self.fl = 0b00000100
            
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
    
    '''handlers'''
    def handle_ldi(self, op, register, value, v = None):
        self.reg[register] = value
        self.pc +=3
        return 
    def handle_prn(self, op, register, val = None, v = None):
        self.pc += 2
        return print(self.reg[register])
    def handle_push(self, op, value, val = None, v = None):
        self.reg[SP] -= 1
        reg_val = self.reg[value]
        self.ram[self.reg[SP]] = reg_val
        self.pc += 2
        return 
    def handle_pop(self, op, register, val = None, v = None):
        val = self.ram[self.reg[SP]]
        self.reg[register] = val
        self.reg[SP] +=1
        self.pc += 2
        return 
    def handle_jmp(self, op, plus_one, val = None, v = None):
        reg_num = plus_one
        self.pc = self.reg[reg_num]
    def handle_jeq(self, op, plus_one, val = None, v = None):
        if self.fl == 0b00000001:
            reg_num = plus_one
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
    def handle_jne(self, op, plus_one,  val = None, v = None):
        if self.fl == 0b00000010:
            reg_num = plus_one
            self.pc = self.reg[reg_num]
        elif self.fl == 0b00000100:
            reg_num = plus_one
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
    def handle_addi(self, op, dest, register, val):
        self.reg[dest] = self.reg[register] + val
    def ret(self, op, register, value, v = None):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] +=1 
    def call(self, op, register, value, v = None):
        ret_add = self.pc +2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = ret_add
        reg_num = self.ram[self.pc+1]
        self.pc = self.reg[reg_num]

    def run(self):
        """Run the CPU."""
        halted, self.pc = False, 0
        while not halted:
            IR = self.ram[self.pc]
            if IR == HLT:
                halted = True
                sys.exit(1)
            elif IR in self.bt:
                self.bt[IR](IR, self.ram[self.pc+1], self.ram[self.pc+2], self.ram[self.pc+3])
            else: 
                print(f'unsupported instruction! {bin(IR)}')
                sys.exit(['error handling instruction'])
