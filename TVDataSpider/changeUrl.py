# encoding: utf-8
import hashlib
import random
import urllib.request
import json
import time

from bs4 import BeautifulSoup

from TVDataSpider.constant import Constant

BASEURL = 'http://211.149.211.194:80/'

def requestResult(requestUrl):
    headers = {'User-Agent': Constant.userAgent}
    tempRequest = urllib.request.Request(url=requestUrl, headers=headers)
    try:
        tempResponse = (urllib.request.urlopen(tempRequest))
        return tempResponse
    except:
        return ''

def deleteBOM(tempStr):
    if tempStr.startswith(u'\ufeff'):
        tempStr = tempStr.encode('utf-8')[3:].decode('utf-8')
        return tempStr
    else:
        return tempStr

def proxy_hoge(url, referer, ver):
    api = '';
    strref = '';
    tm = str(int(time.time()))
    token = '862DF6728D919D06E3182D5129832559'
    str1 = token + ver + referer + tm + url + token
    m = hashlib.md5()
    m.update(str1.encode('UTF-8'))
    hash = m.hexdigest()
    if referer:
        strref = "&refererurl=" + referer
    if url.find(".ahtv.cn") > 0:
        api = 'http://ahtv.live.ttzx.tv/m2o/player/drm.php'
    if url.find(".fjtv.net") > 0:
        api = 'http://fjtv.live.ttzx.tv/m2o/player/drml.php'
    if api:
        url1 = api + '?url=' + url + strref + '&time=' + tm + '&hash=' + hash + '&playerVersion=' + ver
        return deleteBOM(str(requestResult(url1).read(), encoding="UTF-8"))

def requestRightAddress(address):
    if address:
        return urlParsing(address)
    else:
        return 'error'

def urlParsing(uri):
    if uri != '' and uri.find('://') > 0:
        sign = '&splatid=1036'
        vid = uri[(uri.index('://') + 3):]

        # letv:// 开头的视频地址
        if uri.find('letv://') == 0:
            LETVURL = BASEURL
            stream_id = vid.split("&")[0]
            url = 'letv.php?act=geturl' + sign + '&stream_id=' + stream_id + '&_t=' + str(random.randint(1000, 9999))
            tempUrl = deleteBOM(str(requestResult(LETVURL + url).read(), encoding="UTF-8"))
            leuri = json.loads(tempUrl)['url']
            if leuri.find('.letv.com') > 0 or leuri.find('.lecloud.com') > 0:
                leuri += '&jsonp=?'
            if requestResult(LETVURL + leuri):
                try:
                    tempStr = deleteBOM(str(requestResult(LETVURL + leuri).read(), encoding="UTF-8"))
                    jDict = json.loads(tempStr)
                    if jDict['location']:
                        muri = jDict['location']
                        list = jDict['nodelist']
                        for tempList in list:
                            m3u8 = tempList['location']
                            if m3u8.find("&path=") > 0:
                                muri = m3u8
                                break
                        return muri
                except :
                    return 'error'

        # http://uri.itv186.cn/vlive/ 开头的视频地址
        elif uri.find('http://uri.itv186.cn/vlive/') == 0:
            ITVURL = 'http://uri.itv186.cn/vlive/'
            url = 'letv.php?act=geturl' + sign + '&url=' + uri + '&_t=' + str(random.randint(1000, 9999))
            itvFirstRequest = urllib.request.Request(BASEURL + url)
            itvFirstResponse = (urllib.request.urlopen(itvFirstRequest))
            itvFirstUri = json.loads(itvFirstResponse.read(), encoding="UTF-8")['url']
            itvSecondRequest = urllib.request.Request(ITVURL + itvFirstUri)
            itvSecondResponse = urllib.request.urlopen(itvSecondRequest).read()
            itvSecondData = itvSecondResponse.decode('UTF-8')
            p_m3u8 = itvSecondData.split("\n")
            for tmpStr in p_m3u8:
                if tmpStr != '' and tmpStr.find("://") > 0:
                    return tmpStr;


        # .ahtv.cn视频地址
        elif uri.find('.ahtv.cn') > 0 and uri.find('.m3u8') > 0:
            return proxy_hoge(uri, "http://www.ahtv.cn/", "4.0.3")

        # fjtv.net视频地址
        elif uri.find(".fjtv.net") > 0 and uri.find(".m3u8") > 0:
            return proxy_hoge(uri, "http://v.fjtv.net/", "4.0.3")

        # http:// 开头的视频地址
        elif uri.find("http://") == 0:
            if uri.find("") > -1:
                uri = uri.replace("http://live.aishang.", "http://125.88.39.78/live.aishang.")
                return uri

        # hunantv:// 开头的视频地址
        elif uri.find('hunantv://') == 0:
            try:
                url = 'http://live.api.hunantv.com/pc/getById?liveId=' + vid + '&liveType=2&callback=?'
                tempStr = deleteBOM(str(requestResult(url).read(), encoding="UTF-8")).replace('?(', '').replace(')', '')
                return json.loads(tempStr)['data']['html5Sources'][0]['url']
            except:
                return 'error'

        # pa:// 开头的视频地址
        elif uri.find("pa://") == 0:
            url = 'cntv.php?channel=' + uri + '&client=iosapp'
            tempStr = deleteBOM(str(requestResult(BASEURL + url).read(), encoding="UTF-8"))
            hls_url = json.loads(tempStr.encode('utf8')[3:].decode('utf8'))['hls_url']
            hls1 = hls_url['hls4'];
            hls2 = hls_url['hls2'];
            hls3 = hls_url['hls3'];
            hls4 = hls_url['hls1'];
            hls5 = hls_url['hls5'];
            hls6 = hls_url['hls6'];
            if hls1 and hls1.find(".m3u8") > 7:
                return hls1
            elif hls2 and hls2.find(".m3u8") > 7:
                return hls2
            elif hls3 and hls3.find(".m3u8") > 7:
                return hls3
            elif hls4 and hls4.find(".m3u8") > 7:
                return hls4
            elif hls5 and hls5.find(".m3u8") > 7:
                return hls5
            elif hls6 and hls6.find(".m3u8") > 7:
                return hls6

        # pplive:// 开头的视频地址
        elif uri.find("pplive://") == 0:
            ppurl = 'http://play.api.pptv.com/boxplay.api?id=300146&type=m3u8.web.phone&gslbversion=2&ft=2&version=4&userLevel=1&appver=4.2.5&appid=com.pptv.iphoneapp&playback=0&o=pub.pptv.com'
            if len(vid)> 15:
                tempStr = deleteBOM(str(requestResult(ppurl + '&callback=?').read(), encoding="UTF-8")).replace('\\', '')
                ppSoup = BeautifulSoup(tempStr, 'lxml')
                host = ppSoup.find('sh').getText()
                key = ppSoup.find('key').getText()
                puri = "http://" + host + "/live/5/30/" + vid + ".m3u8?playback=0&pre=ikan&o=pub.pptv.com&type=m3u8.web.phone&k=" + key
                return puri
            else:
                return "http://web-play.pptv.com/web-m3u8-" + vid + ".m3u8?type=m3u8.web.phone&playback=0&o=pub.pptv.com"

        # :// 开头的视频地址
        elif uri.find("://") > 2:
            url = "letv.php?act=geturl" + sign + "&channel=" + vid + "&_t=" + str(random.randint(1000, 9999))
            tempStr = deleteBOM(str(requestResult(BASEURL + url).read(), encoding="UTF-8"))
            return json.loads(tempStr)['url']

