from opcodes import *

def decode(self, memory, Program_Counter):
    
    pc = Program_Counter
    op = (memory[pc] << 8) | memory[pc + 1]

    a = (op & 0xF000) >> 12     # 1st 4 bits
    b = (op & 0xF00) >> 8       # 2nd 4 bits
    c = (op & 0xF0) >> 4        # 3rd 4 bits
    d = (op & 0xF)              # 4th 4 bits

    byte1 = op >> 8             # first byte
    byte2 = op & 0xFF           # second byte
    print(hex(op))

    if a == 0x0:
        if byte2 == 0xE0: # RETURN
            OP_00E0(self)
        elif byte2 == 0xEE: # CLR
            OP_00EE(self)
        elif op == 0x0000: 
            print("invalid opcode!:",hex(byte1+byte2))
            exit()

    elif a == 1:
        OP_1nnn(self, op)
    elif a == 2:
        OP_2nnn(self, op)
    elif a == 3:
        OP_3xkk(self, b, op)
    elif a == 4:
        OP_4xkk(self, b, op)
    elif a == 5:
        OP_5xy0(self, b, c)
    elif a == 6:
        OP_6xkk(self, b, op)
    elif a == 7:
        OP_7xkk(self, b, op)

    elif a == 8:

        if d == 0:
            OP_8xy0(self, b, c)
        elif d == 1:
            OP_8xy1(self, b, c)
        elif d == 2:
            OP_8xy2(self, b, c)
        elif d == 3:
            OP_8xy3(self, b, c)
        elif d == 4:
            OP_8xy4(self, b, c)
        elif d == 5:
            OP_8xy5(self, b, c)
        elif d == 6:
            OP_8xy6(self, b, c)
        elif d == 7:
            OP_8xy7(self, b, c)
        elif d == 0xE:
            OP_8xyE(self, b, c)

    elif a == 9:
        OP_9xy0(self, b, c)
    elif a == 0xA:
        OP_Annn(self, op)
    elif a == 0xB:
        OP_Bnnn(self, op)
    elif a == 0xC:
        OP_Cxkk(self, b, op)
    elif a == 0xD:
        OP_Dxyn(self, b, c, d)

    elif a == 0xE:

        if d == 0xE:
            OP_Ex9E(self, b)
        elif d == 0x1:
            OP_ExA1(self, b)
        pass
    
    elif a == 0xF:
        if op & 0xFF == 0x1E:
            OP_Fx1E(self, b)
        elif op & 0xFF == 0x07:
            OP_Fx07(self, b)
        elif op & 0xFF == 0x0A:
            OP_Fx0A(self, b)
        elif op & 0xFF == 0x15:
            OP_Fx15(self, b)
        elif op & 0xFF == 0x18:
            OP_Fx18(self, b)
        elif op & 0xFF == 0x29:
            OP_Fx29(self, b)
        elif op & 0xFF == 0x33:
            OP_Fx33(self, b)
        elif op & 0xFF == 0x55:
            OP_Fx55(self, b)
        elif op & 0xFF == 0x65:
            OP_Fx65(self, b)

    return byte1,byte2