# coding=utf-8

import urllib3
urllib3.disable_warnings()

import sqlite3
import re
from bs4 import BeautifulSoup as BS
import concurrent.futures

from lib.sender import send
from lib.logger import logger

class FofaCmsFinger:
    def __init__(self, url, thread_count=30):
        self.url = url
        self.finger = []
        self.re_title = re.compile(r'title="(.*)"')
        self.re_header = re.compile(r'header="(.*)"')
        self.re_body = re.compile(r'body="(.*)"')
        self.re_bracket = re.compile(r'\((.*)\)')
        self.thread_count = thread_count
        self.title = ""
        self.body = ""
        self.header = ""

    def run(self):
        if self.thread():
            result = ""
            for i in self.finger:
                result += i + ", "
            print("[+]Fofa banner info:", result)
            logger.info("fofa banner info [" + result + "]")
        else:
            print("[-]Failed to access URL.")
            logger.error("failed to access url")

    def load_db_data(self, id):
        with sqlite3.connect('./fingerprint/fofa_cms_finger.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT name, keys FROM `fofa` WHERE id=\'{}\''.format(id))
            for row in result:
                return row[0], row[1]

    def count(self):
        with sqlite3.connect('./fingerprint/fofa_cms_finger.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute('SELECT COUNT(id) FROM `fofa`')
            for row in result:
                return row[0]

    def check_rule(self, key):
        if 'title="' in key:
            if re.findall(self.re_title, key)[0].lower() in self.title.lower():
                return True
        elif 'body="' in key:
            if re.findall(self.re_body, key)[0] in self.body:
                return True
        else:
            if re.findall(self.re_header, key)[0] in self.header:
                return True

    def match(self, id):
        """取出数据库的key进行匹配"""
        name, key = self.load_db_data(id)
        # 满足一个条件即可的情况
        if '||' in key and '&&' not in key and '(' not in key:
            for rule in key.split('||'):
                if self.check_rule(rule):
                    self.finger.append(name)
                    # print '%s[+] %s   %s%s' % (G, self.target, name, W)
                    break
        # 只有一个条件的情况
        elif '||' not in key and '&&' not in key and '(' not in key:
            if self.check_rule(key):
                self.finger.append(name)
                # print '%s[+] %s   %s%s' % (G, self.target, name, W)
        # 需要同时满足条件的情况
        elif '&&' in key and '||' not in key and '(' not in key:
            num = 0
            for rule in key.split('&&'):
                if self.check_rule(rule):
                    num += 1
            if num == len(key.split('&&')):
                self.finger.append(name)
                # print '%s[+] %s   %s%s' % (G, self.target, name, W)
        else:
            # 与条件下存在并条件: 1||2||(3&&4)
            if '&&' in re.findall(self.re_bracket, key)[0]:
                for rule in key.split('||'):
                    if '&&' in rule:
                        num = 0
                        for _rule in rule.split('&&'):
                            if self.check_rule(_rule):
                                num += 1
                        if num == len(rule.split('&&')):
                            self.finger.append(name)
                            # print '%s[+] %s   %s%s' % (G, self.target, name, W)
                            break
                    else:
                        if self.check_rule(rule):
                            self.finger.append(name)
                            # print '%s[+] %s   %s%s' % (G, self.target, name, W)
                            break
            else:
                # 并条件下存在与条件： 1&&2&&(3||4)
                for rule in key.split('&&'):
                    num = 0
                    if '||' in rule:
                        for _rule in rule.split('||'):
                            if self.check_rule(_rule):
                                num += 1
                                break
                    else:
                        if self.check_rule(rule):
                            num += 1
                if num == len(key.split('&&')):
                    self.finger.append(name)
                    # print '%s[+] %s   %s%s' % (G, self.target, name, W)

    def thread(self):
        response = send(self.url)
        if response is None:
            return False
        else:
            self.title = BS(response.text, "lxml").title.text.strip().strip('\n')
            self.body = response.text
            self.header = response.headers
            thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count)
            futures = (thread_pool.submit(self.match, id) for id in range(0, int(self.count())))
            for i in concurrent.futures.as_completed(futures):
                pass
            return True
