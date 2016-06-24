#-*- coding:utf-8 -*-
import datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from WindPy import *
import threading
from tkinter import *
'''
w.start()
StockList = ["399300.SZ","399905.SZ","000016.SH","399001.SZ","399006.SZ"] #沪深300，中证500，上证50，深综指，创业板指
StockName = [u"沪深300",u"中证500",u"上证50",u"深综指",u"创业板指"]
StartDateAndTime = "2016-01-04 15:00:00"
BarSize = "BarSize=15"
fig = plt.figure()
ax1 = plt.subplot2grid((1,1),(0,0))
plt.xlabel('Date')
plt.ylabel('Price')
'''
#data = w.wsi("399300.SZ", "open,high,low,close", StartDateAndTime, "2016-04-01 00:46:18", BarSize)
'''
class test(object):
    def __init__(self,parent):
        self.parent = parent
        self.n = 0
        Button(self.parent,text=u'沪深300',command = self.hs300).pack()
        num = 2
        fig = []
        self.canvas = []
        for i in range(num):
            fig.append(plt.figure())
            self.canvas.append(FigureCanvasTkAgg)

class Get15MinThread(threading.Thread):
    def __init__(self,Code,Name):
        super(Get15MinThread,self).__init__()
        self.IndexCode = Code
        self.IndexName = Name
        self.Time = []
        self.Open = []
        self.High = []
        self.Low = []
        self.Close = []
        self.OHLC = []
        self.Init15MinData()

    def Init15MinData(self):
        NowDateAndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        RawData = w.wsi(self.IndexCode, "open,high,low,close", StartDateAndTime, NowDateAndTime, BarSize)
        for i in range(len(RawData.Times)):
            #self.Time.append(RawData.Times[i].strftime("%Y-%m-%d %H:%M:%S"))
            self.Time.append(i)
            self.Open.append(RawData.Data[0][i])
            self.High.append(RawData.Data[1][i])
            self.Low.append(RawData.Data[2][i])
            self.Close.append(RawData.Data[3][i])
        for i in range(100):
            k = len(RawData.Times)-100+i
            append_me = self.Time[k],self.Open[k],self.High[k],self.Low[k],self.Close[k]
            self.OHLC.append(append_me)
        plt.title(self.IndexName)
        candlestick_ohlc(ax1, self.OHLC, width=0.4, colorup='#77d879', colordown='#db3f3f')
        plt.show()

    def AskFor15MinData(self):
        data = w.wsi(self.IndexCode, "open,high,low,close", StartDateAndTime, "2016-04-01 00:46:18", BarSize)
'''
#t = Get15MinThread(StockList[0],StockName[0])
#t.start()

date = []
open = []
high = []
low = []
close = []
ohlc = []
for i in range(30):
    date.append(i)
    open.append(2+i)
    high.append(4+i)
    low.append(1+i)
    close.append(3+i)

fig = plt.figure()
ax1 = plt.subplots()
#ax1 = plt.subplot2grid((1,1), (0,0))

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('stock')
plt.legend()
#plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)

plt.ion()

for x in range(30):
    append_me = date[x], open[x], high[x], low[x], close[x]
    ohlc.append(append_me)
    csticks = candlestick_ohlc(ax1, ohlc,width=0.4, colorup='#77d879', colordown='#db3f3f')
    plt.pause(0.1)

