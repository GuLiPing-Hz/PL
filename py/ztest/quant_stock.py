#python 3.6

#pip install pandas
#pip install lxml

#根据提示语 安装缺少的模块
#pip install requests
#pip install bs4
#pip install tushare

import tushare
import numpy as np

class QuantOrder(object):
	"""docstring for QuantOrder"""
	def __init__(self):
		super(QuantOrder, self).__init__()
		
class QuantAccountData(object):
	def __init__(self):
		""" 
			构造函数 
		"""

class QuantUserData(object):
	def __init__(self):
		""" 
			构造函数 
		"""
		
class QuantStockContext(object):
	def __init__(self,start,end,frequency):
		""" 
			构造函数 
		"""
		#开始日期 format：YYYY-MM-DD 为空时取上市首日
		self.start_time= start 

		#结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
		self.end_time= end

		#数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
		self.frequency = frequency

		#自定义数据
		self.user_data = QuantUserData()
		print("self.user_data =",id(self.user_data))

		self.account = QuantAccountData()

		self.account_initial = QuantAccountData()

		self.order = QuantOrder()

STOCK_FLOAT = 0.001
def stock_buy(name,price,cash):
    count = int(cash/price//100*100)
    if(count > 100):
        #直接认为买入成功 价格+误差
        buy_money = (price+STOCK_FLOAT)*count
        fee = context.account.commission*buy_money #佣金
        if(fee < context.account.commission_base):
            fee = context.account.commission_base
        
        context.account.money -= buy_money #减去买入金额
        context.account.money -= fee #减去费用
        context.account.stock += count;
        print("买入["+name+"]成功 剩余现金 =",context.account.money,",持有股票 =",context.account.stock
            ,"成交额 =",buy_money,"总费用 =",fee,"印花税 =",0);
    else:
        print("买入["+name+"]失败 现金不足买入一手!!!")

def stock_sell(name,price,count):
    #直接认为买入成功 价格-误差
    sell_money = (price-STOCK_FLOAT)*count
    fee = context.account.commission*sell_money #佣金
    if(fee < context.account.commission_base):
        fee = context.account.commission_base
    fee1 = context.account.tax*sell_money #印花税
    fee += fee1
    
    context.account.money += sell_money #加上卖出金额
    context.account.money -= fee #减去费用
    context.account.stock -= count;
    print("卖出["+name+"]成功 剩余现金 =",context.account.money,",持有股票 =",context.account.stock
        ,"成交额 =",sell_money,"总费用 =",fee,"印花税 =",fee1);

def summarize(price):
    curTotal = context.account.money+context.account.stock*price
    orignTotal = context.account_initial.money
    orignPrice = context.account_initial.price_start
    print("当前我的资产总价值 money = ",curTotal,"策略收益 ="
        ,str((curTotal-orignTotal)/orignTotal*100)+"%","基准收益 = "
        ,str((price-orignPrice)/orignPrice*100)+"%");

#开始日期 format：YYYY-MM-DD 为空时取上市首日
#结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
#数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
context = QuantStockContext("","","D") #2015-08-10

context.order.buy = stock_buy
context.order.sell = stock_sell
context.summarize = summarize

context.security = "159915"
#print("context.user_data =",id(context.user_data))

context.account_initial.money = 10000 #起始持有RMB数量
context.account_initial.stock = 0   #起始持有股票数量
context.account.commission = 0.00025 #万二点五佣金
context.account.commission_base = 5  #佣金最低额
context.account.tax = 0.001          #印花税  交易上海的股票需要过户费,我暂且忽略过户费

# 设置ATR值回看窗口
context.user_data.T = 20 # >= 1

#认为未来将上涨
#设置买入atr倍数
context.user_data.BuyAtr = 0.5
#设置卖出atr倍数
context.user_data.SellAtr = 2#4#3.6

context.user_data.BuyUnit = 0.01

context.user_data.IsFirstInHandle = True

def init_local_context(context):
    # 上一次买入价
    context.user_data.last_buy_price = 0
    # 是否持有头寸标志
    context.user_data.hold_flag = False#context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
    # 限制最多买入的单元数
    context.user_data.limit_unit = 4
    # 现在买入1单元的security数目
    context.user_data.unit = 0
    # 买入次数
    context.user_data.add_time = 0

# 用户自定义的函数，可以被handle_data调用: 唐奇安通道计算及判断入场离场
# data是日线级别的历史数据，price是当前分钟线数据（用来获取当前行情），T代表需要多少根日线
def in_or_out(context, data, price, T):
    up = np.max(data["high"].iloc[-T:])
    # 这里是T/2唐奇安下沿，在向下突破T/2唐奇安下沿卖出而不是在向下突破T唐奇安下沿卖出，这是为了及时止损
    down = np.min(data["low"].iloc[-int(T / 2):])
    print("当前价格为: %s, 唐奇安上轨为: %s, 唐奇安下轨为: %s" % (price, up, down))
    # 当前价格升破唐奇安上沿，产生入场信号
    if price > up:
        print("价格突破唐奇安上轨")
        return 1
    # 当前价格跌破唐奇安下沿，产生出场信号
    elif price < down:
        print("价格跌破唐奇安下轨")
        return -1
    # 未产生有效信号
    else:
        print("价格未产生有效信号")
        return 0

# 用户自定义的函数，可以被handle_data调用
# 判断是否加仓或止损:当价格相对上个买入价上涨 0.5ATR时，再买入一个unit; 当价格相对上个买入价下跌 2ATR时，清仓
def add_or_stop(price, lastprice, atr, context):
    buyArtPrice = lastprice + context.user_data.BuyAtr * atr
    sellArtPrice = lastprice - context.user_data.SellAtr * atr
    if price >= buyArtPrice:
        print("当前价格比上一个购买价格上涨超过"+str(context.user_data.BuyAtr)+"个ATR("+str(buyArtPrice)+")")
        return 1
    elif price <= sellArtPrice:
        print("当前价格比上一个购买价格下跌超过"+str(context.user_data.SellAtr)+"个ATR("+str(sellArtPrice)+")")
        return -1
    else:
        print("当前价格在我们的波动返回内("+str(sellArtPrice)+"~"+str(buyArtPrice)+")")
        return 0

# 用户自定义的函数，可以被handle_data调用：ATR值计算
def calc_atr(data):  # data是日线级别的历史数据
    tr_list = []
    for i in range(len(data)):
        tr = max(data["high"].iloc[i] - data["low"].iloc[i], data["high"].iloc[i] - data["close"].iloc[i - 1],
                 data["close"].iloc[i - 1] - data["low"].iloc[i])
        tr_list.append(tr)
    atr = np.array(tr_list).mean()
    return atr

# 用户自定义的函数，可以被handle_data调用
# 计算unit
def calc_unit(per_value, atr):
    return per_value / atr

def handle_data(context,k_data):
    print("进入处理函数")
    
    #print(context.account)
    # if context.user_data.IsFirstInHandle:
    #     context.user_data.hold_flag = context.account_initial.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
    #     #print(str(context.account_initial.huobi_cny_btc)+";"+str(context.account.huobi_cny_btc))
    #     context.user_data.IsFirstInHandle = False
        
    
    # 获取历史数据
    hist = k_data #DataFrame
    #print("hist.index=",hist.index)

    # 获取当前行情数据
    hist_end_data = hist.iloc[len(hist)-1]
    #print("hist_end_data =\n",hist_end_data)
    #print("hist_end_data.open =",hist_end_data.open);
    price = hist_end_data.close

    if len(hist.index) < (context.user_data.T + 1):
        print("bar的数量不足, 等待下一根bar...")
    else:
        # 1 计算ATR
        atr = calc_atr(hist.iloc[:len(hist)-1])
        print("art = ",atr)

        # 2 判断加仓或止损
        if context.user_data.hold_flag is True and context.account.stock > 0:  # 先判断是否持仓
            print("判断是加仓还是止损")
            temp = add_or_stop(price, context.user_data.last_buy_price, atr, context)
            if temp == 1:  # 判断加仓
                if context.user_data.add_time < context.user_data.limit_unit:  # 判断加仓次数是否超过上限
                    print("产生加仓信号")
                    print("min("+str(context.account.money)+","+str(context.user_data.unit)+"*"+str(price))
                    cash_amount = min(context.account.money, context.user_data.unit * price)  # 不够1 unit时买入剩下全部

                    context.user_data.last_buy_price = price
                    context.user_data.add_time += 1
                    print("正在买入 "+context.security+" ;下单金额为 "+str(cash_amount)+" 元")
                    context.order.buy(context.security,price, cash_amount)
                else:
                    print("加仓次数已经达到上限，不会加仓")
            elif temp == -1:  # 判断止损
                # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
                init_local_context(context)
                # 卖出止损
                print("产生止损信号;正在卖出 "+str(context.security)+";卖出数量为 "+str(context.account.stock))
                context.order.sell(context.security,price, context.account.stock)
        # 3 判断入场离场
        else:
            print("判断是进场还是离场")
            out = in_or_out(context, hist.iloc[:len(hist) - 1], price, context.user_data.T)
            if out == 1:  # 入场
                if context.user_data.hold_flag is False:
                    print("账户余额money = "+str(context.account.money)+",art="+str(atr))
                    value = context.account.money * context.user_data.BuyUnit
                    context.user_data.unit = calc_unit(value, atr)
                    print("入场单元 context.user_data.unit="+str(context.user_data.unit)+"*"+str(price))
                    context.user_data.add_time = 1
                    context.user_data.hold_flag = True
                    context.user_data.last_buy_price = price
                    cash_amount = min(context.account.money, context.user_data.unit * price)
                    # 有买入信号，执行买入
                    print("产生入场信号;正在买入 " + context.security + " ;下单金额为 "+str(cash_amount)+" 元")

                    context.order.buy(context.security,price, cash_amount)
                else:
                    print("已经入场，不产生入场信号")
            elif out == -1:  # 离场
                if context.account.stock >= 0: #context.user_data.hold_flag is True
                    # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
                    init_local_context(context)
                    # 有卖出信号，且持有仓位，则市价单全仓卖出
                    print("产生止盈离场信号;正在卖出 " + context.security + " ;卖出数量为 "+str(context.account.stock))
                    context.order.sell(context.security,price, context.account.stock)
                else:
                    print("尚未入场或已经离场，不产生离场信号")

    context.summarize(price)
    print("进入处理函数 end")

def main():

    #初始化我的账户钱和股票数量
    context.account.money = context.account_initial.money
    context.account.stock = context.account_initial.stock
    init_local_context(context)

    print("tushare version =",tushare.__version__)
    print("*"*100)

    k_data = tushare.get_k_data(context.security,start=context.start_time, end=context.end_time,ktype=context.frequency)
    #print(k_data)
    #print(type(k_data))
    #print(len(k_data))

    k_data_start = k_data.iloc[0]
    # print(k_data_start)
    context.account_initial.price_start = k_data_start.open
    print("first open =",context.account_initial.price_start)

    needCount = context.user_data.T+1
    # print("needCount =",needCount)
    # print(k_data[0:needCount])
    for i in range(len(k_data)):
        # print("i",i)
        k_data_seg = []

        if i < needCount:
            k_data_seg = k_data[0:i];
        else:
            k_data_seg = k_data[i-needCount:i];

        if len(k_data_seg) != 0:
            handle_data(context,k_data_seg)

if __name__ == '__main__':
	main()
