# coding=utf-8

import requests
import re
import threading
import queue

from lib.header_generator import get_headers

# 暂时还没找到好用的免费代理IP站点，时过境迁...

class GetProxyIp(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue

    def run(self):
        while not self.work_queue.empty():
            ip = self.work_queue.get()
            check_ip_valid(ip)

def get_proxy_ips():
    url = "http://www.89ip.cn/tqdl.html?api=1&num=10&port=&address=&isp="
    response = requests.get(url=url, headers=get_headers(), timeout=10, verify=False)
    # 粗糙的正则，获取ip+port足矣
    pattern = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}')
    ip_list = re.findall(pattern, response.text)
    print(ip_list)
    return ip_list

def check_ip_valid(ip):
    url = "http://202020.ip138.com/"
    proxy = dict()
    proxy["http"] = ip
    try:
        print(proxy)
        r = requests.get(url=url, proxies=proxy, headers=get_headers(), timeout=5, verify=False)
        new_ip = re.findall(r'\[(.*?)\]', r.text)[0]
        if new_ip == ip:
            print('[*] Successful ! The IP is available ! ')
            print(proxy)
    except Exception as e:
        pass

def main():
    threads = []
    thread_count = 30
    work_queue = queue.Queue()

    ip_list = get_proxy_ips()
    for ip in ip_list:
        work_queue.put(ip)

    for i in range(thread_count):
        t = GetProxyIp(work_queue)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()