# M7-03

个人使用的一款Web CMS指纹扫描器。线上的话就推荐云悉了。

步骤及原理：

1. 使用Fofa的CMS指纹库输出相关banner信息，这部分参考的：[TideSec/TideFinger](https://github.com/TideSec/TideFinger)
2. 使用whatweb API扫描CMS，若未找到具体CMS则进行下一步
3. 分别使用GitHub上收集的三个不同的CMS指纹库进行扫描

使用方法：

```powershell
Usage: python m7-03.py -u <Target URL> [-t <Thread_count>] [-s <Sleep_time>] [-l <Log_level>]

Options:
  -h, --help            show this help message and exit
  -v, --version         show scanner's version and exit
  -u URL, --url=URL     target url for scan
  -t COUNT, --thread=COUNT
                        [Optional] scan thread_count (default 30)
  -s SLEEP, --sleep=SLEEP
                        [Optional] sleep time per request (default 1s)
  -l LOGLEVEL, --log-level=LOGLEVEL
                        [Optional] log level 1-5:
                        CRITICAL,ERROR(default),WARNING,INFO,DEBUG
```

-u参数为必须项、指定扫描的目标URL；其余为可选项，-t参数指定多线程的数量，-s参数指定线程请求之间的休眠时间，-l参数指定日志记录的级别。

具体扫描过程可根据log目录下的日志文件进行分析。

待添加功能：代理IP池

扫描效果：

```powershell
PS M:\M7-03> python m7-03.py -u https://www.qhlingwang.com                                               

        _|      _|  _|_|_|_|_|                _|    _|_|_|
        _|_|  _|_|          _|              _|  _|        _|
        _|  _|  _|        _|    _|_|_|_|_|  _|  _|    _|_|
        _|      _|      _|                  _|  _|        _|
        _|      _|    _|                      _|    _|_|_|  v1.0



[*]Using fofa database to scan...
[+]Fofa banner info: jquery,
[*]Using whatweb api to scan...
[-]Not found CMS by whatweb, some other info: {'error': '源码太大,忽略识别'}
[*]Using fingerprint database1 to scan...
[+]Found CMS: EmpireCMS(帝国)
[*]Finished.
PS M:\M7-03>                                                     
```

