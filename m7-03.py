# coding=utf-8

import time

from lib.banner import show_banner
from lib.input_parser import input_parse
from whatweb_api import whatweb_scan
from load_fingerprint_db1 import load_db1_scan
from load_fingerprint_db2 import load_db2_scan
from load_fingerprint_db3 import load_db3_scan
from fofa_db import FofaCmsFinger
from lib.logger import logger

def main():
    show_banner()
    params = input_parse()
    if params.url[-1] == "/":
        url = params.url
    else:
        url = params.url + "/"
    # url = "https://www.qhlingwang.com/"
    threads_count = params.count
    sleep_time = params.sleep
    scan_interval = 3

    # 先输出fofa指纹库中匹配的信息
    print("[*]Using fofa database to scan...")
    logger.info("use fofa database to scan")
    fofa = FofaCmsFinger(url)
    fofa.run()

    # 分别使用whatweb api和不同指纹库扫描识别CMS
    time.sleep(scan_interval)
    print("[*]Using whatweb api to scan...")
    logger.info("use whatweb api to scan")
    if not whatweb_scan(url):
        time.sleep(scan_interval)
        print("[*]Using fingerprint database1 to scan...")
        logger.info("use fingerprint database1 to scan")
        if not load_db1_scan(url, threads_count, sleep_time):
            time.sleep(scan_interval)
            print("[*]Using fingerprint database2 to scan...")
            logger.info("use fingerprint database2 to scan")
            if not load_db2_scan(url, threads_count, sleep_time):
                time.sleep(scan_interval)
                print("[*]Using fingerprint database3 to scan...")
                logger.info("use fingerprint database3 to scan")
                if not load_db3_scan(url, threads_count, sleep_time):
                    print("[-]Not found CMS.")
                    logger.info("not found cms")

    print("[*]Finished.")
    logger.info("finished")

if __name__ == '__main__':
    main()
