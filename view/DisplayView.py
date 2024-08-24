import tkinter as tk
from tkinter import Menu, StringVar, font
from tkinter import ttk
from view.BaseView import BaseView

class DisplayView(BaseView):
    def __init__(self, root, config, timer):
        super().__init__(root, config)
        self.timer = timer  # 接收 Timer 实例

        self.create_menu()
        self.create_display()

    def create_menu(self):
        """创建菜单栏"""
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.timer.quit_all)

    def create_display(self):
        """创建主显示内容"""
        self.txt = StringVar()
        self.txt.set(self.config.read("TIMER", "initial_time"))

        # 设置初始字体大小
        self.fnt = font.Font(family="Helvetica", size=150, weight="bold")

        # 创建一个较大的Label来显示时间
        self.lbl = ttk.Label(self.root, textvariable=self.txt, font=self.fnt, foreground="white", background="black")
        self.lbl.place(relx=0.5, rely=0.4, anchor="center")  # 居中显示

        # 创建控制按钮
        self.create_controls()

        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.resize_widgets)

    def create_controls(self):
        """创建控制按钮和其他控件"""
        # 初始按钮字体设置
        self.btn_font = font.Font(family="Helvetica", size=20, weight="bold")

        # Start 按钮
        self.start_button = self.widget_factory.create_button("Start", self.timer.run_timer)
        self.start_button.config(font=self.btn_font)
        self.start_button.place(relx=0.3, rely=0.8, relwidth=0.15, relheight=0.1)  # 调整大小

        # Stop 按钮
        self.stop_button = self.widget_factory.create_button("Stop", self.timer.go_stop)
        self.stop_button.config(font=self.btn_font)
        self.stop_button.place(relx=0.5, rely=0.8, relwidth=0.15, relheight=0.1)

        # Reset 按钮
        self.reset_button = self.widget_factory.create_button("Reset", self.timer.reset)
        self.reset_button.config(font=self.btn_font)
        self.reset_button.place(relx=0.7, rely=0.8, relwidth=0.15, relheight=0.1)

    def resize_widgets(self, event):
        """根据窗口大小动态调整控件和字体大小"""
        # 调整字体大小
        new_font_size = max(int(event.width / 20), 20)
        self.fnt.config(size=new_font_size)
        self.btn_font.config(size=int(new_font_size / 7.5))

        # 动态调整按钮和标签大小
        self.lbl.place(relx=0.5, rely=0.4, anchor="center")
        self.start_button.place(relx=0.3, rely=0.8, relwidth=0.15, relheight=0.1)
        self.stop_button.place(relx=0.5, rely=0.8, relwidth=0.15, relheight=0.1)
        self.reset_button.place(relx=0.7, rely=0.8, relwidth=0.15, relheight=0.1)

    def update_display(self, text):
        """更新显示内容"""
        self.txt.set(text)
