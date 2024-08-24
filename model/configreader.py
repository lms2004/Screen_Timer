import configparser
import os

class ConfigReader:
    def __init__(self, filename):
        self.parser = configparser.ConfigParser()
        config_dir = "./config"
        self.filename = os.path.join(os.path.abspath(config_dir), filename)  # 确保文件路径正确
        
        # 使用指定编码读取配置文件
        with open(self.filename, 'r', encoding='utf-8') as config_file:
            self.parser.read_file(config_file)

    def read(self, section, key):
        return self.parser.get(section, key)

    def write(self, section, key, value):
        # 修改配置内容
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, key, value)
        
        # 使用指定编码将新的配置内容写入文件
        with open(self.filename, "w", encoding='utf-8') as new_config:
            self.parser.write(new_config)
