#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015    liukelin
# @author: liukelin      314566990@qq.com
import time
import alipay_config as alipay_config_class
from lib import alipay_submit_class
from lib import alipay_notify_class
from urllib import urlencode, urlopen
from vip import settings
#
# 请求支付
# @param data 请求post数据
# @return 支付跳转from表单
#
def alipay_pay(data = {}):
    config_ = alipay_config_class.alipay_config()
    payment_type = "1"
    anti_phishing_key = ""  # 防钓鱼时间戳
    exter_invoke_ip = ""  # 客户端的IP地址

    DOMAIN = settings.HOST
    alipay_gateway_new = 'https://mapi.alipay.com/gateway.do?'
    #服务器异步通知页面路径
    notify_url = DOMAIN + "/alipay_notify_url/"
    #需http://格式的完整路径，不允许加?id=123这类自定义参数

    # 服务器同步通知页面路径
    return_url = DOMAIN + "/alipay_return_url/"
    # 需http://格式的完整路径，不允许加?id=123这类自定义参数

    #支付宝合作商户网站唯一订单号
    out_trade_no = data['out_trade_no']

    #商品的标题
    subject = data['subject']
    # 必填

    #订单的资金总额
    total_fee = data['total_fee']
    #必填

    #商品详情
    body = data['body']
    #必填


    #构造要请求的参数数组，无需改动
    parameter = {
        'service': "mobile.securitypay.pay",
        'partner': config_['partner'],
        'payment_type': payment_type,
        'notify_url': notify_url,
        # 'return_url': return_url,
        'seller_email': config_['seller_email'],
        'out_trade_no': out_trade_no,
        'subject': subject,
        'total_fee': total_fee,
        'body': body,
        'anti_phishing_key': anti_phishing_key,
        'exter_invoke_ip': exter_invoke_ip,
        '_input_charset': config_['input_charset'].lower(),
    }

    #建立请求
    alipaySubmit = alipay_submit_class.AlipaySubmit(config_)
    # html_text = alipaySubmit.buildRequestForm(parameter, "get", "ok")
    # return html_text
    para = alipaySubmit.buildRequestPara(parameter)
    return para


# 支付宝服务器异步通知
# @param request_data 请求post数据
# @return 支付跳转from表单
def notify_url(request_data) :
    #计算得出通知验证结果
    config_ = alipay_config_class.alipay_config()
    #计算得出通知验证结果
    alipayNotify = alipay_notify_class.AlipayNotify(config_)
    verify_result = alipayNotify.verifyNotify(request_data)

    if verify_result :    #验证成功
        #批量付款数据中转账成功的详细信息
        # $success_details = $_POST['success_details'];
        # #批量付款数据中转账失败的详细信息
        # $fail_details = $_POST['fail_details'];
        # echo "success";  
        #调试用，写文本函数记录程序运行情况是否正常
        #logResult("这里写入想要调试的代码变量值，或其他运行的结果记录");
        return True
    else :
        #验证失败
        # "fail"
        return False
