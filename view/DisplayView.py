import tkinter as tk
from tkinter import Menu, StringVar, font
from tkinter import ttk
from view.BaseView import BaseView

class DisplayView(BaseView):
    def __init__(self, root, config, timer):
        super().__init__(root, config)
        self.timer = timer  # 接收 Timer 实例

        # 从配置文件中读取参数
        self.font_family = self.config.read("DISPLAY", "font_family")
        self.font_size = int(self.config.read("DISPLAY", "font_size"))
        self.font_weight = self.config.read("DISPLAY", "font_weight")
        self.foreground_color = self.config.read("DISPLAY", "foreground_color")
        self.background_color = self.config.read("DISPLAY", "background_color")
        self.btn_font_size = int(self.config.read("DISPLAY", "button_font_size"))

        # 读取布局参数
        self.lbl_relx = float(self.config.read("LAYOUT", "lbl_relx"))
        self.lbl_rely = float(self.config.read("LAYOUT", "lbl_rely"))
        self.start_btn_relx = float(self.config.read("LAYOUT", "start_btn_relx"))
        self.stop_btn_relx = float(self.config.read("LAYOUT", "stop_btn_relx"))
        self.reset_btn_relx = float(self.config.read("LAYOUT", "reset_btn_relx"))
        self.btn_rely = float(self.config.read("LAYOUT", "btn_rely"))
        self.btn_relwidth = float(self.config.read("LAYOUT", "btn_relwidth"))
        self.btn_relheight = float(self.config.read("LAYOUT", "btn_relheight"))

        # 读取窗口调整因子
        self.font_resize_factor = float(self.config.read("LAYOUT", "font_resize_factor"))
        self.min_font_size = int(self.config.read("LAYOUT", "min_font_size"))

        self.create_menu()
        self.create_display()

    def create_menu(self):
        """创建菜单栏"""
        
        # 创建主菜单栏并添加到根窗口
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # 创建 'File' 菜单并添加选项
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # 添加菜单项并绑定功能
        file_menu.add_command(label="Start/Stop", accelerator="F1", command=self.timer.go_stop)
        file_menu.add_command(label="Reset", accelerator="F2", command=self.timer.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+X", command=self.timer.quit_all)



    def create_display(self):
        """创建主显示内容"""
        self.txt = StringVar()
        minutes = int(self.config.read("TIMER", "minutes"))
        seconds = int(self.config.read("TIMER", "seconds"))
        initial_time = f"{minutes:02}:{seconds:02}"  # 格式化为 MM:SS
        self.txt.set(initial_time)

        # 设置初始字体大小
        self.fnt = font.Font(family=self.font_family, size=self.font_size, weight=self.font_weight)

        # 创建一个较大的Label来显示时间
        self.lbl = ttk.Label(self.root, textvariable=self.txt, font=self.fnt, foreground=self.foreground_color, background=self.background_color)
        self.lbl.place(relx=self.lbl_relx, rely=self.lbl_rely, anchor="center")  # 使用配置中的布局参数
        
        # 创建控制按钮
        self.create_controls()

        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.resize_widgets)

    def create_controls(self):
        """创建控制按钮和其他控件"""
        # 初始按钮字体设置
        self.btn_font = font.Font(family=self.font_family, size=self.btn_font_size, weight=self.font_weight)

        # Start 按钮
        self.start_button = self.widget_factory.create_button("Start", self.timer.run_timer)
        self.start_button.config(font=self.btn_font)
        self.start_button.place(relx=self.start_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)

        # Stop 按钮
        self.stop_button = self.widget_factory.create_button("Stop", self.timer.go_stop)
        self.stop_button.config(font=self.btn_font)
        self.stop_button.place(relx=self.stop_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)

        # Reset 按钮
        self.reset_button = self.widget_factory.create_button("Reset", self.timer.reset)
        self.reset_button.config(font=self.btn_font)
        self.reset_button.place(relx=self.reset_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)

    def resize_widgets(self, event):
        """根据窗口大小动态调整控件和字体大小"""
        # 调整字体大小
        new_font_size = max(int(event.width / self.font_resize_factor), self.min_font_size)
        self.fnt.config(size=new_font_size)
        self.btn_font.config(size=int(new_font_size / 7.5))

        # 动态调整按钮和标签大小
        self.lbl.place(relx=self.lbl_relx, rely=self.lbl_rely, anchor="center")
        self.start_button.place(relx=self.start_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)
        self.stop_button.place(relx=self.stop_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)
        self.reset_button.place(relx=self.reset_btn_relx, rely=self.btn_rely, relwidth=self.btn_relwidth, relheight=self.btn_relheight)

    def update_display(self, text):
        """更新显示内容"""
        self.txt.set(text)
