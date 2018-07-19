# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request
from flask import Response
import json
import requests

loginModule = Blueprint('login', __name__)


@loginModule.route('/', methods=['POST'])
def login():
    req_data = json.loads(request.data)
    post_data = {
        "IDToken1": req_data["name"],
        "IDToken2": req_data["key"],
        "inputCode": req_data["code"],
        "encoded": "false"
    }
    # 注入验证码对应的cookie
    jar = requests.utils.cookiejar_from_dict(request.cookies)
    # 禁止重定向以获得登录的cookie
    r = requests.post("http://cer.nju.edu.cn/amserver/UI/Login", data=post_data, cookies=jar, allow_redirects=False)
    result = []
    res = Response(mimetype='application/json')
    if len(r.content) == 0:
        result.append('cer_success')
        for key, value in r.cookies.items():
            res.set_cookie(key, value)
    res.set_data(json.dumps(result, ensure_ascii=False))
    return res


# 获得验证码图片并保存cookie, 验证码对应登录网址为http://cer.nju.edu.cn/amserver/UI/Login
@loginModule.route('/cer_code', methods=['GET'])
def cer_code():
    r = requests.get("http://cer.nju.edu.cn/amserver/verify/image.jsp")
    res = Response(r.content, mimetype="image/jpg")
    for key, value in r.cookies.items():
        res.set_cookie(key, value)
    return res
