from opcodes import *
from decode import * 
import time
import os
import pygame as pg
import numpy as np
import random
import sys

class CPU:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16 # Registers V[0] - V[15]
        self.Stack = []
        self.Index = 0
        self.Program_Counter = 0x200

        self.screen = np.zeros((32, 64), dtype=np.uint8)
        self.screen[14][28] = 1 # draws dummy pixel to screen, gets removed one cycle later by CLS


# python3 chip8.py ROMS/
    def LOAD_ROM(self): # loads the program into self.memory
        with open(sys.argv[1], 'rb') as a:
            file = a.read()
        for i in range(len(file)):
            self.memory[0x200 + i] = file[i]
        print(self.memory[:128])

    def update_screen(self, window): # updates the pixels on the screen
        colors = np.array([[120, 152, 57], [74, 88, 46]])

        surface_array = colors[self.screen].swapaxes(0, 1)
        surface = pg.surfarray.make_surface(surface_array)
        surface = pg.transform.scale(surface, (self.screen.shape[1]*10, self.screen.shape[0]*10))

        window.blit(surface, (0,0))
        pg.display.flip()


    def cycle(self): # completes one cpu instruction

        decode(self, self.memory, self.Program_Counter) # decodes and executes the opcode

        for i, val in enumerate(self.V): # prints V[0] - V[F]
            print(f"V[{i}]: {val}")

        # prints the values of the program counter, stack pointer, and index
        print("PC:",hex(self.Program_Counter))
        print("I:",hex(self.Index))

    def decrement_timers():
        pass

cpu = CPU()
cpu.LOAD_ROM()
pg.init()
window = pg.display.set_mode((640, 320))

while True:
    cpu.update_screen(window)
    cpu.cycle()
    time.sleep(0.1)
    