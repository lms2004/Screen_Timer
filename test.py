import time
import socket
import threading
from scapy.all import sniff, IP, TCP

class MonitoringFactory:
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


if __name__ == "__main__":
    monitoring_factory = MonitoringFactory("blog.csdn.net")
    monitor_thread = monitoring_factory.start_monitoring()

    # 主线程可以做其他事情，这里只是简单的等待监控线程运行
    while monitor_thread.is_alive():
        time.sleep(1)

