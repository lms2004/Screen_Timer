import os
import pygame
import tkinter as tk
from tkinter import ttk, StringVar, font
import psutil
import socket
import threading
from scapy.all import sniff, IP, TCP

# SoundFactory 使用示例
# 初始化并生成一个音效对象
# sound = SoundFactory.generate_sound('alert.wav')
# sound.play()

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


# ProcessMonitorFactory 使用示例
# 检查是否有名为 'python' 的进程在运行
# is_running = ProcessMonitorFactory.is_process_running('python')
# print(f"Is 'python' running? {is_running}")

class ProcessMonitorFactory:
    @staticmethod
    def is_process_running(process_name):
        # 遍历所有运行中的进程
        for proc in psutil.process_iter(['name']):
            try:
                # 检查进程名称是否包含指定的名称
                if proc.info['name'] and process_name in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 如果进程已经终止或无法访问，继续检查下一个进程
                continue
        return False


# WebsiteMonitoringFactory 使用示例
# 监控对 'blog.csdn.net' 的 TCP 连接
# monitoring_factory = WebsiteMonitoringFactory("blog.csdn.net")
# monitor_thread = monitoring_factory.start_monitoring()

class WebsiteMonitoringFactory:
    def __init__(self, target_domain):
        self.target_domain = target_domain
        self.target_ips = self.resolve_domain(target_domain)
        self.detected = False
        self.monitor_thread = None

    def resolve_domain(self, domain):
        try:
            ip_addresses = socket.gethostbyname_ex(domain)[2]  # 获取所有 IP 地址
            print(f"Resolved IP addresses for {domain}: {ip_addresses}")
            return set(ip_addresses)
        except socket.gaierror:
            print(f"Could not resolve the IP addresses for {domain}")
            return set()

    def process_packet(self, packet):
        if packet.haslayer(IP) and packet.haslayer(TCP):
            dest_ip = packet[IP].dst
            if dest_ip in self.target_ips and packet[TCP].flags == 'S':  # 检查是否是 TCP SYN 包
                print(f"TCP connection attempt detected to {dest_ip}.")
                self.detected = True  # 记录检测到的访问

    def monitor_website(self):
        while True:
            if not self.target_ips:
                print("No target IP addresses available. Exiting...")
                break

            # 捕获数据包并处理，监控 TCP SYN 包来检测连接建立
            sniff(prn=self.process_packet, store=False, timeout=1, filter="tcp")  # 只捕获 TCP 数据包
            
            # 检查是否检测到目标网站访问
            if self.detected:
                print(f"TCP connection to {self.target_domain} detected. Pausing for a short period...")
                self.detected = False  # 重置检测状态
                print("重新开始检测")

    def start_monitoring(self):
        self.monitor_thread = threading.Thread(target=self.monitor_website)
        self.monitor_thread.daemon = True  # 设置为守护线程，主程序退出时自动终止
        self.monitor_thread.start()
        return self.monitor_thread
