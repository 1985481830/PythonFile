from WindPy import *
import datetime

w.start()

dat = []
for x in range(1,13):
    if x < 10:
        dat.append('0'+str(x))
    else:
        dat.append(str(x))

LastTradeDay = []
for x in range(5,13):
    L = w.wsd("IC15"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,8):
    L = w.wsd("IC16"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)

BeginDate = "2015-04-16"
EndDate = "2016-06-16"

IC00 = w.wsd("IC00.CFE", "close", BeginDate, EndDate, "").Data[0]
IC01 = w.wsd("IC01.CFE", "close", BeginDate, EndDate, "").Data[0]
IC02 = w.wsd("IC02.CFE", "close", BeginDate, EndDate, "").Data[0]
IC03 = w.wsd("IC03.CFE", "close", BeginDate, EndDate, "").Data[0]
ZZ500 = w.wsd("399905.SZ", "open,high,low,close", BeginDate, EndDate, "")
ZZ500O = ZZ500.Data[0]
ZZ500H = ZZ500.Data[1]
ZZ500L = ZZ500.Data[2]
ZZ500C = ZZ500.Data[3]
Dat = []
for x in range(len(ZZ500.Times)):
    Dat.append(ZZ500.Times[x])

SignIC = []

for x in range(1,len(ZZ500.Times),1):
    flag = True

    '''if ZZ500C[x]/ZZ500C[x-1]>1.005: #阳线且涨了0.5%就过滤
        flag = False
    if ((min(ZZ500O[x],ZZ500C[x])-ZZ500L[x])/(abs(ZZ500C[x]-ZZ500O[x])))<2: #下影线长度不到实体的2倍就过滤
        flag = False'''

    if ZZ500C[x]>ZZ500O[x]:
        flag = False

    if flag == True:
        basisToday = IC00[x]-ZZ500C[x]
        basisLastday = IC00[x-1]-ZZ500C[x-1]
        if (basisToday - basisLastday)<30:
            flag = False
        else:
            if abs((basisToday - basisLastday)/basisLastday) < 0.3:
                flag = False

    if IC00[x]<IC00[x-1] or IC01[x]<IC01[x-1] or IC02[x]<IC02[x-1] or IC03[x]<IC03[x-1]:
        flag = False

    if flag == True:
        for i in range(len(LastTradeDay)):
            if abs((Dat[x]-LastTradeDay[i]).days)<=2:
                flag = False

    if flag == True:
        SignIC.append(ZZ500.Times[x].strftime("%Y-%m-%d"))

#沪深300

LastTradeDay = []
for x in range(5,13):
    L = w.wsd("IF10"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,13):
    L = w.wsd("IF11"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,13):
    L = w.wsd("IF12"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,13):
    L = w.wsd("IF13"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,13):
    L = w.wsd("IF14"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,13):
    L = w.wsd("IF15"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)
for x in range(1,8):
    L = w.wsd("IF16"+dat[x-1]+".CFE", "lasttrade_date", "2016-03-01", "2016-03-01", "").Data[0][0]
    LastTradeDay.append(L)

BeginDate = "2010-04-16"
EndDate = "2016-06-16"

IF00 = w.wsd("IF00.CFE", "close", BeginDate, EndDate, "").Data[0]
IF01 = w.wsd("IF01.CFE", "close", BeginDate, EndDate, "").Data[0]
IF02 = w.wsd("IF02.CFE", "close", BeginDate, EndDate, "").Data[0]
IF03 = w.wsd("IF03.CFE", "close", BeginDate, EndDate, "").Data[0]
HS300 = w.wsd("399300.SZ", "open,high,low,close", BeginDate, EndDate, "")
HS300O = HS300.Data[0]
HS300H = HS300.Data[1]
HS300L = HS300.Data[2]
HS300C = HS300.Data[3]
Dat = []
for x in range(len(HS300.Times)):
    Dat.append(HS300.Times[x])

SignIF = []

for x in range(1,len(HS300.Times),1):
    flag = True

    '''if HS300C[x]/HS300C[x-1]>1.005: #阳线且涨了0.5%就过滤
        flag = False
    if ((min(HS300O[x],HS300C[x])-HS300L[x])/(abs(HS300C[x]-HS300O[x])))<2: #下影线长度不到实体的2倍就过滤
        flag = False'''

    if HS300C[x]>HS300O[x]:
        flag = False

    if flag == True:
        basisToday = IF00[x]-HS300C[x]
        basisLastday = IF00[x-1]-HS300C[x-1]
        if (basisToday - basisLastday)<30:
            flag = False
        else:
            if abs((basisToday - basisLastday)/basisLastday) < 0.3:
                flag = False

    if IF00[x]<IF00[x-1] or IF01[x]<IF01[x-1] or IF02[x]<IF02[x-1] or IF03[x]<IF03[x-1]:
        flag = False

    if flag == True:
        for i in range(len(LastTradeDay)):
            if abs((Dat[x]-LastTradeDay[i]).days)<=2:
                flag = False

    if flag == True:
        SignIF.append(HS300.Times[x].strftime("%Y-%m-%d"))

M = 3