import math
from WindPy import *
w.start()

x = w.wsq("399905.SZ", "rt_time,rt_last")

a = 3


'''dates = w.wsd("000300.SH", "close", "2016-04-08", "2016-04-13", "").Times
for x in range(len(dates)):
    dates[x]=dates[x].strftime("%Y%m%d")

indexreturn = w.wsd("CI005027.WI", "pct_chg", "2016-04-08", "2016-04-13", "").Data[0]

f=open("E:/res.txt","w")

for x in range(len(dates)):
    cons = w.wset("indexconstituent","date="+dates[x]+";windcode=CI005027.WI").Data[1]
    stocklist = ""
    for i in range(len(cons)-1):
        stocklist = stocklist + cons[i]+","
    stocklist = stocklist + cons[len(cons)-1]
    vols = w.wsd(stocklist,"volume",dates[x],dates[x],"")
    pctchg = w.wsd(stocklist, "pct_chg", dates[x], dates[x], "")
    stockcount = 0
    totalr = 0
    for i in range(len(cons)):
        flag = True
        if math.isnan(vols.Data[0][i]) == True:
            flag = False
        else:
            if vols.Data[0][i] < 0.00001:
                flag = False
        if flag == True:
            stockcount = stockcount + 1
            totalr = totalr + pctchg.Data[0][i]
    r = totalr/stockcount
    print("%s %d %.3f %.3f"%(dates[x],stockcount,r,indexreturn[x]))
    f.write("%s %d %.3f %.3f"%(dates[x],stockcount,r,indexreturn[x]))

f.close()'''


'''stop = []
cons = w.wset("indexconstituent","date=20160104;windcode=CI005027.WI").Data[1]
stocklist = ""
for i in range(len(cons)-1):
    stocklist =stocklist + cons[i]+","
stocklist = stocklist + cons[len(cons)-1]

vols = w.wsd(stocklist, "volume", "2016-01-04", "2016-04-11", "")

for i in range(len(vols.Times)):
    count = 0
    for j in range(len(cons)):
        if vols.Data[j][i] < 0.00001:
            count = count + 1
    stop.append(count)

a = 0
for i in range(len(stop)):
    a = a + stop[i]
a = a/len(stop)'''



