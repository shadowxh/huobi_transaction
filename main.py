#coding=utf-8

'''
本程序在 Python 3.3.0 环境下测试成功
使用方法：python HuobiMain.py
'''

from Util import *
import huobi
import json
import os
import time

def get_money_in_order():
    orders=json.loads(huobi.getOrders(1,GET_ORDERS));
    if len(orders)==0:return 0;
    return float(orders[0]["order_amount"])-float(orders[0]["processed_amount"]);

def get_id_of_order():
    orders=json.loads(huobi.getOrders(1,GET_ORDERS));
    if len(orders)==0:return -1;
    return orders[0]["id"];

def get_all_money():
    acc_info=json.loads(huobi.getAccountInfo(ACCOUNT_INFO));
    return acc_info["available_cny_display"];

def get_all_btc():
    acc_info=json.loads(huobi.getAccountInfo(ACCOUNT_INFO));
    return acc_info["available_btc_display"];
 
def get_cur_price():
    try_count=0;
    while True:
        r=requests.get(url='http://api.huobi.com/staticmarket/ticker_btc_json.js')
        try_count+=1;
        if r.status_code==200:
            ret=json.loads(r.text)
            return (ret["ticker"]["last"])
        if try_count>20:
            print("can't get current price of BTC,will quit soon!");
            os._exit();

def buy_retry(buy_price,buy_num):
    try_count=0;
    while True:
        buy_ret=json.loads(huobi.buy(1,str(buy_price),str(buy_num),None,None,BUY));
        try_count+=1;
        if "result" not in buy_ret:
            print("buy_ret:\n",buy_ret);
            os._exit(0);
        if buy_ret["result"]=="success":
            print("[buy] price:",buy_price," btc_num:",buy_num);
            return buy_ret["id"];
        if try_count>5:
            print("can't buy,will quit soon!");
            os._exit(0);

def sell_retry(sell_price,sell_num):
    try_count=0;
    while True:
        sell_ret=json.loads(huobi.sell(1,str(sell_price),str(sell_num),None,None,SELL));
        try_count+=1;
        if "result" not in sell_ret:
            print("sell_ret:\n",sell_ret);
            os._exit(0);
        if sell_ret["result"]=="success":
            print("[sell] price:",sell_price," btc_num:",sell_num);
            return buy_ret["id"];
        if try_count>5:
            print("can't sell,will quit soon!");
            os._exit(0);

if __name__ == "__main__":
    cost_cny=99.16;
    trans_cnt=0; 
    have_buy=1;
    try:
        while trans_cnt<5:
            time.sleep(0.1);
            if have_buy==0:
                cur_price=float(get_cur_price());
                if cur_price>float(os.environ["buy_price"]):
                    print("current price is larger than ",os.environ["buy_price"]);
                    continue;
                cur_price-=1;
                cost_cny=float(get_all_money());
                buy_num=cost_cny/cur_price;
                buy_num_round=round(buy_num,4);
                while buy_num_round>buy_num:
                    buy_num_round-=0.0001;
                buy_num=buy_num_round;
                if buy_num<0.001:continue;
                print("[before buy] cur_price:",cur_price," buy_num:",buy_num);
                buy_retry(cur_price,buy_num);
                not_processed=get_money_in_order();
                while not_processed!=0:
                    print("buy remain:",not_processed,"BTC");
                    not_processed=get_money_in_order();
                cost_cny=cur_price*buy_num;
                have_buy=1;
            else:
                print("ready to sell");
                print(cost_cny);
                cur_price=float(get_cur_price());
                my_btc=float(get_all_btc());
                my_btc_round=round(my_btc,4);
                while my_btc_round>my_btc:
                    my_btc_round-=0.0001;
                my_btc=my_btc_round;
                if my_btc<0.001:continue;
                print("all_btc:",my_btc);
                will_get_cny=my_btc*cur_price*(1.0-0.002);
                print("will_get_cny:",will_get_cny);
                print("diff(earn):",will_get_cny-cost_cny);
                if will_get_cny-cost_cny>0.5:
                    print("[before sell] cur_price:",cur_price," sell_num:",my_btc);
                    sell_retry(cur_price,my_btc);
                    not_processed=get_money_in_order();
                    while not_processed!=0:
                        print("sell remain:",not_processed,"BTC");
                        not_processed=get_money_in_order();
                    have_buy=0;
                    trans_cnt+=1;
    except Exception as e:
        print("exception raised");
        print(e);
"""
    print("number of orders:",get_cnt_of_orders());
    print(huobi.buy(1,"1","0.01",None,None,BUY))
    print("number of orders:",get_cnt_of_orders());
    print(huobi.cancelOrder(1,get_id_of_order(),CANCEL_ORDER));
    print("number of orders:",get_cnt_of_orders());
    #print (HuobiService.buy(1,"1","0.01",None,None,BUY))
	#print(HuobiService.get_cur());
    #print("获取k线");
    #HuobiService.get_kline("60min");
    #print ("获取账号详情")
    #print (HuobiService.getAccountInfo(ACCOUNT_INFO))
    #print ("获取所有正在进行的委托")
    #print (HuobiService.getOrders(1,GET_ORDERS))
"""
"""
    print ("获取订单详情")
    print (HuobiService.getOrderInfo(1,68278313,ORDER_INFO))
    print ("限价买入")
    print (HuobiService.buy(1,"1","0.01",None,None,BUY))
    print ("限价卖出")
    print (HuobiService.sell(2,"100","0.2",None,None,SELL))
    print ("市价买入")
    print (HuobiService.buyMarket(2,"30",None,None,BUY_MARKET))
    print ("市价卖出")
    print (HuobiService.sellMarket(2,"1.3452",None,None,SELL_MARKET))
    print ("查询个人最新10条成交订单")
    print (HuobiService.getNewDealOrders(1,NEW_DEAL_ORDERS))
    print ("根据trade_id查询order_id")
    print (HuobiService.getOrderIdByTradeId(1,274424,ORDER_ID_BY_TRADE_ID))
    print ("取消订单接口")
    print (HuobiService.cancelOrder(1,68278313,CANCEL_ORDER))
"""

