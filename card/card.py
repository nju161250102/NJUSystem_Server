# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request
import requests
import json
import datetime
from bs4 import BeautifulSoup

cardModule = Blueprint('card', __name__)


# 从三个接口获取校园卡相关信息
@cardModule.route('/info/', methods=['GET'])
def info():
    jar = requests.utils.cookiejar_from_dict(request.cookies)
    r1 = requests.get('http://mapp.nju.edu.cn/mobile/getCardInfo.mo', cookies=jar)
    # print r1.content
    r2 = requests.get('http://cpay.nju.edu.cn/pay/bankcard/list', cookies=jar)
    # print r2.content
    r3 = requests.get('http://cpay.nju.edu.cn/pay/ykt/cardstatus', cookies=jar)
    # print r3.content
    data = json.loads(r3.content)["data"]
    status = "正常"
    if data["frozenflag"] != "0":
        status = "冻结"
    if data["lockflag"] != "0":
        status = "锁定"
    if data["lossflag"] != "0":
        status = "挂失"
    res_data = {
        "name": json.loads(r1.content, encoding='utf-8')["data"]["name"],
        "balance": json.loads(r1.content, encoding='utf-8')["data"]["balance"],
        "bankCardNo": json.loads(r2.content, encoding='utf-8')["data"]["bankcards"][0]["bankcardno"],
        "status": status.decode('utf-8')
    }
    return json.dumps(res_data, ensure_ascii=False)


# 接口地址https://oa.nju.edu.cn/ecard/web/，访问速度很慢
@cardModule.route('/record/', methods=['GET'])
def oa_record():
    # 获取请求中查询参数，并转换日期格式
    start_date = request.args.get("from").replace("-", "/")
    end_date = request.args.get("to").replace("-", "/")
    jar = requests.utils.cookiejar_from_dict(request.cookies)

    details = []
    date_num = datetime.datetime.strptime(end_date, '%Y/%m/%d') - datetime.datetime.strptime(start_date, '%Y/%m/%d')
    daily = [0] * (date_num.days + 1)
    page_num = 0
    income = 0
    expense = 0

    # 获取校园卡卡号
    r1 = requests.get('http://cpay.nju.edu.cn/pay/ykt/cardstatus', cookies=jar)
    card_no = json.loads(r1.content)["data"]["cardno"]

    while True:
        # 构造POST请求数据
        post_data = {
            "beginDate": start_date,
            "endDate": end_date,
            "cardId": card_no,
            "serialType": 1,
            "page": page_num,
        }
        r = requests.post("https://oa.nju.edu.cn/ecard/njuLogin", data=post_data, cookies=jar, allow_redirects=False)
        rr = requests.post(
            "https://oa.nju.edu.cn/ecard/web/"+r.cookies.get("LOGIN")+"/1?p_p_id=querydetail&p_p_action=1&p_p_state=maximized&p_p_mode=view&_querydetail_struts_action=%2Fext%2Fecardtransactionquerydetail_result"
            , data=post_data, cookies=r.cookies, verify=False)
        # 解析HTML结果
        soup = BeautifulSoup(rr.text, "html.parser")
        trs = soup.find_all(name='tr', attrs={"class": ["tr_1", "tr_2"]})
        for tr in trs:
            _soup = BeautifulSoup(str(tr), "html.parser")
            tds = _soup.find_all(name='td')
            item = {
                "transName": tds[0].get_text(strip=True),
                "termName": tds[1].get_text(strip=True),
                "transTime": tds[3].get_text(strip=True),
                "amount": tds[4].get_text(strip=True),
                "balance": tds[5].get_text(strip=True),
            }
            if float(item["amount"]) < 0:
                expense += (- float(item["amount"]))
                delta = datetime.datetime.strptime(item["transTime"], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_date, '%Y/%m/%d')
                daily[delta.days] += (- float(item["amount"]))
            else:
                income += float(item["amount"])
            details.append(item)
        # 检查是否还有剩余数据
        page_soup = soup.find_all(name='td', attrs={"class": "text_brown", "align": "center"})
        page_flag = page_soup[0].get_text(strip=True)
        if page_flag.split('/')[0] == page_flag.split('/')[1]:
            break
        page_num += 1

    return json.dumps({
        "details": details,
        "daily": daily,
        "income": "%.2f" % income,
        "expense": "%.2f" % expense
    }, ensure_ascii=False)


# 废弃接口, 因为仅能显示部分记录
def record():
    jar = requests.utils.cookiejar_from_dict(request.cookies)
    start_date = request.args.get("from")
    end_date = request.args.get("to")
    details = []
    date_num = datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')
    daily = [0] * (date_num.days + 1)
    in_sum = 0
    out_sum = 0
    page = 1
    flag = True
    while flag:
        r = requests.get('http://mapp.nju.edu.cn/mobile/getTransList.mo?pageSize=50&page=' + str(page), cookies=jar)
        item_list = json.loads(r.content, encoding='utf-8')["data"]["items"]
        for item in item_list:
            if compare_date(start_date, item["transTime"]) >= 0:
                if compare_date(end_date, item["transTime"]) <= 0:
                    details.append(item)
                    if item["amount"][0] == '-':
                        out_sum += float(item["amount"][1:])
                        daily[compare_date(start_date, item["transTime"])] += float(item["amount"][1:])
                    else:
                        in_sum += float(item["amount"][1:])
            else:
                flag = False
        page += 1
    return json.dumps({
        "details": details,
        "daily": daily.reverse(),
        "income": in_sum,
        "expense": out_sum
    }, ensure_ascii=False)


# 求日期相差的天数
# time1: YYYY-mm-dd time2:yy-MM-dd HH:MM
# 返回 time2 - time1
def compare_date(time1, time2):
    time_a = datetime.datetime.strptime(time1, '%Y-%m-%d')
    time_b = datetime.datetime.strptime(time2, '%y-%m-%d %H:%M')
    delta = time_b - time_a
    return delta.days
