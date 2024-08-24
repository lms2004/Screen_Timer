import os
import pygame
import tkinter as tk
from tkinter import ttk, StringVar, font

class SoundFactory:
    initialized = False  # 类变量，用于跟踪是否已经初始化过

    @staticmethod
    def initialize_mixer(frequency=44100, size=-16, channels=2, buffer=2048, volume=10.0):
        pygame.mixer.pre_init(frequency, size, channels, buffer)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)
        SoundFactory.initialized = True  # 标记为已初始化

    @staticmethod
    def generate_sound(filename):
        if not SoundFactory.initialized:
            SoundFactory.initialize_mixer()  # 自动初始化

        sound_dir = "./assets"
        return pygame.mixer.Sound(os.path.join(os.path.abspath(sound_dir), filename))

