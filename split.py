import codecs
import math
from WindPy import *
import datetime
import os

def divseg(segment,denominator,signal):
    dsg = []
    if signal == "vol":
        for x in range(len(segment)):
            total = int(segment[x][2])
            single = math.ceil(total/(denominator*100))*100
            tempdsg = []
            i = 0
            while i<denominator:
                if total>single:
                    tempdsg.append(single)
                    total = total - single
                else:
                    tempdsg.append(total)
                    total = 0
                i = i + 1
            dsg.append(tempdsg)
    if signal == "amo":
        for x in range(len(segment)):
            total = float(segment[x][2])
            single = math.ceil(total/(denominator*100))*100
            tempdsg = []
            i = 0
            while i<denominator:
                if total > single:
                    tempdsg.append(single/float(segment[x][2])*float(segment[x][5]))
                    total = total - single
                else:
                    tempdsg.append(total/float(segment[x][2])*float(segment[x][5]))
                    total = 0
                i = i + 1
            dsg.append(tempdsg)
    return dsg

begindat = "20160504"
enddat = datetime.datetime.now().strftime("%Y%m%d") #取今天日期

#自定义参数
numtag = "可用股数" #当前余额，可用股数
type = "迅投" #CAT、迅投
#自定义参数

rawfilepath = "C:/"+type+".csv"

if type == "CAT":
    if numtag == "当前余额":
        tag = 4
    if numtag == "可用股数":
        tag = 5
if type == "迅投":
    if numtag == "当前余额":
        tag = 5
    if numtag == "可用股数":
        tag = 8

w.start()

codes = []
classes = []

dirpath = "C:/"+enddat+type+"/"
try:
    os.mkdir(dirpath)
except:
    pass

codes.append(['CI005005.WI'])
classes.append("钢铁")
codes.append(['CI005027.WI','884114.WI','884039.WI','884076.WI'])
classes.append("指数增强")

position = []
portfolio = []

if type == "CAT":
    f = codecs.open(rawfilepath,"r","utf-8")
    f.readline()
    while True:
        contents = f.readline()
        if not contents:
            break
        else:
            contents = contents.split("\r\n")[0]
            content = contents.split(",")
            if content[tag] != "0":
                position.append([content[1],content[2],content[tag],content[9],content[10],content[12],content[14]])
            #代码、名称、当前余额(可用股数)、成本价、现价、市值、盈亏
    f.close()

    bdat = datetime.datetime.strptime(begindat,"%Y%m%d")
    edat = datetime.datetime.strptime(enddat,"%Y%m%d")

    for x in range(len(codes)):
        tempportfolio = []
        for i in range(len(codes[x])):
            windcode = codes[x][i]
            dat = bdat
            while dat <= edat:
                single_index_portfolio = []
                rawdata = w.wset("sectorconstituent", "date=" + dat.strftime("%Y%m%d") + ";windcode=" + windcode)
                cons = []
                for j in range(len(rawdata.Data[1])):
                    cons.append(rawdata.Data[1][j][0:6])
                name = rawdata.Data[2]
                for j in range(len(cons)):
                    if not (cons[j] in tempportfolio):
                        single_index_portfolio.append(cons[j])
                for j in range(len(single_index_portfolio)):
                    tempportfolio.append(single_index_portfolio[j])
                dat = dat + datetime.timedelta(days = 1)
        tempportfolio.sort()
        portfolio.append(tempportfolio)

    for i in range(len(portfolio)):
        segment = []
        for x in range(len(position)):
            if position[x][0] in portfolio[i]:
                segment.append(position[x])

        if len(segment) == 0: #没这板块的股
            continue

        for denominator in range(1,5,1):
            divsegment = divseg(segment, denominator, "vol")
            divsegamo = divseg(segment, denominator, "amo")
            for numerator in range(1,denominator+1,1):
                filepath = dirpath+classes[i]+str(numerator)+"("+str(denominator)+")"+".csv"
                f = open(filepath,"w")
                for x in range(len(segment)-1):
                    f.write("%s,%s,%s,0,0,%s\n"%(segment[x][0],segment[x][1],divsegment[x][numerator-1],divsegamo[x][numerator-1]))
                x = len(segment)-1
                f.write("%s,%s,%s,0,0,%s"%(segment[x][0],segment[x][1],divsegment[x][numerator-1],divsegamo[x][numerator-1]))
                f.close()

        stocktotalamount = 0
        for x in range(len(segment)):
            stocktotalamount = stocktotalamount + float(segment[x][5])

        interval = 500000
        nominalinteral = 50
        nominalamount = 0
        curamount = 0
        while (curamount + interval) < stocktotalamount:
            curamount = curamount + interval
            nominalamount = nominalamount + nominalinteral
            divvol = []
            divamount = []
            ratio = curamount/stocktotalamount
            for k in range(len(segment)):
                volume = math.ceil(ratio*float(segment[k][2])/100)*100
                divvol.append(volume)
                divamount.append(volume/float(segment[k][2])*float(segment[k][5]))
            filepath = dirpath + classes[i] + str(nominalamount) +"万.csv"
            f = open(filepath,"w")
            for k in range(len(segment)-1):
                f.write("%s,%s,%s,0,0,%s\n"%(segment[k][0],segment[k][1],divvol[k],divamount[k]))
            k = len(segment)-1
            f.write("%s,%s,%s,0,0,%s"%(segment[k][0],segment[k][1],divvol[k],divamount[k]))
            f.close()

        curamount = stocktotalamount
        nominalamount = "全清"
        divvol = []
        divamount = []
        ratio = curamount / stocktotalamount
        for k in range(len(segment)):
            divvol.append(segment[k][2])
            divamount.append(segment[k][5])
        filepath = dirpath + classes[i] + str(nominalamount) + ".csv"
        f = open(filepath, "w")
        for k in range(len(segment) - 1):
            f.write("%s,%s,%s,0,0,%s\n" % (segment[k][0], segment[k][1], divvol[k],divamount[k]))
        k = len(segment) - 1
        f.write("%s,%s,%s,0,0,%s" % (segment[k][0],segment[k][1],divvol[k],divamount[k]))
        f.close()

if type == "迅投":
    f = open(rawfilepath,"r")
    f.readline()
    while True:
        contents = f.readline()
        if not contents:
            break
        else:
            contents = contents.split("\n")[0]
            content = contents.split(",")
            if content[tag] != "0":
                position.append([content[2],content[3],content[tag],content[10],content[11],str(float(content[tag])*float(content[11])),content[6]])
            #代码、名称、当前余额(可用股数)、成本价、现价、市值、盈亏
    f.close()

    bdat = datetime.datetime.strptime(begindat,"%Y%m%d")
    edat = datetime.datetime.strptime(enddat,"%Y%m%d")

    for x in range(len(codes)):
        tempportfolio = []
        for i in range(len(codes[x])):
            windcode = codes[x][i]
            dat = bdat
            while dat <= edat:
                single_index_portfolio = []
                rawdata = w.wset("sectorconstituent", "date=" + dat.strftime("%Y%m%d") + ";windcode=" + windcode)
                cons = []
                for j in range(len(rawdata.Data[1])):
                    cons.append(rawdata.Data[1][j][0:6])
                name = rawdata.Data[2]
                for j in range(len(cons)):
                    if not (cons[j] in tempportfolio):
                        single_index_portfolio.append(cons[j])
                for j in range(len(single_index_portfolio)):
                    tempportfolio.append(single_index_portfolio[j])
                dat = dat + datetime.timedelta(days = 1)
        tempportfolio.sort()
        portfolio.append(tempportfolio)

    for i in range(len(portfolio)):
        segment = []
        for x in range(len(position)):
            if position[x][0] in portfolio[i]:
                segment.append(position[x])

        if len(segment) == 0: #没这板块的股
            continue

        for denominator in range(1,5,1):
            divsegment = divseg(segment, denominator, "vol")
            divsegamo = divseg(segment, denominator, "amo")
            for numerator in range(1,denominator+1,1):
                filepath = dirpath+classes[i]+str(numerator)+"("+str(denominator)+")"+".csv"
                f = open(filepath,"w")
                for x in range(len(segment)-1):
                    if numtag == "当前余额":
                        f.write("%s,%s,%s,0,0,%s\n"%(segment[x][0],segment[x][1],divsegment[x][numerator-1],divsegamo[x][numerator-1]))
                    if numtag == "可用股数":
                        f.write("%s,%s,%s,1,1\n"%(segment[x][0],segment[x][1],divsegment[x][numerator-1]))
                x = len(segment)-1
                if numtag == "当前余额":
                    f.write("%s,%s,%s,0,0,%s"%(segment[x][0],segment[x][1],divsegment[x][numerator-1],divsegamo[x][numerator-1]))
                if numtag == "可用股数":
                    f.write("%s,%s,%s,1,1"%(segment[x][0],segment[x][1],divsegment[x][numerator-1]))
                f.close()

        stocktotalamount = 0
        for x in range(len(segment)):
            stocktotalamount = stocktotalamount + float(segment[x][5])

        interval = 500000
        nominalinteral = 50
        nominalamount = 0
        curamount = 0
        while (curamount + interval)< stocktotalamount:
            curamount = curamount + interval
            nominalamount = nominalamount + nominalinteral
            divvol = []
            divamount = []
            ratio = curamount/stocktotalamount
            for k in range(len(segment)):
                volume = math.ceil(ratio*float(segment[k][2])/100)*100
                divvol.append(volume)
                divamount.append(volume/float(segment[k][2])*float(segment[k][5]))
            filepath = dirpath + classes[i] + str(nominalamount) +"万.csv"
            f = open(filepath,"w")
            for k in range(len(segment)-1):
                if numtag == "当前余额":
                    f.write("%s,%s,%s,0,0,%s\n"%(segment[k][0],segment[k][1],divvol[k],divamount[k]))
                if numtag == "可用股数":
                    f.write("%s,%s,%s,1,1\n" % (segment[k][0], segment[k][1], divvol[k]))
            k = len(segment)-1
            if numtag == "当前余额":
                f.write("%s,%s,%s,0,0,%s" % (segment[k][0], segment[k][1], divvol[k], divamount[k]))
            if numtag == "可用股数":
                f.write("%s,%s,%s,1,1" % (segment[k][0], segment[k][1], divvol[k]))
            f.close()

        curamount = stocktotalamount
        nominalamount = "全清"
        divvol = []
        divamount = []
        ratio = curamount / stocktotalamount
        for k in range(len(segment)):
            divvol.append(segment[k][2])
            divamount.append(segment[k][5])
        filepath = dirpath + classes[i] + str(nominalamount) + ".csv"
        f = open(filepath, "w")
        for k in range(len(segment) - 1):
            if numtag == "当前余额":
                f.write("%s,%s,%s,0,0,%s\n" % (segment[k][0], segment[k][1], divvol[k], divamount[k]))
            if numtag == "可用股数":
                f.write("%s,%s,%s,1,1\n" % (segment[k][0], segment[k][1], divvol[k]))
        k = len(segment) - 1
        if numtag == "当前余额":
            f.write("%s,%s,%s,0,0,%s" % (segment[k][0], segment[k][1], divvol[k], divamount[k]))
        if numtag == "可用股数":
            f.write("%s,%s,%s,1,1" % (segment[k][0], segment[k][1], divvol[k]))
        f.close()


