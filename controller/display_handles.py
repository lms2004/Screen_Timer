import tkinter as tk
from tkinter import ttk, StringVar, font

class WidgetFactory:
    def __init__(self, root, font, background_color, foreground_color):
        self.root = root
        self.font = font
        self.background_color = background_color
        self.foreground_color = foreground_color

    def create_label(self, textvariable):
        """创建Label控件"""
        lbl = ttk.Label(
            self.root, 
            textvariable=textvariable, 
            font=self.font, 
            foreground=self.foreground_color, 
            background=self.background_color
        )
        return lbl

    def create_spinbox(self, textvariable, from_, to, validatecommand):
        """创建Spinbox控件"""
        spinbox = tk.Spinbox(
            self.root,
            from_=from_,
            to=to,
            textvariable=textvariable,
            bg=self.background_color,
            fg=self.foreground_color,
            width=3,
            font=self.font,
            justify="center",
            relief="flat",
            validate="key",
            validatecommand=validatecommand
        )
        return spinbox

    def create_button(self, text, command):
        """创建Button控件"""
        button = tk.Button(
            self.root,
            text=text,
            command=command,
            font=self.font,
            bg=self.background_color,
            fg=self.foreground_color,
            relief="flat",
            width=10,
            padx=5,
            pady=5
        )
        return button

    def update_fonts(self, new_font_size):
        """更新所有控件的字体大小"""
        self.font.config(size=new_font_size)
        for widget in self.root.winfo_children():
            try:
                widget.config(font=self.font)
            except:
                pass
