# coding=utf-8

from optparse import OptionParser
import sys
from urllib import request, error
import logging

from lib.logger import log, logger
from lib.conf import DEFAULT_LOG_LEVEL, DEFAULT_THREAD_COUNT, DEFAULT_SLEEP_TIME

# 解析命令行输入参数
def input_parse():
    parser = OptionParser('python m7-03.py -u <Target URL> [-t <Thread_count>] [-s <Sleep_time>] [-l <Log_level>]')
    parser.version = "M7-03 v1.0"
    parser.add_option("-v", "--version", dest="version", action="store_true", help="show scanner's version and exit")
    parser.add_option('-u', '--url', dest='url', type='string', help='target url for scan')
    parser.add_option('-t', '--thread', dest='count', type='int', default=DEFAULT_THREAD_COUNT, help='[Optional] scan thread_count (default 30)')
    parser.add_option('-s', '--sleep', dest='sleep', type='int', default=DEFAULT_SLEEP_TIME, help='[Optional] sleep time per request (default 1s)')
    parser.add_option('-l', '--log-level', dest='loglevel', type='int', default=DEFAULT_LOG_LEVEL, help='[Optional] log level 1-5: CRITICAL,ERROR(default),WARNING,INFO,DEBUG')
    (options, args) = parser.parse_args()

    if options.version:
        print(parser.version, "  --  By Mi1k7ea")
        sys.exit(1)

    # url参数是必须的且能正常访问
    if not options.url:
        parser.print_help()
        sys.exit(1)
    else:
        try:
            request.urlopen(options.url)
        except error.HTTPError:
            parser.error("URL can not be visited.")
        except error.URLError:
            parser.error("URL can not be visited.")

    # 设置日志级别: 1-5
    log_level = options.loglevel
    if log_level == 1:
        log_level = logging.CRITICAL
    elif log_level == 2:
        log_level = logging.ERROR
    elif log_level == 3:
        log_level = logging.WARN
    elif log_level == 4:
        log_level = logging.INFO
    elif log_level == 5:
        log_level = logging.DEBUG
    else:
        parser.error("Log level value must be between 1-5.")

    # 以域名或IP地址为日志文件名，开启日志功能
    log_name = options.url.split("://")[1].split("/")[0].replace(".", "_")
    log(log_name, log_level)

    if options.count <= 0 or options.count > 100:
        logger.error("Thread count invalid.")
        parser.error("Thread count should between 1-100.")

    if options.sleep < 0 or options.sleep > 10:
        logger.error("Sleep time invalid.")
        parser.error("Sleep time should between 0-10.")

    logger.info("Log level is " + str(options.loglevel))
    logger.info("Thread count is " + str(options.count))
    logger.info("Sleep time is " + str(options.sleep) + "s")
    return options
