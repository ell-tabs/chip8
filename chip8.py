from opcodes import *
from decode import * 
import time
import os

class CPU:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16 # Registers V[0] - V[15]
        self.Stack_Pointer = 0
        self.Index = 0
        self.Program_Counter = 0

        self.screen = [[0] * 64 for _ in range(32)]

        self.program = [00, 0xE0, 00, 0xEE, 0x12, 34]

    def LOAD_ROM(self):
        for i in range(len(self.program)):
            self.memory[i] = self.program[i]

    def update_screen(self):
        pass


    def cycle(self):
        decode(self.memory, self.Program_Counter)
        self.Program_Counter += 2

    def decrement_timers():
        pass

cpu = CPU()

while True:
    os.system("clear")
    cpu.LOAD_ROM()
    cpu.cycle()
    cpu.update_screen()
    time.sleep(0.5)
    