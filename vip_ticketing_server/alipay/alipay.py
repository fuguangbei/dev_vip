# -*- coding: utf-8 -*-
import rsa
import base64
import os
from urllib import quote
import time
import json
import urllib
import datetime
from django.utils import timezone

from django.conf import settings
from urllib import urlencode
import uritools
from vip import settings

_private_rsa_key = None
_public_rsa_key_ali = None

#def module_init():
path = os.path.dirname(__file__)
priv_path = os.path.abspath(os.path.join(path, "rsa_private_key.pem"))
pub_path = os.path.abspath(os.path.join(path, "rsa_public_key.pem"))
pub_path_ali = os.path.abspath(os.path.join(path, "rsa_public_key_ali.pem"))

pem = open(priv_path, "r").read()
_private_rsa_key = rsa.PrivateKey.load_pkcs1(pem)

pem = open(pub_path_ali, "r").read()
_public_rsa_key_ali = rsa.PublicKey.load_pkcs1_openssl_pem(pem)

#init when run
#module_init()

class Alipay(object):
    ## default value
    _input_charset = "utf-8"
    sign_type = "RSA"# only support RSA
    payment_type = 1

    # get value from settings.py
    # partner id, len=16 (2088...)
    partner = '2088102168670384'    #合作身份者id，以2088开头的16位纯数字
    notify_url = settings.HOST + "/alipay_notify_url/"
    # the account id of seller (email or phone or partner id)
    seller_id = 'clairecayman@icloud.com'
    appid = "2016090101835295"
    method = "alipay.trade.app.pay"


    def __init__(self, out_trade_no, subject, body, total_fee):
        # unique value, max=64
        self.out_trade_no = out_trade_no
        # order title/ trade keys, max=128
        self.subject = subject
        # the detail info of order, max=512
        self.body = body
        # the total pay fee
        self.total_fee = total_fee

    def init_optional_value(self, it_b_pay):
        # order timeout, m:minute, h:hour, d:day ("30m")
        self.it_b_pay = it_b_pay

    def _build_sign_url(self):
        url = ""
        # static value
        biz_content = {}
        biz_content["seller_id"] = ""
        biz_content["total_amount"] = str(self.total_fee)

        biz_content["subject"] = self.subject
        biz_content["out_trade_no"] = self.out_trade_no
        biz_content["timeout_express"] = "3m"
        biz_content["product_code"] = "QUICK_MSECURITY_PAY"
        biz_content["body"] = self.body
        url = url + 'app_id=%s' % quote(self.appid)
        # url = url + '&biz_content=%s' % quote(str(biz_content).replace("'",'"'))
        url = url + '&biz_content=%s' % quote(json.dumps(biz_content).replace("'", '"'))
        url = url + '&charset=%s' % quote(self._input_charset)
        url = url + '&method=%s' % quote(self.method)
        url1 = self.notify_url
        # url1 = url1.decode('gbk', 'replace')
        url1 = quote(url1).replace("/","%2F")
        url = url + '&notify_url=%s' % quote(url1, safe="%/:=&?~#+!$,;'@()*[]") #quote(self.notify_url)
        url = url + '&sign_type=%s' % quote(self.sign_type)
        url = url + '&timestamp=%s' % quote(time.strftime('%Y-%m-%d %X',time.localtime(time.time())))
        url = url + '&version=%s' % quote("1.0")
        return url

    def _build_sign(self):
        url = ""
        # static value
        biz_content = {}
        biz_content["seller_id"] = ""
        biz_content["total_amount"] = str(self.total_fee)

        biz_content["subject"] = self.subject
        biz_content["out_trade_no"] = self.out_trade_no
        biz_content["timeout_express"] = "3m"
        biz_content["product_code"] = "QUICK_MSECURITY_PAY"
        biz_content["body"] = self.body

        url = url + 'app_id=%s' % self.appid
        url = url + '&biz_content=%s' % (json.dumps(biz_content).replace("'",'"'))

        url = url + '&charset=%s' % self._input_charset
        url = url + '&method=%s' % self.method

        url = url + '&notify_url=%s' % self.notify_url
        url = url + '&sign_type=%s' % self.sign_type
        url = url + '&timestamp=%s' % time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        url = url + '&version=%s' % "1.0"
        return url


    def _create_sign(self, content):
        content = content.encode(self._input_charset)
        sign = rsa.sign(content, _private_rsa_key, "SHA-1")
        sign = base64.encodestring(sign).replace("\n", "")
        sign = {"sign":sign}
        sign = urlencode(sign)
        return sign[5:]

    def create_pay_url(self):
        content = self._build_sign_url()
        signcontent = self._build_sign()
        sign_url = self._create_sign(signcontent)
        result = "%s&sign=%s" % (content, sign_url)
        # result = {"result":result}
        # result = urlencode(result)
        return result

def notify_sign_value(request, content, key):
    if key in request.POST:
        value = request.POST[key]
        print "key: ", key, "value: ", value
        return "&%s=%s"%(key, value)
    else:
        return ""

def check_notify_sign(request):
    """
    按照字母顺序排序，然后使用阿里云的公匙验证。
    """
    content = ""
    post_list = sorted(request.POST.iteritems(), key=lambda d:d[0], reverse=False)
    for key_value in post_list:
        if key_value[0] not in ["sign", "sign_type"]:
            content = "%s&%s=%s"%(content, key_value[0], key_value[1])
            print content
    #remove the first &
    content = content[1:]
    content = content.encode("utf-8")
    try:
        sign = request.POST["sign"]
        sign = base64.decodestring(sign)
        rsa.verify(content, sign, _public_rsa_key_ali)
        return True
    except Exception,e:
        print "check_notify_sign error", e
        return False
