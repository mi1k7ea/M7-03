# coding=utf-8

import requests
import hashlib

from lib.header_generator import get_headers

def send(url):
    response = requests.get(url, headers=get_headers(), verify=False, timeout=5)
    if response.status_code != 200:
        return None
    return response

def get_md5(content):
    m5 = hashlib.md5()
    m5.update(content.encode(encoding='utf-8'))
    return m5.hexdigest()