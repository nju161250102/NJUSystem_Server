# coding=utf-8
import os
import sqlite3
import pandas as pd
from model import AliPay


def classify(item: AliPay):
    if item.money_state == "" or item.money_state == "冻结":
        return "无效交易", ""
    if "余额宝-" in item.name and "-收益发放" in item.name:
        return "理财", "余额宝收益"
    if "蚂蚁财富-" in item.target:
        if item.flag == "收入":
            return "理财", "基金购买"
        else:
            return "理财", "基金赎回"
    if "博时黄金" in item.target:
        if item.flag == "收入":
            return "理财", "黄金购买"
        else:
            return "理财", "黄金卖出"
    if item.target in ["中国工商银行", "网商银行"]:
        return "转账", "转账到银行卡"
    if "淘宝" in item.source:
        return "消费", "淘宝"
    if "中国铁路" in item.target:
        return "消费", "火车票"
    if "车巴达" in item.target:
        return "消费", "汽车票"
    if "定期理财" in item.name and item.flag == "支出":
        return "理财", "定期购买"
    if "理财赎回" in item.name and item.flag == "收入":
        return "理财", "定期赎回"
    if item.source == "支付宝网站" and item.type == "即时到账交易" and item.money_state != "资金转移":
        if item.target in ["支付宝推荐赏金", "红包推荐奖励"]:
            return "收入", "推荐奖励"
        if item.target in ["蚂蚁财富", "支付宝五福的红包"]:
            return "收入", "活动奖励"
        if "自来水" in item.target:
            return "消费", "水费"
        if item.flag == "收入":
            return "转账", "转入"
        else:
            return "转账", "转出"
    if "其他" in item.source:
        if "超市" in item.target or "超市" in item.name:
            return "消费", "超市"
        if "小天鹅" in item.target:
            return "消费", "洗衣"

    return "其他", ""


def main():
    #
    conn = sqlite3.connect('alipay.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS alipay;")
    c.execute('''
    CREATE TABLE alipay (
        trade_number TEXT DEFAULT NULL,
        order_number TEXT DEFAULT NULL,
        create_time TIMESTAMP DEFAULT NULL,
        pay_time TIMESTAMP DEFAULT NULL,
        modify_time TIMESTAMP DEFAULT NULL,
        source TEXT DEFAULT NULL,
        type TEXT DEFAULT NULL,
        target TEXT DEFAULT NULL,
        name TEXT DEFAULT NULL,
        money REAL DEFAULT NULL,
        flag INTEGER DEFAULT NULL,
        trade_state TEXT DEFAULT NULL,
        fee REAL DEFAULT NULL,
        money_back REAL DEFAULT NULL,
        remark TEXT DEFAULT NULL,
        money_state REAL DEFAULT NULL,
        first_type TEXT DEFAULT '',
        second_type TEXT DEFAULT '');
    ''')
    # 读取文件
    df = pd.read_csv("D:/alipay_record.csv", encoding="gbk")
    # 去掉列名后面的空格
    columns_dict = {}
    for i in range(len(df.columns)):
        columns_dict[df.columns[i]] = df.columns[i].strip()
    df = df.rename(columns=columns_dict)
    #
    for index, row in df.iterrows():
        print(row["交易号"])
        item = AliPay.from_row(row)
        item.first_type, item.second_type = classify(item)
        item.save()


if __name__ == '__main__':
    main()
