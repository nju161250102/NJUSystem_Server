# -*- coding:utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from login import loginModule
from card import cardModule
import requests
import json

app = Flask(__name__)
app.register_blueprint(loginModule, url_prefix='/api/login/')
app.register_blueprint(cardModule, url_prefix='/api/card/')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/personInfo/', methods=['GET'])
def person_info():
    jar = requests.utils.cookiejar_from_dict(request.cookies)
    r = requests.get("http://imp.nju.edu.cn/imp/iss/myAccount.do?action=getMyAcount", cookies=jar)
    req_data = json.loads(r.content)
    res_data = {
        "name": req_data["username"],   # 姓名
        "id": req_data["userid"],       # 学号
        "identity": req_data["card"],   # 身份证号
        "college": req_data["orgdn"],   # 所在学院
        "phone": req_data["phone"],     # 联系电话
        "email": req_data["email"]      # 电子邮箱
    }
    return json.dumps(res_data, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
