# encoding: utf-8
import datetime
import random
import logging
from logging.config import fileConfig
import time
from math import floor


class Constant():
    user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        ]

    userAgent = random.choice(user_agent_list)

    Success_Status = 0
    Success_Msg = '数据获取成功'

    None_Status = 10000
    None_Msg = '暂无数据'

    Error_Status = 10001
    Error_Msg = '参数错误'

class Logger():
    fileConfig('log/logging.ini')
    sechdLogger = logging.getLogger('sechd')
    defaultLogger = logging.getLogger('default')
    visitLogger = logging.getLogger('visit')
    grabberLogger = logging.getLogger('grabber')

class Time():
    # 获取当前时间
    def getNowTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    # 计算时间差
    def timedelta(self, startTimeStr, endTimeStr):
        startTime = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S')
        endTime = datetime.datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S')
        secInt = (endTime - startTime).seconds
        minStr = str(floor((secInt) / 60))
        secStr = str(secInt % 60)
        if int(minStr) <= 0:
            return '共计耗时' + secStr + '秒'
        else:
            return '共计耗时' + minStr + '分' + secStr + '秒'

