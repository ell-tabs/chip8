from opcodes import *

def decode(memory, Program_Counter):
    
    pc = Program_Counter
    op = (memory[pc] << 8) | memory[pc + 1]

    a = (op & 0xF000) >> 12     # 1st 4 bits
    b = (op & 0xF00) >> 8       # 2nd 4 bits
    c = (op & 0xF0) >> 4        # 3rd 4 bits
    d = (op & 0xF)              # 4th 4 bits

    byte1 = (op & 0x00FF) >> 8  # first byte
    byte2 = op & 0xFF           # second byte

    if a == 0x0:
        if byte2 == 0xEE: # RETURN
            print("OP: 00EE")
            OP_00EE()
        if byte2 == 0xE0: # CLR
            print("OP: 00E0")
            OP_00E0()
        else: 
            print("invalid opcode") 
            exit()

    elif a == 1:
        print("1NNN")
        OP_1nnn()
    elif a == 2:
        OP_2nnn()
    elif a == 3:
        OP_3xkk()
    elif a == 4:
        OP_4xkk()
    elif a == 5:
        OP_5xy0()
    elif a == 6:
        OP_6xkk()
    elif a == 7:
        OP_7xkk()

    elif a == 8:
        b &= 0xF

        if b == 0:
            OP_8xy0
        elif b == 1:
            OP_8xy1()
        elif b == 2:
            OP_8xy2()
        elif b ==3:
            OP_8xy3()
        elif b == 4:
            OP_8xy4()
        elif b == 5:
            OP_8xy5()
        elif b == 6:
            OP_8xy6()
        elif b == 7:
            OP_8xy7()
        elif b == 0xE:
            OP_8xyE()

    elif a == 9:
        OP_9xy0()
    elif a == 0xA:
        OP_Annn()
    elif a == 0xB:
        OP_Bnnn()
    elif a == 0xC:
        OP_Cxkk()
    elif a == 0xD:
        OP_Dxyn()

    elif a == 0xE:
        b &= 0xF

        if b == 0xE:
            OP_Ex9E()
        elif b == 0x1:
            OP_ExA1()

        pass
    
    elif a == 0xF:
        pass