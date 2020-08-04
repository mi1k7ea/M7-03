# coding=utf-8

import threading
import queue
import json

from lib.sender import send, get_md5

# 通过Event来控制多线程的终止
event = threading.Event()
event.set()

class ScanCMS(threading.Thread):
    def __init__(self, work_queue, url, threads_count):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.url = url
        self.threads_count = threads_count

    def run(self):
        while not self.work_queue.empty():
            if not event.is_set():
                exit(0)
            data = self.work_queue.get()
            cms_url = self.url + data["url"]
            print("[*]Start to check URL:", cms_url)
            response = send(cms_url)
            if response is None or response.text is None:
                continue
            if data["re"]:
                if response.text.find(data["re"]) != -1:
                    print("[*]Found CMS:", data["name"])
                    event.clear()
            else:
                response_text_md5 = get_md5(response.text)
                if response_text_md5 == data["md5"]:
                    print("[*]Found CMS:", data["name"])
                    event.clear()

def main():
    url = "http://www.jxlhs.com"
    threads = []
    threads_count = 10
    work_queue = queue.Queue()

    with open("fingerprint/data.json", "rb") as f:
        finger_data = json.load(f, encoding="utf-8")
        for data in finger_data:
            work_queue.put(data)

    for i in range(threads_count):
        thread = ScanCMS(work_queue, url, threads_count)
        threads.append(thread)

    for i in threads:
        i.start()

    for i in threads:
        i.join()

if __name__ == '__main__':
    main()