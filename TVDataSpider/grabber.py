# encoding: utf-8
import os
import urllib.request
import psutil
from bs4 import BeautifulSoup

from TVModel.models import Type
from TVModel.models import Program
from TVModel.models import ProgramDetail

from TVDataSpider.constant import Constant
from TVDataSpider.constant import Logger
from TVDataSpider.constant import Time

# BASEURL = 'http://iptv.cdzmn.com/tv.php'

BASEURL = 'http://211.149.211.194:80/tv.php'

# 利用bs4解析网页
def resolveHtml(url, tag):
    try:
        # 获取一级网页信息
        headers = {'User-Agent': Constant.userAgent}
        request = urllib.request.Request(url = url, headers = headers)
        response = (urllib.request.urlopen(request,timeout = 3000).read())
        data = response.decode('UTF-8')

        # 利用bs解析一级网页信息
        soup = BeautifulSoup(data, 'lxml')
        list = soup.find_all(tag)

        if list:
            return list
        else:
            return None
    except:
        Logger.grabberLogger.exception('网页解析错误，当前url为：' + url)

# 抓取程序入口
def grabData():
    Logger.grabberLogger.info("########################################################################")
    # 获取当前运行的pid
    p1 = psutil.Process(os.getpid())
    # 该进程所占cpu的使用率
    Logger.grabberLogger.info("抓取前进程pid:" + str(p1.pid) + ',' + "CPU占用率: " + (str)(p1.cpu_percent(None)) + "%" + ',' +'内存占用率: ' + "%.2f%%" % (p1.memory_percent()) + '\n')
    try:
        myTime = Time()
        startTimeStr = myTime.getNowTime()
        grabTypeData()
        endTimeStr = myTime.getNowTime()
        p2 = psutil.Process(os.getpid())
        Logger.grabberLogger.info("抓取后进程pid:" + str(p2.pid) + ',' + "CPU占用率: " + (str)(p2.cpu_percent(None)) + "%" + ',' +'内存占用率: ' + "%.2f%%" % (p2.memory_percent()))
        Logger.grabberLogger.info('本次数据抓取' + myTime.timedelta(startTimeStr, endTimeStr))
        Logger.grabberLogger.info("########################################################################" + "\n\n\n")
    except:
        Logger.grabberLogger.info("########################################################################" + "\n\n\n")

# 抓取第一层type页面信息
def grabTypeData():
    try:
        myTime = Time()
        startTimeStr = myTime.getNowTime()
        Logger.grabberLogger.info("*************************************************")
        Logger.grabberLogger.info(startTimeStr + " " + "开始抓取第一级页面")

        typeList = resolveHtml(BASEURL, 'li')
        if typeList:

            for typeFollowMessage in typeList :
                str = typeFollowMessage.find('a').get_text().strip()
                list = Type.objects.filter(name = str)

                programTempUrl = typeFollowMessage.find('a').get('href')
                programIndex = programTempUrl.find('?')
                if programIndex > 0:
                    programUrl = BASEURL + programTempUrl[programIndex:]
                else:
                    programUrl = programTempUrl

                if list:
                    type = Type.objects.get(name=str)
                    type.url = programUrl
                    type.save()
                else:
                    type = Type()
                    type.name = str
                    type.url = programUrl
                    type.save()
            endTimeStr = myTime.getNowTime()
            Logger.grabberLogger.info(endTimeStr + " " + "第一级页面抓取结束" + ',' + myTime.timedelta(startTimeStr, endTimeStr))
            Logger.grabberLogger.info("*************************************************" + '\n')
            grabProgramData()
    except:
        Logger.grabberLogger.exception('第一级网页入库错误:')
        Logger.grabberLogger.info("*************************************************")

# 抓取第二层programe页面信息
def grabProgramData():
    try:
        myTime = Time()
        startTimeStr = myTime.getNowTime()
        Logger.grabberLogger.info("*************************************************")
        Logger.grabberLogger.info(startTimeStr + " " + "开始抓取第二级页面")

        list = Type.objects.all()
        if list:
            for type in list:
                if type.name == '咪咕':
                    programe = Program()
                    programe.name = '咪咕'
                    programe.url = type.url
                    programe.type = type.name
                    programe.save()
                else:
                    programList = resolveHtml(type.url, 'li')

                    if programList:
                        for programFollowMessage in programList:
                            str1 = programFollowMessage.find('a').get_text()
                            list1 = Program.objects.filter(name = str1)

                            thirdTempUrl = programFollowMessage.find('a').get('href')
                            thirdIndex = thirdTempUrl.find('?')
                            if thirdIndex > 0:
                                programDetailUrl = BASEURL + thirdTempUrl[thirdIndex:]
                            else:
                                programDetailUrl = thirdTempUrl


                            if list1:
                                programe = Program.objects.get(name = str1)
                                str2 = programe.type
                                programe.url = programDetailUrl
                                if str2.find(type.name) == -1:
                                    programe.type = type.name + ',' + str2
                                programe.save()
                            else:
                                programe = Program()
                                programe.name = programFollowMessage.find('a').get_text()
                                programe.url = programDetailUrl
                                programe.type = type.name
                                programe.save()
            endTimeStr = myTime.getNowTime()
            Logger.grabberLogger.info(endTimeStr + " " + "第二级页面抓取结束" + ',' + myTime.timedelta(startTimeStr, endTimeStr))
            Logger.grabberLogger.info("*************************************************" + '\n')
            grabProgramDetailData()
    except:
        Logger.grabberLogger.exception('第二级网页入库错误:')
        Logger.grabberLogger.info("*************************************************")

# 抓取第三层programDetail页面信息
def grabProgramDetailData():
    try:
        myTime = Time()
        startTimeStr = myTime.getNowTime()
        Logger.grabberLogger.info("*************************************************")
        Logger.grabberLogger.info(startTimeStr + " " + "开始抓取第三级页面")

        list = Program.objects.all()
        if list:
            for programe in list:
                programDetaiOptionlList = resolveHtml(programe.url, 'option')
                address = ''
                if programDetaiOptionlList:
                    for programDetailOptionMessage in programDetaiOptionlList:
                        str3 = programDetailOptionMessage.get_text()
                        str4 = programDetailOptionMessage.get('value')
                        address += str3 + str4 + '^'

                str5 = programe.name
                list2 = ProgramDetail.objects.filter(name=str5)

                if list2:
                    programDetail = ProgramDetail.objects.get(name=str5)
                    programDetail.address = address
                    programDetail.save()
                else:
                    programDetail = ProgramDetail()
                    programDetail.name = str5
                    programDetail.address = address
                    programDetail.save()

                programDetaiMenulList = resolveHtml(programe.url, 'li')
                if programDetaiMenulList:
                    del programDetaiMenulList[0]
                    str7 = ''
                    for programDetaiMenu in programDetaiMenulList:
                        str8 = programDetaiMenu.get_text()
                        if '微信' in str8 :
                            continue;
                        else:
                            str7 = str7 + programDetaiMenu.get_text() + '^'
                    list3 = ProgramDetail.objects.filter(name=str5)

                    if list3:
                        programDetail = ProgramDetail.objects.get(name=str5)
                        programDetail.menu = str7
                        programDetail.save()
                    else:
                        programDetail = ProgramDetail()
                        programDetail.menu = str7
                        programDetail.save()
            endTimeStr = myTime.getNowTime()
            Logger.grabberLogger.info(endTimeStr+ " " + "第三级页面抓取结束" + ',' + myTime.timedelta(startTimeStr, endTimeStr))
            Logger.grabberLogger.info("*************************************************" + '\n')
    except:
        Logger.grabberLogger.exception('第三级网页入库错误:')
        Logger.grabberLogger.info("*************************************************")