from WindPy import *
import datetime

f = open("E:/记录/离岸人民币ZigZag/USDCNH最高价ZigZag.csv")
HZigZag = []
while True:
    contents = f.readline()
    if not contents:
        break
    else:
        contents = contents.split("\n")[0]
        content = contents.split(",")
        HZigZag.append(content[8])
f.close()

f = open("E:/记录/离岸人民币ZigZag/USDCNH最低价ZigZag.csv")
LZigZag = []
Dat = []
O = []
H = []
L = []
C = []
while True:
    contents = f.readline()
    if not contents:
        break
    else:
        contents = contents.split("\n")[0]
        content = contents.split(",")
        Dat.append(datetime.datetime.strptime(content[0],"%Y-%m-%d").strftime("%Y-%m-%d"))
        O.append(content[1])
        H.append(content[2])
        L.append(content[3])
        C.append(content[4])
        LZigZag.append(content[8])
f.close()

HDate = []
Direction = 1 #0向下，1向上
i = 1
NowZigZag = HZigZag[0]
while i < len(HZigZag):
    if Direction == 0:
        if HZigZag[i]>NowZigZag:
            Direction = 1
            continue
        else:
            NowZigZag = HZigZag[i]
    if Direction == 1:
        if HZigZag[i]<NowZigZag:
            Direction = 0
            HDate.append(Dat[i-1])
        else:
            NowZigZag = HZigZag[i]
    i = i + 1

LDate = []
Direction = 1
i = 1
NowZigZag = LZigZag[0]
while i < len(LZigZag):
    if Direction == 0:
        if LZigZag[i]>NowZigZag:
            Direction = 1
            LDate.append(Dat[i - 1])
            continue
        else:
            NowZigZag = LZigZag[i]
    if Direction == 1:
        if LZigZag[i]<NowZigZag:
            Direction = 0
        else:
            NowZigZag = LZigZag[i]
    i = i + 1

w.start()
indexData = w.wsd("399300.SZ", "open,high,low,close", "2010-8-23", "2016-5-12", "")
indexH = indexData.Data[1]
indexL = indexData.Data[2]
indexTimes = []

for i in range(len(indexData.Times)):
    indexTimes.append(indexData.Times[i].strftime("%Y-%m-%d"))

Hsample = 0
Hwin = 0
Hwindate = []

for i in range(len(LDate)):
    CurDate = LDate[i]
    x = -1
    for j in range(len(indexData.Times)):
        if indexTimes[j] == CurDate:
            x = j
    if (x != -1) and (x>=3) and ((x+4)<=(len(indexH)-1)):
        Hsample = Hsample + 1
        flag = True
        segment = indexH[x-3:x+4]
        MAX = max(segment)
        if indexH[x] < MAX*(1-0.005):
            flag = False
        '''for k in range(x-3,x,1):
            if indexH[k]>indexH[x]:
                flag = False
        for k in range(x+1,x+4,1):
            if indexH[k]>indexH[x]:
                flag = False'''
        if flag == True:
            Hwin = Hwin + 1
            Hwindate.append(CurDate)

Lsample = 0
Lwin = 0
Lwindate = []

for i in range(len(HDate)):
    CurDate = HDate[i]
    x = -1
    for j in range(len(indexData.Times)):
        if indexTimes[j] == CurDate:
            x = j
    if (x != -1) and (x>=3) and ((x+4)<=(len(indexL)-1)):
        Lsample = Lsample + 1
        flag = True
        segment = indexL[x-3:x+4]
        MIN = min(segment)
        if indexL[x] > MIN*(1+0.005):
            flag = False
        '''for k in range(x-3,x,1):
            if indexH[k]>indexH[x]:
                flag = False
        for k in range(x+1,x+4,1):
            if indexH[k]>indexH[x]:
                flag = False'''
        if flag == True:
            Lwin = Lwin + 1
            Lwindate.append(CurDate)

print("%s %s %s %s"%(Hwin,Hsample,Lwin,Lsample))








