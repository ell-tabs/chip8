# opcodes

def OP_00E0(self): # clears screen matrix
    print('cleared screen!')
    for row in self.screen:
        for i in range(len(row)):
            row[i] = 0
    self.Program_Counter += 2

def OP_00EE(self):
    print('returned from subroutine!')
    self.Program_Counter += 2

def OP_1nnn(self, a):
    self.Program_Counter = a & 0xFFF

def OP_2nnn(self):
    pass

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

def OP_8xy0():
    pass
def OP_8xy1():
    pass
def OP_8xy2():
    pass
def OP_8xy3():
    pass
def OP_8xy4():
    pass
def OP_8xy5():
    pass
def OP_8xy6():
    pass
def OP_8xy7():
    pass
def OP_8xyE():
    pass

def OP_9xy0(self, x, y):
    if self.V[x] != self.V[y]:
        self.Program_Counter += 4
    else:
        self.Program_Counter += 2

def OP_Annn(self, op):
    self.Index = op & 0xFFF
    self.Program_Counter += 2
def OP_Bnnn():
    pass
def OP_Cxkk():
    pass
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
def OP_Ex9E():
    pass
def OP_ExA1():
    pass

def OP_Fx07():
    pass
def OP_Fx0A():
    pass
def OP_Fx15():
    pass
def OP_Fx18():
    pass
def OP_Fx1E():
    pass
def OP_Fx29():
    pass
def OP_Fx33():
    pass
def OP_Fx55():
    pass
def OP_Fx65():
    pass