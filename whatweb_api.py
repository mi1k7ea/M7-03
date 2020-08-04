# coding=utf-8

import urllib3
urllib3.disable_warnings()

import requests
import zlib
import json

from lib.header_generator import get_headers
from lib.logger import logger

def upload_to_whatweb(url):
    response = requests.get(url, headers=get_headers(), verify=False, timeout=5)
    whatweb_dict = {"url": response.url, "text": response.text, "headers": dict(response.headers)}
    whatweb_dict = json.dumps(whatweb_dict)
    whatweb_dict = whatweb_dict.encode()
    whatweb_dict = zlib.compress(whatweb_dict)
    data = {"info": whatweb_dict}
    return requests.post("http://whatweb.bugscaner.com/api.go", files=data)

def whatweb_scan(url):
    response = upload_to_whatweb(url)
    # print("[*]Use remaining times today:", response.headers["X-RateLimit-Remaining"])
    if "CMS" in response.json().keys():
        print("[*]Found CMS:", response.json()['CMS'][0])
        logger.info("found cms " + response.json()['CMS'][0])
        return True
    else:
        print("[-]Not found CMS by whatweb, some other info:", response.json())
        logger.info("not found CMS by whatweb")
        return False
