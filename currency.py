from WindPy import *
import datetime
w.start()

HB = w.wsd("511990.SH", "open,close", "2013-04-18", "2016-04-13", "PriceAdj=F")

YH = w.wsd("511880.SH", "open,close", "2013-04-18", "2016-04-13", "PriceAdj=F")

dates = HB.Times
money = 10000000.0
stock = 0
status = True #持钱

f = open("F:/currency.txt","w")

for i in range(len(dates)):
    weekday =  dates[i].weekday()
    if i!=(len(dates)-1):
        nextdateweekday = dates[i+1].weekday()
    if (weekday == 0) and (status == True):
        f.write("%s 周%d买入华宝 价格%.3f %.3f\n" % (dates[i].strftime("%Y-%m-%d"), weekday + 1, HB.Data[0][i], money))
        stock = money / HB.Data[0][i]
        money = 0
        status = False
        continue
    if (weekday == 1) and (status == False) and (i!=(len(dates)-1)) and (nextdateweekday!=2):
        money = stock * HB.Data[1][i]
        stock = 0
        status = True
        f.write("%s 周%d卖出华宝 价格%.3f %.3f\n" % (dates[i].strftime("%Y-%m-%d"), weekday + 1, HB.Data[1][i],money))
        continue
    if (weekday == 2) and (status == False):
        money = stock * HB.Data[1][i]
        stock = 0
        status = True
        f.write("%s 周%d卖出华宝 价格%.3f %.3f\n" % (dates[i].strftime("%Y-%m-%d"), weekday + 1, HB.Data[1][i], money))
        continue
    if (weekday == 3) and (status == True):
        f.write("%s 周%d买入银华 价格%.3f %.3f\n" % (dates[i].strftime("%Y-%m-%d"), weekday + 1, YH.Data[0][i], money))
        stock = money / YH.Data[0][i]
        money = 0
        status = False
        continue
    if (weekday == 4) and (status == False):
        money = stock * YH.Data[1][i]
        stock = 0
        status = True
        f.write("%s 周%d卖出银华 价格%.3f %.3f\n" % (dates[i].strftime("%Y-%m-%d"), weekday + 1, YH.Data[1][i],money))
        continue

f.close()
