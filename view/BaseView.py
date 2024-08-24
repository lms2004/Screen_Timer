import tkinter as tk
from tkinter import StringVar, font

from controller.display_handles import WidgetFactory

class BaseView:
    def __init__(self, root, config):
        self.root = root
        self.config = config

        # 从配置文件中获取参数
        self.font_family = config.read("DISPLAY", "font_family")
        self.font_size = int(config.read("DISPLAY", "font_size"))
        self.font_weight = config.read("DISPLAY", "font_weight")
        self.foreground_color = config.read("DISPLAY", "foreground_color")
        self.background_color = config.read("DISPLAY", "background_color")
        
        # 注册验证函数
        self.spinput = self.root.register(self.validate_numbers)

        # 初始化字体和工厂
        self.txt = StringVar()
        self.fnt = font.Font(family=self.font_family, size=self.font_size, weight=self.font_weight)

        # 使用工厂创建控件
        self.widget_factory = WidgetFactory(self.root, self.fnt, self.background_color, self.foreground_color)

    def validate_numbers(self, input_value):
        """
        验证输入是否为数字。
        :param input_value: 用户输入的值
        :return: True 如果输入值是数字或空值, 否则返回 False
        """
        if input_value.isdigit() or input_value == "":
            return True
        else:
            return False
        

    def get_font(self):
        """
        获取配置的字体对象。
        :return: tkinter.font.Font 对象
        """
        return font.Font(family=self.font_family, size=self.font_size, weight=self.font_weight)
