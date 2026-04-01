from opcodes import *
from decode import * 
import time
import os
import pygame as pg
import numpy as np
import random
import sys
from pysinewave import SineWave
sinewave = SineWave(pitch = 20, pitch_per_second = 10)

class CPU:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16 # Registers V[0] - V[15]
        self.Stack = []
        self.Index = 0
        self.Program_Counter = 0x200
        self.DT = 0
        self.ST = 0

        self.screen = np.zeros((32, 64), dtype=np.uint8)
        self.screen[14][28] = 1 # draws dummy pixel to screen, gets removed one cycle later by CLS
        self.keys = [0] * 16
        self.char = {
    '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
    'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
    'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
    'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF
}

        self.input_state = {key: 0 for key in self.keys}
    # The fontset
        self.font_set = [	
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
	0x20, 0x60, 0x20, 0x20, 0x70, # 1
	0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
	0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
	0x90, 0x90, 0xF0, 0x10, 0x10, # 4
	0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
	0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
	0xF0, 0x10, 0x20, 0x40, 0x40, # 7
	0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
	0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
	0xF0, 0x90, 0xF0, 0x90, 0x90, # A
	0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
	0xF0, 0x80, 0x80, 0x80, 0xF0, # C
	0xE0, 0x90, 0x90, 0x90, 0xE0, # D
	0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
	0xF0, 0x80, 0xF0, 0x80, 0x80, # F
    ]
# python3 chip8.py ROMS/
    def LOAD_ROM(self): # loads the program into self.memory
        with open(sys.argv[1], 'rb') as a:
            file = a.read()
        for i in range(len(file)):
            self.memory[0x200 + i] = file[i]
        for i in range(80):
            self.memory[0x50 + i] = self.font_set[i]
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

    def decrement_timers(self):
        if self.DT > 1:
            self.DT -=1
        if self.ST > 1:
            sinewave.play()
            self.ST -= 1
        elif self.ST <= 1:
            sinewave.stop()
            

    def detect_input(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN and pg.key.name(event.key) in self.char:
                self.keys[self.char[pg.key.name(event.key)]] = 1
                print("event key down",pg.key.name(event.key))
                #if event.key in self.keys:
            if event.type == pg.KEYUP and pg.key.name(event.key) in self.char:
                self.keys[self.char[pg.key.name(event.key)]] = 0
                print("event key up",pg.key.name(event.key))
                #if event.key in self.keys:
                #    self.keys[event.key] = 0

last_frame_time = time.perf_counter()
cycle_delay = 1 / 500
frame_delay = 1 / 60

cpu = CPU()
cpu.LOAD_ROM()
pg.init()
window = pg.display.set_mode((640, 320))
INSTRUCTIONS_PER_SECOND = 500
FRAMES_PER_SECOND = 60

last_frame_time = time.perf_counter()
last_timer_time = time.perf_counter()

while True:
    start = time.perf_counter()

    cpu.detect_input()
    cpu.cycle()

    # Update timers at 60 Hz
    if time.perf_counter() - last_timer_time >= 1/60:
        cpu.decrement_timers()
        last_timer_time += 1/60

    # Draw screen at 60 FPS
    if time.perf_counter() - last_frame_time >= frame_delay:
        cpu.update_screen(window)
        last_frame_time += frame_delay

    # Sleep just enough to maintain instruction speed
    elapsed = time.perf_counter() - start
    time.sleep(max(0, cycle_delay - elapsed))
'''
python3 chip8.py ROMS/
'''