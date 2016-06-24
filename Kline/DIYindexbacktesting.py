#-*- coding:utf-8 -*-
from WindPy import *
import csv

with open('E:/zz500.csv',newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    Date = []
    ZigZag = []
    for row in reader:
        Date.append(row[0])
        ZigZag.append(row[5])

Direction = 0 #0向下，1向上
TurnUpDate = []
TurnDownDate = []
i = 1
NowZigZag = ZigZag[0]
while i<len(ZigZag):
    if (Direction==0):
        if ZigZag[i]>NowZigZag:
            Direction = 1
            TurnUpDate.append(Date[i - 1])
        else:
            NowZigZag = ZigZag[i]
    if (Direction==1):
        if ZigZag[i]<NowZigZag:
            Direction = 0
            TurnDownDate.append(Date[i - 1])
        else:
            NowZigZag = ZigZag[i]
    i = i + 1

#TurnUpDate = ["20090105","20100104","20110104","20120104","20130104","20140102","20150105"]
#TurnDownDate = ["20091231","20101231","20111230","20121231","20131231","20141231","20151231"]
CurIndex = "399905.SZ"

w.start()

PortfolioReturn = []
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


        '''HalfSectionValue = 0
        for x in range(round(len(section)/2),len(section),1):
            HalfSectionValue = HalfSectionValue + MarketValue[section[x]]
        for x in range(round(len(section) / 2), len(section), 1):
            Portfolio.append(section[x])
            #StockWeight.append(MarketValue[section[x]]/HalfSectionValue*IndustryWeight[k]) #该股在这半段股票中的权重，乘以板块总体的权重，得到最终权重
        '''
    '''TotalHalfValue = 0
    for j in range(len(Portfolio)):
        TotalHalfValue = TotalHalfValue + MarketValue[Portfolio[j]]
    for j in range(len(Portfolio)):
        StockWeight.append(MarketValue[Portfolio[j]]/TotalHalfValue)'''

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
f.close()


