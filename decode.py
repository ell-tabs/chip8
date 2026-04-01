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
        b &= 0xF

        if b == 0:
            OP_8xy0(self)
        elif b == 1:
            OP_8xy1(self)
        elif b == 2:
            OP_8xy2(self)
        elif b ==3:
            OP_8xy3(self)
        elif b == 4:
            OP_8xy4(self)
        elif b == 5:
            OP_8xy5(self)
        elif b == 6:
            OP_8xy6(self)
        elif b == 7:
            OP_8xy7(self)
        elif b == 0xE:
            OP_8xyE(self)

    elif a == 9:
        OP_9xy0(self, b, c)
    elif a == 0xA:
        OP_Annn(self, op)
    elif a == 0xB:
        OP_Bnnn()
    elif a == 0xC:
        OP_Cxkk(self, b, op)
    elif a == 0xD:
        OP_Dxyn(self, b, c, d)

    elif a == 0xE:
        b &= 0xF

        if b == 0xE:
            OP_Ex9E(self)
        elif b == 0x1:
            OP_ExA1(self)

        pass
    
    elif a == 0xF:
        if op & 0xFF == 0x1E:
            OP_Fx1E(self, b)
        pass

    return byte1,byte2