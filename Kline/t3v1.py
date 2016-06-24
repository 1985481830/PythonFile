#-*- coding:utf-8 -*-
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

import numpy as np
from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.finance import candlestick_ohlc
from WindPy import *
import threading
import datetime
import time

LabelNum = 30
CandleNum = 101
StockCode = ["399300.SZ","399905.SZ","000016.SH","399001.SZ","399006.SZ"] #沪深300，中证500，上证50，深成指，创业板指
StockName = ["沪深300","中证500","上证50","深成指","创业板指"]
StockString = "399300.SZ,399905.SZ,000016.SH,399001.SZ,399006.SZ"
StockDict = {"399300.SZ":0,"399905.SZ":1,"000016.SH":2,"399001.SZ":3,"399006.SZ":4}
StartDateAndTime = "2016-03-04 15:00:00" #15分钟K线的开始时间
BarSize = "BarSize=15"
DrawOHLC = [[0,0,0,0,0]] * CandleNum #要画到图上的数据集，要修改之，需要先获取ThreadLock
DrawTime = [0] * CandleNum
DrawOHLC[CandleNum-1] =[CandleNum-1,3120,3150,3100,3130]
CurrentIndex = 0 #默认画的是第一品种，即沪深300
CurrentFreq = 30 #默认是30分钟

K15OHLC = []  # 存放各指数的15分钟数据
K15Time = []  # 与OHLC对应的时间，带日期
K30OHLC = []
K30Time = []
LastK30OHLC = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
LastK30Time = ["", "", "", "", ""]
K60OHLC = []
K60Time = []
LastK60OHLC = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
LastK60Time = ["", "", "", "", ""]

def drawPic():
    drawPic.f.clf()
    drawPic.a = drawPic.f.add_subplot(111)
    #color = ['b', 'r', 'y', 'g']
    yUpLimit = DrawOHLC[0][2]
    yDownLimit = DrawOHLC[0][3]
    for i in range(CandleNum):
        if DrawOHLC[i][2] > yUpLimit:
            yUpLimit = DrawOHLC[i][2]
        if DrawOHLC[i][3] < yDownLimit:
            yDownLimit = DrawOHLC[i][3]
    yUpLimit = (int(yUpLimit/50)+1)*50
    yDownLimit = int(yDownLimit/50)*50
    candlestick_ohlc(drawPic.a, DrawOHLC,width=0.4, colorup='#db3f3f', colordown='#77d879',alpha =1)
    drawPic.a.set_title(StockName[CurrentIndex]+" %d分钟"%CurrentFreq)
    drawPic.a.set_xlim(-1,CandleNum+1)
    drawPic.a.set_ylim(yDownLimit,yUpLimit)
    drawPic.canvas.show()

class GetK15Data(threading.Thread):
    def __init__(self):
        super(GetK15Data,self).__init__()

    def InitK15Data(self):
        BeginLock.acquire()

        NowDateAndTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #字符串
        #NowDateAndTime = "2016-04-08 13:19:34" #~~~~~~~~~
        for i in range(len(StockCode)): #各指数单独进行
            IndexCode = StockCode[i]
            flag = False
            while (flag == False):
                IndexRawData = w.wsi(IndexCode, "open,high,low,close", StartDateAndTime, NowDateAndTime, BarSize)
                if (IndexRawData.ErrorCode == 0):
                    flag = True #取到成功为止
            K15OHLC.append(IndexRawData.Data) #K15OHLC最后就有数个List，每个List又有对应指数的开高低收
            for j in range(len(IndexRawData.Times)):
                IndexRawData.Times[j] = IndexRawData.Times[j].strftime("%Y-%m-%d %H:%M:%S") #变成字符串
            K15Time.append(IndexRawData.Times) #数个List，每个单独对应一个指数的时间

            TempKTime = []
            O = []
            H = []
            L = []
            C = []
            for j in range(1,len(K15Time[i]),2): #合成最初的30分钟K线
                TempKTime.append(K15Time[i][j])
                O.append(K15OHLC[i][0][j-1])
                H.append(max(K15OHLC[i][1][j-1],K15OHLC[i][1][j]))
                L.append(min(K15OHLC[i][2][j-1],K15OHLC[i][2][j]))
                C.append(K15OHLC[i][3][j])
            K30Time.append(TempKTime)
            K30OHLC.append([O,H,L,C])

            NewLast30KStr = TempKTime[len(TempKTime) - 1]  #取日内跳价，生成当前的最后一根30分钟K线的原始数据
            NewNowTimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticks = w.wst(StockCode[i], "last", NewLast30KStr, NewNowTimeStr, "")  # 取日内跳价
            MaxTick = max(ticks.Data[0])
            MinTick = min(ticks.Data[0])
            #ThreadLock.acquire()
            LastK30OHLC[i][0] = ticks.Data[0][0]
            LastK30OHLC[i][1] = MaxTick
            LastK30OHLC[i][2] = MinTick
            LastK30OHLC[i][3] = ticks.Data[0][len(ticks.Data[0]) - 1]
            #ThreadLock.release()

            TempKTime = []
            O = []
            H = []
            L = []
            C = []
            for j in range(6,len(K15Time[i]),4): #合成最初的60分钟K线；控制好StartDateAndTime的话，K15Time长度肯定是大于7的
                TempKTime.append(K15Time[i][j])
                O.append(K15OHLC[i][0][j-3])
                H.append(max(K15OHLC[i][1][j-3],K15OHLC[i][1][j-2],K15OHLC[i][1][j-1],K15OHLC[i][1][j]))
                L.append(min(K15OHLC[i][2][j-3],K15OHLC[i][2][j-2],K15OHLC[i][2][j-1],K15OHLC[i][2][j]))
                C.append(K15OHLC[i][3][j])
            K60Time.append(TempKTime)
            K60OHLC.append([O,H,L,C])

            NewLast60KStr = TempKTime[len(TempKTime) - 1] #取日内跳价，生成当前的最后一根60分钟K线的原始数据
            NewNowTimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticks = w.wst(StockCode[i], "last", NewLast60KStr, NewNowTimeStr, "")  # 取日内跳价
            MaxTick = max(ticks.Data[0])
            MinTick = min(ticks.Data[0])
            #ThreadLock.acquire()
            LastK60OHLC[i][0] = ticks.Data[0][0]
            LastK60OHLC[i][1] = MaxTick
            LastK60OHLC[i][2] = MinTick
            LastK60OHLC[i][3] = ticks.Data[0][len(ticks.Data[0]) - 1]
            #ThreadLock.release()

            if (i == CurrentIndex):
                if (CurrentFreq == 30):
                    K30Length = len(K30Time[i])
                    for j in range(CandleNum-2,-1,-1):
                        K30J = K30Length+j-CandleNum+1 #注意是从0开始，故不是-100而是-101
                        DrawOHLC[j] = [j,K30OHLC[i][0][K30J],K30OHLC[i][1][K30J],K30OHLC[i][2][K30J],K30OHLC[i][3][K30J]]
                        DrawTime[j] = K30Time[i][K30J]
                    #drawPic()
                    '''for j in range(LabelNum - 1): #把DrawOHLC的数据也写到Label上
                        TimeLabel[LabelNum - j - 1]['text'] = DrawTime[CandleNum - 2 - j][5:]
                        DataOLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][1]
                        DataHLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][2]
                        DataLLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][3]
                        DataCLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][4]'''


                else: #此时CurrentFreq为60，代表60分钟线
                    K60Length = len(K60Time[i])
                    for j in range(CandleNum-2, -1, -1):
                        K60J = K60Length + j - CandleNum+1
                        DrawOHLC[j] = [j,K60OHLC[i][0][K60J],K60OHLC[i][1][K60J],K60OHLC[i][2][K60J],K60OHLC[i][3][K60J]]
                        DrawTime[j] = K60Time[i][K60J]
                    #drawPic()
                    '''for j in range(LabelNum - 1):  # 把DrawOHLC的数据也写到Label上
                        TimeLabel[LabelNum - j - 1]['text'] = DrawTime[CandleNum - 2 - j][5:]
                        DataOLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][1]
                        DataHLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][2]
                        DataLLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][3]
                        DataCLabel[LabelNum - j - 1]['text'] = DrawOHLC[CandleNum - 2 - j][4]'''

        BeginLock.release()

    def CycleGetK15(self):
        MorningBeginTime = datetime.datetime.strptime("09:45:00","%H:%M:%S")
        MorningEndTime = datetime.datetime.strptime("11:30:00","%H:%M:%S")
        AfternoonBeginTime = datetime.datetime.strptime("13:15:00","%H:%M:%S")
        AfternoonEndTime = datetime.datetime.strptime("15:00:00","%H:%M:%S")
        TodayStr = datetime.datetime.now().strftime('%Y-%m-%d ') #字符串
        TimeInterval = datetime.timedelta(minutes=15)  # 15分钟的间隔

        while True:
            time.sleep(5)
            NowTimeStr = datetime.datetime.now().strftime('%H:%M:%S') #字符串
            #NowTimeStr = "14:06:17" #~~~~~~~
            NowTime = datetime.datetime.strptime(NowTimeStr,"%H:%M:%S") #dattime，只有时间，无日期（日期是1900-1-1）
            #if NowTime > datetime.datetime.strptime("00:00:00", "%H:%M:%S"): #~~~~~~~~~~
            if ((NowTime > MorningBeginTime) and (NowTime < MorningEndTime)) or ((NowTime > AfternoonBeginTime) and (NowTime < AfternoonEndTime)):
                for i in range(len(StockCode)):
                    LastK15Time = datetime.datetime.strptime(K15Time[i][len(K15Time[i])-1][-8:],"%H:%M:%S") #去掉日期，取时间
                    if ((NowTime - LastK15Time) > TimeInterval):
                        #当前时间已经超过了上一根有15分钟，就新取一次K线
                        RawData = w.wsi(StockCode[i], "open,high,low,close", K15Time[i][len(K15Time[i])-1], TodayStr+NowTimeStr, BarSize)
                        if len(RawData.Times)>1: #0号一定是上一根K线对应的日期，len至少为1；大于1才代表有新K线
                            del (RawData.Times[0])
                            for j in range(4):
                                del RawData.Data[j][0]  #把开高低收的第一个去掉，对应的是0号，即上一根K线
                            for j in range(len(RawData.Times)):
                                K15Time[i].append(RawData.Times[j].strftime("%Y-%m-%d %H:%M:%S"))
                                K15OHLC[i][0].append(RawData.Data[0][j])
                                K15OHLC[i][1].append(RawData.Data[1][j])
                                K15OHLC[i][2].append(RawData.Data[2][j])
                                K15OHLC[i][3].append(RawData.Data[3][j])

                            TempKTime = [] #添加30分钟K线
                            O = []
                            H = []
                            L = []
                            C = []
                            for j in range(len(K15Time[i])-len(RawData.Times),len(K15Time[i]),1):
                                if (j%2 == 1):
                                    TempKTime.append(K15Time[i][j])
                                    O.append(K15OHLC[i][0][j-1])
                                    H.append(max(K15OHLC[i][1][j-1],K15OHLC[i][1][j]))
                                    L.append(min(K15OHLC[i][2][j-1],K15OHLC[i][2][j]))
                                    C.append(K15OHLC[i][3][j])
                            for j in range(len(TempKTime)):
                                K30Time[i].append(TempKTime[j])
                                K30OHLC[i][0].append(O[j])
                                K30OHLC[i][1].append(H[j])
                                K30OHLC[i][2].append(L[j])
                                K30OHLC[i][3].append(C[j])

                            if len(TempKTime) > 0:  #当30分钟增加之后，有必要重新获取新一轮的日内跳价，以合成最后一根K线
                                NewLast30KStr = TempKTime[len(TempKTime)-1]
                                NewNowTimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                ticks = w.wst(StockCode[i], "last", NewLast30KStr, NewNowTimeStr, "") #取日内跳价
                                MaxTick = max(ticks.Data[0])
                                MinTick = min(ticks.Data[0])
                                #ThreadLock.acquire()
                                LastK30OHLC[i][0] = ticks.Data[0][0]
                                LastK30OHLC[i][1] = MaxTick
                                LastK30OHLC[i][2] = MinTick
                                LastK30OHLC[i][3] = ticks.Data[0][len(ticks.Data[0])-1]
                                #ThreadLock.release()

                            TempKTime = []  #添加60分钟K线
                            O = []
                            H = []
                            L = []
                            C = []
                            for j in range(len(K15Time[i]) - len(RawData.Times), len(K15Time[i]), 1):
                                if (j%4 == 2):
                                    TempKTime.append(K15Time[i][j])
                                    O.append(K15OHLC[i][0][j-3])
                                    H.append(max(K15OHLC[i][1][j-3],K15OHLC[i][1][j-2],K15OHLC[i][1][j-1],K15OHLC[i][1][j]))
                                    L.append(min(K15OHLC[i][2][j-3],K15OHLC[i][2][j-2],K15OHLC[i][2][j-1],K15OHLC[i][2][j]))
                                    C.append(K15OHLC[i][3][j])
                            for j in range(len(TempKTime)):
                                K60Time[i].append(TempKTime[j])
                                K60OHLC[i][0].append(O[j])
                                K60OHLC[i][1].append(H[j])
                                K60OHLC[i][2].append(L[j])
                                K60OHLC[i][3].append(C[j])

                            if len(TempKTime) > 0:  #当60分钟增加之后，有必要重新获取新一轮的日内跳价，以合成最后一根K线
                                NewLast60KStr = TempKTime[len(TempKTime)-1]
                                NewNowTimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                ticks = w.wst(StockCode[i], "last", NewLast60KStr, NewNowTimeStr, "") #取日内跳价
                                MaxTick = max(ticks.Data[0])
                                MinTick = min(ticks.Data[0])
                                #ThreadLock.acquire()
                                LastK60OHLC[i][0] = ticks.Data[0][0]
                                LastK60OHLC[i][1] = MaxTick
                                LastK60OHLC[i][2] = MinTick
                                LastK60OHLC[i][3] = ticks.Data[0][len(ticks.Data[0])-1]
                                #ThreadLock.release()

                            if (i == CurrentIndex): #如果是当前选中的图就要更新画图区域数据;暂时先不用Lock看看能不能跑
                                if (CurrentFreq == 30):
                                    K30Length = len(K30Time[i])
                                    for j in range(CandleNum-2, -1, -1):
                                        K30J = K30Length + j - CandleNum+1   # 注意是从0开始，故不是-100而是-101
                                        DrawOHLC[j] = [j, K30OHLC[i][0][K30J], K30OHLC[i][1][K30J],
                                                       K30OHLC[i][2][K30J], K30OHLC[i][3][K30J]]
                                        DrawTime[j] = K30Time[i][K30J]
                                    drawPic()
                                    for j in range(LabelNum - 1):  # 把DrawOHLC的数据也写到Label上
                                        TimeLabel[j+1]['text'] = DrawTime[CandleNum - 2 - j][5:]
                                        DataOLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][1]
                                        DataHLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][2]
                                        DataLLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][3]
                                        DataCLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][4]
                                        root.update()
                                else:  # 此时CurrentFreq为60，代表60分钟线
                                    K60Length = len(K60Time[i])
                                    for j in range(CandleNum-2, -1, -1):
                                        K60J = K60Length + j - CandleNum+1
                                        DrawOHLC[j] = [j, K60OHLC[i][0][K60J], K60OHLC[i][1][K60J],
                                                       K60OHLC[i][2][K60J], K60OHLC[i][3][K60J]]
                                        DrawTime[j] = K60Time[i][K60J]

                                    drawPic()
                                    for j in range(LabelNum - 1):  # 把DrawOHLC的数据也写到Label上
                                        TimeLabel[j+1]['text'] = DrawTime[CandleNum - 2 - j][5:]
                                        DataOLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][1]
                                        DataHLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][2]
                                        DataLLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][3]
                                        DataCLabel[j+1]['text'] = DrawOHLC[CandleNum - 2 - j][4]
                                        root.update()

    def run(self):
        self.InitK15Data() #初始化15分钟数据
        self.CycleGetK15() #对各指数进行循环，当前时间大于最后一根K线超过15分钟时就启动获取15分钟数据


class CycleGetLastK(threading.Thread):
    def __init__(self):
        super(CycleGetLastK,self).__init__()

    def wsqCallback(self, inData):
        FieldCount = len(inData.Data) - 1
        CodeCount = len(inData.Codes)
        try:

            for j in range(LabelNum - 1):
                TimeLabel[j+1]['text'] = DrawTime[CandleNum - 2 - j][5:]
                DataOLabel[j+1]['text'] = "%.2f"%DrawOHLC[CandleNum - 2 - j][1]
                DataHLabel[j+1]['text'] = "%.2f"%DrawOHLC[CandleNum - 2 - j][2]
                DataLLabel[j+1]['text'] = "%.2f"%DrawOHLC[CandleNum - 2 - j][3]
                DataCLabel[j+1]['text'] = "%.2f"%DrawOHLC[CandleNum - 2 - j][4]
                #root.update_idletasks()
                root.update()

            for i in range(CodeCount):
                StockI = StockDict[inData.Codes[i]]
                #ThreadLock.acquire()
                if inData.Data[FieldCount][i] > LastK30OHLC[StockI][1]:
                    LastK30OHLC[StockI][1] = inData.Data[FieldCount][i]
                if inData.Data[FieldCount][i] < LastK30OHLC[StockI][2]:
                    LastK30OHLC[StockI][2] = inData.Data[FieldCount][i]
                LastK30OHLC[StockI][3] = inData.Data[FieldCount][i]
                if inData.Data[FieldCount][i] > LastK60OHLC[StockI][1]:
                    LastK60OHLC[StockI][1] = inData.Data[FieldCount][i]
                if inData.Data[FieldCount][i] < LastK60OHLC[StockI][2]:
                    LastK60OHLC[StockI][2] = inData.Data[FieldCount][i]
                LastK60OHLC[StockI][3] = inData.Data[FieldCount][i]
                if FieldCount > 0:
                    LastK30Time[StockI] = str(inData.Data[FieldCount-1][i])
                    LastK60Time[StockI] = str(inData.Data[FieldCount-1][i])
                #ThreadLock.release()
                if StockI == CurrentIndex:
                    if CurrentFreq == 30:
                        DrawOHLC[CandleNum - 1] = [CandleNum - 1, LastK30OHLC[StockI][0], LastK30OHLC[StockI][1],
                                                   LastK30OHLC[StockI][2], LastK30OHLC[StockI][3]]
                    else:
                        DrawOHLC[CandleNum - 1] = [CandleNum - 1, LastK60OHLC[StockI][0], LastK60OHLC[StockI][1],
                                                   LastK60OHLC[StockI][2], LastK60OHLC[StockI][3]]
                    drawPic()
                    print(inData.Times[i].strftime("%m-%d %H:%M:%S"))
                    TimeLabel[0]['text'] = inData.Times[i].strftime("%m-%d %H:%M:%S")
                    DataOLabel[0]['text'] = "%.2f"%DrawOHLC[CandleNum - 1][1]
                    DataHLabel[0]['text'] = "%.2f"%DrawOHLC[CandleNum - 1][2]
                    DataLLabel[0]['text'] = "%.2f"%DrawOHLC[CandleNum - 1][3]
                    DataCLabel[0]['text'] = "%.2f"%DrawOHLC[CandleNum - 1][4]
                    # root.update_idletasks()
                    root.update()

        except:
            pass

    def run(self):
        #self.firstdraw = False  # 因为在合成K线的线程初始化时，主线程还未loop，不能更新label；这一变量用于在获取最后一根K线的回调函数中更新
        w.wsq(StockString, "rt_time,rt_last",func = self.wsqCallback)

def SetPic(Index,Freq):
    global CurrentIndex
    global CurrentFreq
    global LastK30Time
    global LastK60Time
    CurrentIndex = Index
    CurrentFreq = Freq

    if Freq == 30:
        K30Length = len(K30Time[Index])
        for j in range(CandleNum - 2, -1, -1):
            K30J = K30Length + j - CandleNum + 1  # 注意是从0开始，故不是-100而是-101
            DrawOHLC[j] = [j, K30OHLC[Index][0][K30J], K30OHLC[Index][1][K30J], K30OHLC[Index][2][K30J], K30OHLC[Index][3][K30J]]
            DrawTime[j] = K30Time[Index][K30J]
        DrawTime[CandleNum-1] = LastK30Time[Index]
        DrawOHLC[CandleNum-1] = [CandleNum-1,LastK30OHLC[Index][0],LastK30OHLC[Index][1],LastK30OHLC[Index][2],LastK30OHLC[Index][3]]
        drawPic()

        for j in range(LabelNum - 1):
            TimeLabel[j + 1]['text'] = DrawTime[CandleNum - 2 - j][5:]
            DataOLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][1]
            DataHLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][2]
            DataLLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][3]
            DataCLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][4]
            # root.update_idletasks()
            root.update()

        TimeLabel[0]['text'] = DrawTime[CandleNum - 1]
        DataOLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][1]
        DataHLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][2]
        DataLLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][3]
        DataCLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][4]
        # root.update_idletasks()
        root.update()
    else:
        K60Length = len(K60Time[Index])
        for j in range(CandleNum - 2, -1, -1):
            K60J = K60Length + j - CandleNum + 1  # 注意是从0开始，故不是-100而是-101
            DrawOHLC[j] = [j, K60OHLC[Index][0][K60J], K60OHLC[Index][1][K60J], K60OHLC[Index][2][K60J], K60OHLC[Index][3][K60J]]
            DrawTime[j] = K60Time[Index][K60J]
        DrawTime[CandleNum-1]=LastK60Time[Index]
        DrawOHLC[CandleNum-1]=[CandleNum-1,LastK60OHLC[Index][0],LastK60OHLC[Index][1],LastK60OHLC[Index][2],LastK60OHLC[Index][3]]
        drawPic()

        for j in range(LabelNum - 1):
            TimeLabel[j + 1]['text'] = DrawTime[CandleNum - 2 - j][5:]
            DataOLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][1]
            DataHLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][2]
            DataLLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][3]
            DataCLabel[j + 1]['text'] = "%.2f" % DrawOHLC[CandleNum - 2 - j][4]
            # root.update_idletasks()
            root.update()

        TimeLabel[0]['text'] = DrawTime[CandleNum - 1]
        DataOLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][1]
        DataHLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][2]
        DataLLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][3]
        DataCLabel[0]['text'] = "%.2f" % DrawOHLC[CandleNum - 1][4]
        # root.update_idletasks()
        root.update()

if __name__ == '__main__':

    matplotlib.use('TkAgg')
    root = Tk()
    root.title("自定义行情")
    drawPic.f = Figure(figsize=(14, 9), dpi=100)
    drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
    drawPic.canvas.show()
    drawPic.canvas.get_tk_widget().grid(row=1, column = 0,columnspan=12,rowspan = 32)
    #Label(root, text='请输入样本数量：').grid(row=1, column=0)
    #inputEntry = Entry(root)
    #inputEntry.grid(row=1, column=1)
    #inputEntry.insert(0, '50')
    Label(root, text="     ", width=13, height=1).grid(row=1, column=12, columnspan=1, rowspan=1)
    Label(root, text="开盘价",width=7,height = 1).grid(row=1,column=13,columnspan=1,rowspan = 1)
    Label(root, text="最高价", width=7, height=1).grid(row=1,column=14,columnspan=1,rowspan = 1)
    Label(root, text="最低价", width=7, height=1).grid(row=1,column=15,columnspan=1,rowspan = 1)
    Label(root, text="收盘价", width=7, height=1).grid(row=1, column=16, columnspan=1, rowspan=1)
    TimeLabel = []
    DataOLabel = []
    DataHLabel = []
    DataLLabel = []
    DataCLabel = []
    for k in range(LabelNum):
        TimeLabel.append(Label(root,text="01-01 12:00:00",width=12,height=1))
        TimeLabel[k].grid(row=k+2,column=12,columnspan=1,rowspan=1)
        DataOLabel.append(Label(root,text="66666.66",width=8,height=1))
        DataOLabel[k].grid(row=k+2,column=13,columnspan=1,rowspan=1)
        DataHLabel.append(Label(root,text="66666.66",width=8,height=1))
        DataHLabel[k].grid(row=k+2,column=14,columnspan=1,rowspan=1)
        DataLLabel.append(Label(root,text="66666.66",width=8,height=1))
        DataLLabel[k].grid(row=k+2,column=15,columnspan=1,rowspan=1)
        DataCLabel.append(Label(root,text="66666.66",width=8,height=1))
        DataCLabel[k].grid(row=k+2,column=16,columnspan=1,rowspan=1)

    #Lab = Label(root, text="Label", width=30, height=10)
    #Lab.grid(row=1, column=12, columnspan=1)
    Button(root, text='沪深300 30分钟', command=lambda:SetPic(0,30)).grid(row=0, column=1,columnspan=1)
    Button(root, text='沪深300 60分钟', command=lambda:SetPic(0,60)).grid(row=0, column=2,columnspan=1)
    Button(root, text='中证500 30分钟', command=lambda:SetPic(1,30)).grid(row=0, column=3,columnspan=1)
    Button(root, text='中证500 60分钟', command=lambda:SetPic(1,60)).grid(row=0, column=4,columnspan=1)
    Button(root, text='上证50 30分钟', command=lambda:SetPic(2,30)).grid(row=0, column=5,columnspan=1)
    Button(root, text='上证50 60分钟', command=lambda:SetPic(2,60)).grid(row=0, column=6,columnspan=1)
    Button(root, text='深成指 30分钟', command=lambda:SetPic(3,30)).grid(row=0, column=7,columnspan=1)
    Button(root, text='深成指 60分钟', command=lambda:SetPic(3,60)).grid(row=0, column=8,columnspan=1)
    Button(root, text='创业板指 30分钟', command=lambda:SetPic(4,30)).grid(row=0, column=9,columnspan=1)
    Button(root, text='创业板指 60分钟', command=lambda:SetPic(4,60)).grid(row=0, column=10,columnspan=1)

    #Button(root, text='画图', command=lambda:ddd(5)).grid(row=1, column=2, columnspan=3)

    w.start()
    #ThreadLock = threading.Lock()
    BeginLock = threading.Lock()


    K15thread = GetK15Data()
    K15thread.start()
    time.sleep(1)

    BeginLock.acquire()

    GetLastKThread = CycleGetLastK()
    GetLastKThread.start()

    time.sleep(1)

    root.mainloop()