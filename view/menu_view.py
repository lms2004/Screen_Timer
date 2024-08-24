import tkinter as tk
from tkinter import Menu, StringVar, font

from view.BaseView import BaseView
from controller.event_handlers import WidgetFactory


class MenuView(BaseView):
    def __init__(self, root, config, timer):
        super().__init__(root, config)
        self.timer = timer
        self.create_menu()

    def create_menu(self):
        """创建菜单并绑定功能"""
        # 创建顶级菜单
        self.menu_pop = Menu(self.root)
        self.menu = Menu(self.menu_pop, tearoff=0)
        self.menu.config(bg="black", fg="white", relief="raised")
        
        # 添加菜单项并绑定功能
        self.menu.add_command(label="Start/Stop", accelerator="F1", command=self.timer.go_stop)
        #   self.menu.add_command(label="Reset", accelerator="F2", command=self.timer.reset)
        #   self.menu.add_separator()
        #   self.menu.add_command(label="Settings", command=self.open_settings)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", accelerator="X", command=self.quit_all)
        self.menu_pop.add_cascade(label="File", menu=self.menu)