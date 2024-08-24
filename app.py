from tkinter import Tk, font, ttk, StringVar, Menu, Toplevel, Spinbox, Button
import pygame
import configparser
import os
import sys

from model.configreader import ConfigReader
from view.DisplayView import DisplayView
from controller.event_handlers import SoundFactory
from model.timer_model import Timer


root = Tk()

# 加载配置文件
config = ConfigReader("settings.ini")

# 加载报警声音
alarm_sound = SoundFactory.generate_sound("alert.wav")

# 创建Timer实例
timer = Timer(config, root, alarm_sound, None)

# 创建DisplayView实例，并将Timer实例传递给它
MainView = DisplayView(root, config, timer)

# 将DisplayView实例赋值给Timer实例中的display_view属性
timer.display_view = MainView

# 顶层框大小
root.geometry("300x100")

# 进入主循环
root.mainloop()
