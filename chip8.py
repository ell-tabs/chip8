from opcodes import *
from decode import * 
import time
import os
import pygame as pg
import numpy as np
import random
import sys
from pysinewave import SineWave
sinewave = SineWave(pitch = 20)

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
        self.keys = [0] * 16
        self.char = {
    '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
    'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
    'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
    'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF
}
        self.rev_char = {
    '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
    'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
    'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
    'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF
}
        self.font_addr = {
    0x0: 0x50,
    0x1: 0x55,
    0x2: 0x5A,
    0x3: 0x5F,
    0x4: 0x64,
    0x5: 0x69,
    0x6: 0x6E,
    0x7: 0x73,
    0x8: 0x78,
    0x9: 0x7D,
    0xA: 0x82,
    0xB: 0x87,
    0xC: 0x8C,
    0xD: 0x91,
    0xE: 0x96,
    0xF: 0x9B,
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

        #for i, val in enumerate(self.V): # prints V[0] - V[F]
        #    print(f"V[{i}]: {val}")

        # prints the values of the program counter, stack pointer, and index
        print("PC:",hex(self.Program_Counter))
        print("I:",hex(self.Index))

    def decrement_timers(self):
        # Decrement DT if it's above 0
        if self.DT > 0:
            self.DT -= 1

        # Decrement ST if it's above 0
        if self.ST > 0:
            sinewave.play()
            self.ST -= 1
        else:
            sinewave.stop()
            

    def detect_input(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN and pg.key.name(event.key) in self.char:
                self.keys[self.char[pg.key.name(event.key)]] = 1
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                exit()
                #if event.key in self.keys:
            if event.type == pg.KEYUP and pg.key.name(event.key) in self.char:
                self.keys[self.char[pg.key.name(event.key)]] = 0
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
CPU_HZ = 500
TIMER_HZ = 60
FRAME_HZ = 60

cycle_delay = 1 / CPU_HZ
timer_delay = 1 / TIMER_HZ
frame_delay = 1 / FRAME_HZ

last_timer_time = time.perf_counter()
last_frame_time = time.perf_counter()

while True:
    start = time.perf_counter()

    # Run one CPU instruction
    cpu.detect_input()
    cpu.cycle()

    # Timers at 60 Hz
    now = time.perf_counter()
    if now - last_timer_time >= timer_delay:
        ticks = int((now - last_timer_time) / timer_delay)
        for _ in range(ticks):
            cpu.decrement_timers()
        last_timer_time += ticks * timer_delay

    print(f"DT: {cpu.DT}, ST: {cpu.ST}")

    # Draw at 60 FPS
    if now - last_frame_time >= frame_delay:
        cpu.update_screen(window)
        last_frame_time += frame_delay

    # Sleep to maintain CPU speed
    elapsed = time.perf_counter() - start
    time.sleep(max(0, cycle_delay - elapsed))

'''
python3 chip8.py ROMS/
'''
