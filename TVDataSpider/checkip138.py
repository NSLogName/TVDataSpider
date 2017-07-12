# encoding: utf-8
import re
import urllib.request


def ISIP(s):
    return len([i for i in s.split('.') if (0 <= int(i) <= 255)]) == 4


def URL(ip):
    request = urllib.request.Request('http://m.ip138.com/ip.asp?ip=%s' % ip)
    response = (urllib.request.urlopen(request, timeout=3000).read())
    fip = response.decode('UTF-8')
    rip = re.compile(r'</h1><p class="result">本站主数据：(.*)</p><p class="result">')
    result = rip.findall(fip)
    return str("%s\t %s" % (ip, result[0]))


def checkip(ip):
    if not re.findall('(\d{1,3}\.){3}\d{1,3}', ip):
        if re.findall(r'(\w+\.)?(\w+)(\.\D+){1,2}', ip):
            DOMAIN = ip
            return URL(DOMAIN)
        else:
            return "输入的IP地址和域名格式不对！"
    else:
        if ISIP(ip):
            IPADDRESS = ip
            return URL(IPADDRESS)
        else:
            return "IP 地址不合法，请重新输入！"


if __name__ == "__main__":
    INPUT = 'www.jb51.com'
    print(checkip(INPUT))