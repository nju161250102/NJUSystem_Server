# -*- coding:utf-8 -*-
from peewee import *

db = SqliteDatabase('alipay.db')


class AliPay(Model):
    trade_number = CharField()
    order_number = CharField()
    create_time = DateTimeField()
    pay_time = DateTimeField()
    modify_time = DateTimeField()
    source = CharField()
    type = CharField()
    target = CharField()
    name = CharField()
    money = DoubleField()
    flag = IntegerField()
    trade_state = CharField()
    fee = DoubleField()
    money_back = DoubleField()
    remark = CharField()
    money_state = DoubleField()
    first_type = CharField()
    second_type = CharField()

    @staticmethod
    def from_row(row):
        return AliPay(
            trade_number=row["交易号"].strip(),
            order_number=row["商家订单号"].strip(),
            create_time=row["交易创建时间"].strip(),
            pay_time=row["付款时间"].strip(),
            modify_time=row["最近修改时间"].strip(),
            source=row["交易来源地"].strip(),
            type=row["类型"].strip(),
            target=row["交易对方"].strip(),
            name=row["商品名称"].strip(),
            money=row["金额（元）"],
            flag=row["收/支"].strip(),
            trade_state=row["交易状态"].strip(),
            fee=row["服务费（元）"],
            money_back=row["成功退款（元）"],
            remark=row["备注"].strip(),
            money_state=row["资金状态"].strip())

    class Meta:
        database = db
