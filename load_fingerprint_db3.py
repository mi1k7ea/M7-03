# coding=utf-8

import threading
import queue
import json
import time

from lib.sender import send, get_md5
from lib.logger import logger

class ScanCMS3:
    def __init__(self, work_queue, url, threads_count):
        self.work_queue = work_queue
        self.url = url
        self.threads_count = threads_count
        self.found = False

    def run(self):
        while not self.work_queue.empty() and self.found is False:
            data = self.work_queue.get()
            if data["staticurl"]:
                cms_url = self.url + data["staticurl"]
                response = send(cms_url)
                if response is None or response.text is None:
                    continue

                response_text_md5 = get_md5(response.text)
                if response_text_md5 == data["checksum"]:
                    print("[+]Found CMS:", data["cmsname"])
                    logger.info("found cms [" + data["cmsname"] + "]")
                    self.found = True
            elif data["keyword"]:
                cms_url = self.url + data["homeurl"]
                response = send(cms_url)
                if response is None or response.text is None:
                    continue
                if response.text.find(data["keyword"]) != -1:
                    print("[+]Found CMS:", data["cmsname"])
                    logger.info("found cms [" + data["cmsname"] + "]")
                    self.found = True

def load_db3_scan(url, threads_count, sleep_time):
    work_queue = queue.Queue()
    threads = []

    with open("fingerprint/cmsprint.json", "rb") as f:
        finger_data = json.load(f, encoding="utf-8")['RECORDS']
        for data in finger_data:
            work_queue.put(data)

    scan = ScanCMS3(work_queue, url, threads_count)

    for i in range(threads_count):
        t = threading.Thread(target=scan.run)
        t.setDaemon(True)
        threads.append(t)

    for t in threads:
        t.start()

    while True:
        if threading.activeCount() <= 1:
            break
        else:
            try:
                time.sleep(sleep_time)
            except KeyboardInterrupt:
                print('[*]User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount())
                logger.error("user aborted")
                scan.found = True

    return scan.found
