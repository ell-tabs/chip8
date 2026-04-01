# opcodes
import random

def OP_00E0(self): # clears screen matrix
    print('cleared screen!')
    for row in self.screen:
        for i in range(len(row)):
            row[i] = 0
    self.Program_Counter += 2

def OP_00EE(self):
    self.Program_Counter = self.Stack.pop()

def OP_1nnn(self, a):
    self.Program_Counter = a & 0xFFF

def OP_2nnn(self, op):
    val = op & 0xFFF
    self.Stack.append(self.Program_Counter + 2)
    self.Program_Counter = val

def OP_3xkk(self, x, op):
    val = op & 0xFF
    if self.V[x] == val:
        self.Program_Counter += 4
    else:
        self.Program_Counter += 2

def OP_4xkk(self, x, op):
    val = op & 0xFF
    if self.V[x] != val:
        self.Program_Counter += 4
    else:
        self.Program_Counter += 2

def OP_5xy0(self, x, y):
    if self.V[x] == self.V[y]:
        self.Program_Counter += 4
    else:
        self.Program_Counter += 2

def OP_6xkk(self, x, op):
    val = op & 0xFF
    self.V[x] = val
    self.Program_Counter += 2

def OP_7xkk(self, x, op):
    val = op & 0xFF
    self.V[x] = (self.V[x] + val) & 0xFF
    self.Program_Counter += 2

def OP_8xy0(self, b, c):
    self.V[b] = self.V[c]
    self.Program_Counter += 2

def OP_8xy1(self, b, c):
    self.V[b] = self.V[b] | self.V[c]
    self.Program_Counter += 2

def OP_8xy2(self, b, c):
    self.V[b] = self.V[b] & self.V[c]
    self.Program_Counter += 2

def OP_8xy3(self, b, c):
    self.V[b] = self.V[b] ^ self.V[c]
    self.Program_Counter += 2

def OP_8xy4(self, b, c):
    a = (self.V[b] & 0xFF) + (self.V[c] & 0xFF)

    if a > 255:
        self.V[0xF] = 1
    else:
        self.V[0xF] = 0

    self.V[b] = a & 0xFF
    self.Program_Counter += 2


def OP_8xy5(self, b, c):
    vx = self.V[b]
    vy = self.V[c]

    self.V[0xF] = 1 if vx >= vy else 0
    self.V[b] = (vx - vy) & 0xFF

    self.Program_Counter += 2

def OP_8xy6(self, b, c):
    bit = self.V[b] & 0x1
    if bit == 1:
        self.V[0xf] = 1
    else:
        self.V[0xf] = 0
    self.V[b] >>= 1  & 0xFF
    self.Program_Counter += 2

def OP_8xy7(self, b, c):
    vx = self.V[b]
    vy = self.V[c]

    # VF = 1 if no borrow
    self.V[0xF] = 1 if vy >= vx else 0

    # store result in Vx
    self.V[b] = (vy - vx) & 0xFF

    self.Program_Counter += 2

def OP_8xyE(self, b, c):
    msb = (self.V[b] >> 7) & 1
    self.V[0xF] = msb
    self.V[b] = (self.V[b] << 1) & 0xFF
    self.Program_Counter += 2

def OP_9xy0(self, x, y):
    if self.V[x] != self.V[y]:
        self.Program_Counter += 4
    else:
        self.Program_Counter += 2

def OP_Annn(self, op):
    self.Index = op & 0xFFF
    self.Program_Counter += 2
def OP_Bnnn(self, op):
    val = op & 0xFFF
    self.Program_Counter = (val + self.V[0])
def OP_Cxkk(self, x, op):
    self.V[x] = random.randint(0, 255) & (op & 0xFF)
    self.Program_Counter += 2
def OP_Dxyn(self, b, c, d):
    self.V[0xF] = 0
    for row in range(d):
        sprite_byte = self.memory[self.Index + row]
        for bit in range(8):
            x = (self.V[b] + bit) % 64
            y = (self.V[c] + row) % 32
            pixel_bit = (sprite_byte >> (7 - bit)) & 1

            if pixel_bit == 1:
                if self.screen[y][x] == 1:
                    self.V[0xF] = 1  # collision detected
                self.screen[y][x] ^= 1

    self.Program_Counter += 2
def OP_Ex9E(self, b):
    if self.keys[self.V[b]] == 1:
        self.Program_Counter += 4
    else:
         self.Program_Counter += 2
def OP_ExA1(self, b):
    if self.keys[self.V[b]] == 0:
        self.Program_Counter += 4
    else:
         self.Program_Counter += 2

def OP_Fx07(self, b):
    self.V[b] = self.DT
    self.Program_Counter += 2

def OP_Fx0A(self, b):

    key_pressed = False

    for i in range(16):
        if self.keys[i] == 1:
            self.V[b] = i
            key_pressed = True
            break

    if key_pressed == True:
        self.Program_Counter += 2

def OP_Fx15(self, b):
    self.DT = self.V[b]
    self.Program_Counter += 2

def OP_Fx18(self, b):
    self.ST = self.V[b]
    self.Program_Counter += 2

def OP_Fx1E(self, b):
    self.Index += self.V[b]
    self.Program_Counter += 2

def OP_Fx29(self, b):
    self.Index = self.font_addr[self.V[b]]
    self.Program_Counter += 2

def OP_Fx33(self, b):
    value = self.V[b]
    self.memory[self.Index]   = value // 100
    self.memory[self.Index+1] = (value // 10) % 10
    self.memory[self.Index+2] = value % 10
    self.Program_Counter += 2

def OP_Fx55(self, b):
    for i in range(b + 1):
        self.memory[self.Index + i] = self.V[i]
    self.Program_Counter += 2

def OP_Fx65(self, b):
    for i in range(b + 1):
        self.V[i] = self.memory[self.Index + i]
    self.Program_Counter += 2
