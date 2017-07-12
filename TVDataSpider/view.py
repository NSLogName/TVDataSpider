# encoding: utf-8
import demjson
import time

import TVDataSpider.changeUrl
import TVDataSpider.checkip138

from django.http import HttpResponse
from django.http import StreamingHttpResponse

from TVModel.models import Type
from TVModel.models import Program
from TVModel.models import ProgramDetail

from TVDataSpider.constant import Constant
from TVDataSpider.constant import Logger


# 获取当前时间
def getNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def hello(request):
    try:
        ip = ''
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
            ipMsg = str(TVDataSpider.checkip138.checkip(ip))
            # Logger.visitLogger.info(getNowTime() + ',' +'当前访问IP为:' + ip + ' ' + '该IP来自于：' + getIPMessage(ip))
            Logger.visitLogger.info("当前访问IP是：" + ipMsg)
    except:
        Logger.visitLogger.exception('获取访问IP出错')

    resultMap = {}
    request.encoding = 'utf-8'
    try:
        if request.method == 'POST':
            response = ''
            optionNo = request.POST['optionNo']
            name = request.POST['name']
            if optionNo == '1':
                list = Program.objects.filter(type__contains=name)
                listTmp = []
                for type in list:
                    listTmp.append(type.name)
                if listTmp:
                    resultMap = setResultMap(Constant.Success_Status, Constant.Success_Msg, listTmp)
                    json = demjson.encode(resultMap)
                else:
                    resultMap = setResultMap(Constant.Error_Status, Constant.Error_Msg)
                    json = demjson.encode(resultMap)
                response = json
                return HttpResponse(response)
            elif optionNo == '0':
                list = ProgramDetail.objects.filter(name=name)
                listTmp = []
                for programDetail in list:
                    map = {'address': programDetail.address, 'menu': programDetail.menu}
                    listTmp.append(map)
                if listTmp:
                    resultMap = setResultMap(Constant.Success_Status, Constant.Success_Msg, listTmp)
                    json = demjson.encode(resultMap)
                else:
                    resultMap = setResultMap(Constant.Error_Status, Constant.Error_Msg)
                    json = demjson.encode(resultMap)
                response = json
                return HttpResponse(response)
            elif optionNo == '2':
                listTmp = []
                map = {'playUrl': TVDataSpider.changeUrl.requestRightAddress(name)}
                listTmp.append(map)
                resultMap = setResultMap(Constant.Success_Status, Constant.Success_Msg, listTmp)
                json = demjson.encode(resultMap)
                response = json
                return HttpResponse(response)
            elif optionNo == '3':
                def file_iterator(file_name, chunk_size=512):
                    with open(file_name, encoding='UTF-8') as f:
                        while True:
                            c = f.read(chunk_size)
                            if c:
                                yield c
                            else:
                                break

                if name == 'v':
                    the_file_name = "log/log_visit.log"
                elif name == 's':
                    the_file_name = 'log/log_sechd.log'
                elif name == 'g':
                    the_file_name = 'log/log_grabber.log'

                response = StreamingHttpResponse(file_iterator(the_file_name))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

                return response
            else:
                resultMap = setResultMap(Constant.Error_Status, Constant.Error_Msg)
                json = demjson.encode(resultMap)
                response = json
                return HttpResponse(response)
        else:
            response = ''
            list = Type.objects.all()
            listTmp = []
            for type in list:
                listTmp.append(type.name)
            if listTmp:
                resultMap = setResultMap(Constant.Success_Status, Constant.Success_Msg, listTmp)
                json = demjson.encode(resultMap)

            else:
                resultMap = setResultMap(Constant.None_Status, Constant.None_Msg)
                json = demjson.encode(resultMap)
            response = json
            return HttpResponse(response)
    except:
        Logger.defaultLogger.info('接口获取数据出现错误：')


def setResultMap(status, msg, data):
    if data:
        resultMap = {'status': Constant.Success_Status, 'msg': Constant.Success_Msg, 'data': data}
        return resultMap
    else:
        resultMap = {'status': status, 'msg': msg}
        return resultMap
