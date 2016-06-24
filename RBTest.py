#-*- coding:utf-8 -*-
from WindPy import *
import csv

with open('E:/中证500zigzag.csv',newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    Date = []
    ZigZag = []
    RBData = []
    for row in reader:
        Date.append(row[0])
        ZigZag.append(row[5])
        RBData.append([row[1],row[2],row[3],row[4]])

Direction = 0 #0向下，1向上
TurnUpDate = []
TurnDownDate = []
TurnUpIndex = []
TurnDownIndex = []
i = 1
NowZigZag = ZigZag[0]
while i<len(ZigZag):
    if (Direction==0):
        if ZigZag[i]>NowZigZag:
            Direction = 1
            TurnUpDate.append(Date[i - 1])
            TurnUpIndex.append(i-1)
        else:
            NowZigZag = ZigZag[i]
    if (Direction==1):
        if ZigZag[i]<NowZigZag:
            Direction = 0
            TurnDownDate.append(Date[i - 1])
            TurnDownIndex.append(i-1)
        else:
            NowZigZag = ZigZag[i]
    i = i + 1

f = open("E:/zz500zigzag.csv","w")
for i in range(len(TurnDownDate)):
    f.write("%s %s\n"%(TurnUpDate[i],TurnDownDate[i]))
f.close()


CurIndex = "CI005005.WI"

w.start()

RBReturn = []
CIReturn = []
SZ50Return = []
ZZ500Return = []
HS300Return = []
forcount = min(len(TurnUpDate),len(TurnDownDate))
for i in range(forcount):
    CurRBOpen = RBData[TurnUpIndex[i]][3]
    CurRBClose = RBData[TurnDownIndex[i]][3]
    CurRBReturn = float(CurRBClose)/float(CurRBOpen) - 1
    CurCIOpen = w.wsd("CI005005.WI", "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    CurCIClose = w.wsd("CI005005.WI", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurSZOpen = w.wsd("000016.SH", "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    CurSZClose = w.wsd("000016.SH", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurZZOpen = w.wsd("399905.SZ", "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    CurZZClose = w.wsd("399905.SZ", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurHSOpen = w.wsd("399300.SZ", "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    CurHSClose = w.wsd("399300.SZ", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurCIReturn = CurCIClose/CurCIOpen - 1
    CurSZReturn = CurSZClose/CurSZOpen - 1
    CurZZReturn = CurZZClose/CurZZOpen - 1
    CurHSReturn = CurHSClose/CurHSOpen - 1
    RBReturn.append(CurRBReturn)
    CIReturn.append(CurCIReturn)
    SZ50Return.append(CurSZReturn)
    ZZ500Return.append(CurZZReturn)
    HS300Return.append(CurHSReturn)

    CurRBOpen = RBData[TurnDownIndex[i]][3]
    CurRBClose = RBData[TurnUpIndex[i+1]][3]
    CurRBReturn = float(CurRBClose) / float(CurRBOpen) - 1
    CurCIOpen = w.wsd("CI005005.WI", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurCIClose = w.wsd("CI005005.WI", "close", TurnUpDate[i+1], TurnUpDate[i+1], "").Data[0][0]
    CurSZOpen = w.wsd("000016.SH", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurSZClose = w.wsd("000016.SH", "close", TurnUpDate[i+1], TurnUpDate[i+1], "").Data[0][0]
    CurZZOpen = w.wsd("399905.SZ", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurZZClose = w.wsd("399905.SZ", "close", TurnUpDate[i+1], TurnUpDate[i+1], "").Data[0][0]
    CurHSOpen = w.wsd("399300.SZ", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CurHSClose = w.wsd("399300.SZ", "close", TurnUpDate[i+1], TurnUpDate[i+1], "").Data[0][0]
    CurCIReturn = CurCIClose/CurCIOpen - 1
    CurSZReturn = CurSZClose/CurSZOpen - 1
    CurZZReturn = CurZZClose/CurZZOpen - 1
    CurHSReturn = CurHSClose/CurHSOpen - 1
    RBReturn.append(CurRBReturn)
    CIReturn.append(CurCIReturn)
    SZ50Return.append(CurSZReturn)
    ZZ500Return.append(CurZZReturn)
    HS300Return.append(CurHSReturn)

    print(i)

f = open("E:/钢.txt","w")
i = 0
while i<len(TurnDownDate):
    f.write("%s %s "%(TurnUpDate[i],TurnDownDate[i]))
    f.write("%.3f %.3f %.3f %.3f %.3f\n"%(RBReturn[i*2]*100,CIReturn[i*2]*100,SZ50Return[i*2]*100,HS300Return[i*2]*100,ZZ500Return[i*2]*100))
    f.write("%s %s "%(TurnDownDate[i],TurnUpDate[i+1]))
    f.write("%.3f %.3f %.3f %.3f %.3f\n"%(RBReturn[i*2+1]*100,CIReturn[i*2+1]*100,SZ50Return[i*2+1]*100,HS300Return[i*2+1]*100,ZZ500Return[i*2+1]*100))
    i = i + 1
f.close()


'''PortfolioReturn = []
ZZ500Return = []
CIReturn = []
forcount = min(len(TurnUpDate),len(TurnDownDate))
for i in range(forcount):
    StockList = w.wset("sectorconstituent", "date="+TurnUpDate[i]+";windcode="+CurIndex).Data[1] #获取第i个上涨期时的中证500成份股
    StockListStr = ""
    for j in range(len(StockList)-1):
        StockListStr = StockListStr + StockList[j] + ","
    StockListStr = StockListStr + StockList[len(StockList)-1]

    MarketValue = w.wsd(StockListStr, "mkt_cap_ashare", TurnUpDate[i], TurnUpDate[i], "").Data[0]
    TotalMarketValue = 0
    for j in range(len(StockList)):
        TotalMarketValue = TotalMarketValue + MarketValue[j]

    Industry = w.wsd(StockListStr,"industry_sw",TurnUpDate[i],TurnUpDate[i],"industryType=1").Data[0] #取得在TurnUpDate[i]当天成份股所属的板块
    IndustryTypes = []
    for j in range(len(StockList)):
        flag = True
        for k in range(len(IndustryTypes)):
            if IndustryTypes[k] == Industry[j]:
                flag = False
        if flag == True:
            IndustryTypes.append(Industry[j])

    IndustryWeight = [] #板块权重，以该板块全部股票占总市值之比来决定
    Portfolio = [] #在该次上涨期中要投资的股票，约250只；数组存放的是在StockList中的下标
    StockWeight = [] #在该次上涨期中要投资的股票的对应权重，合计为1
    for k in range(len(IndustryTypes)):
        section = []
        for j in range(len(StockList)):
            if Industry[j]==IndustryTypes[k]: #当前这支股票属于当前考查的板块
                section.append(j) #section存放当前板块即IndustryTypes[k]中的股票

        sectionvalue = 0
        for j in range(len(section)):
            sectionvalue = sectionvalue + MarketValue[section[j]]
        IndustryWeight.append(sectionvalue/TotalMarketValue)

        value = []
        for j in range(len(section)): #section中存放了当前板块股票在Industry中的下标，MarketValue[section[j]]即是对应的当时A股流通市值
            value.append(MarketValue[section[j]])

        for x in range(len(section)): #对MarketValue进行排序，同时改变section存放
            MinValue = value[x]
            MinX = x
            for y in range(x,len(section),1):
                if value[y]<MinValue:
                    MinValue = value[y]
                    MinX = y
            temp = value[x]
            value[x] = value[MinX]
            value[MinX] = temp
            temp = section[x]
            section[x] = section[MinX]
            section[MinX] = temp

        HalfSectionValue = 0
        for x in range(round(len(section)/2)): #取前一半股票
            HalfSectionValue = HalfSectionValue + MarketValue[section[x]]
        for x in range(round(len(section)/2)):
            Portfolio.append(section[x])
            StockWeight.append(MarketValue[section[x]]/HalfSectionValue*IndustryWeight[k]) #该股在这半段股票中的权重，乘以板块总体的权重，得到最终权重


        HalfSectionValue = 0
        for x in range(round(len(section)/2),len(section),1):
            HalfSectionValue = HalfSectionValue + MarketValue[section[x]]
        for x in range(round(len(section) / 2), len(section), 1):
            Portfolio.append(section[x])
            #StockWeight.append(MarketValue[section[x]]/HalfSectionValue*IndustryWeight[k]) #该股在这半段股票中的权重，乘以板块总体的权重，得到最终权重
        TotalHalfValue = 0
    for j in range(len(Portfolio)):
        TotalHalfValue = TotalHalfValue + MarketValue[Portfolio[j]]
    for j in range(len(Portfolio)):
        StockWeight.append(MarketValue[Portfolio[j]]/TotalHalfValue)

    #PercentChange = w.wss(StockListStr,"pct_chg_per","startDate="+TurnUpDate[i]+";endDate="+TurnDownDate[i]).Data[0]
    InitClose = w.wsd(StockListStr, "close", TurnUpDate[i],TurnUpDate[i],"PriceAdj=F").Data[0]
    FinalClose = w.wsd(StockListStr, "close", TurnDownDate[i],TurnDownDate[i],"PriceAdj=F").Data[0]
    PortfolioReturn.append(0)
    for j in range(len(Portfolio)):
        PortfolioReturn[i] = PortfolioReturn[i] + (FinalClose[Portfolio[j]]/InitClose[Portfolio[j]]-1)*StockWeight[j]
        #PortfolioReturn[i] = PortfolioReturn[i] + PercentChange[j]*StockWeight[j]

    InitIndexClose = w.wsd(CurIndex, "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    FinalIndexClose = w.wsd(CurIndex, "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    #IndexPercentChange = w.wss(CurIndex, "pct_chg_per","startDate="+TurnUpDate[i]+";endDate="+TurnDownDate[i]).Data[0][0]
    ZZ500Return.append((FinalIndexClose/InitIndexClose)-1)
    #ZZ500Return.append(IndexPercentChange)
    CIInitIndexClose = w.wsd("CI005027.WI", "close", TurnUpDate[i], TurnUpDate[i], "").Data[0][0]
    CIFinalIndexClose = w.wsd("CI005027.WI", "close", TurnDownDate[i], TurnDownDate[i], "").Data[0][0]
    CIReturn.append((CIFinalIndexClose/CIInitIndexClose)-1)

f = open("E:/result.txt","w")
for i in range(len(PortfolioReturn)):
    f.write("%s %s "%(TurnUpDate[i],TurnDownDate[i]))
    f.write("%.3f %.3f %.3f\n" % (PortfolioReturn[i]*100, ZZ500Return[i]*100,CIReturn[i]*100))
f.close()'''


