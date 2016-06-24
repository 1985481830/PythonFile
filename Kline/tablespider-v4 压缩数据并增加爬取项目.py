# -*- coding:utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
from time import sleep
import random
import threading
import pymysql
import gzip
import re

header = {
    'Host': 'stock.quote.stockstar.com',
    'Proxy-Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4'
}

class SpiderThread(threading.Thread):

    wait = []   #wait是待爬取股票代码的列表
    lock = threading.Lock()     #从wait中取项目时用lock以防线程冲突
    proxylock = threading.Lock()    #因为有额外线程用来定时更换proxylist，故用proxylock防线程在此时取proxy
    proxylist = []
    BalanceDict = {}
    CashflowDict = {}
    ProfitDict = {}

    def __init__(self,threadNo):
        super(SpiderThread,self).__init__()
        self.threadNo = threadNo

    def randompickproxy(self,proxylist):
        SpiderThread.proxylock.acquire()    #确认此时proxythread没有在写入proxylist
        proxy = proxylist[random.randint(0,len(proxylist)-1)]
        SpiderThread.proxylock.release()
        return proxy

    def connect_to_table(self,code):
        if code[0] == '6':  #table不允许数字打头，只能加个sh或sz了
            exchange = 'sh'
        else:
            exchange = 'sz'
        code = exchange + code
        #注意，在connect的时候要指明charset是utf8（不是utf-8）,这样才不会写入中文时发生错误！
        self.conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '1234',port = 3306,charset='utf8')
        #self.conn = pymysql.connect(host = '10.66.114.178',user = 'root',passwd = '1234abcd',port = 3306,charset='utf8')
        #每个线程都有一个单独的conn，也就是说开多少线程就有多少个数据库连接
        self.conn.select_db('financial_report')     #此时经过预置工作，financial_report库是存在的
        self.cur = self.conn.cursor()   #取游标

        try:  #这里使用了drop，考虑到如果之前有中断过的话，干脆把这支股票的未完成数据表先清除
            self.cur.execute('DROP TABLE '+code+'_detail') #注意这里要先删detail表，如果先删主表的话会因有foreign key在detail中而失败
            self.cur.execute('DROP TABLE '+code)
        except:
            pass

        #下面这一段是创建当前要处理的股票（code表示代码）对应的两张表，主表有sheettype,year,period;detail表有item,data，同时有外键与unique约束
        self.cur.execute('CREATE TABLE IF NOT EXISTS '+code+'(Id_M int NOT NULL AUTO_INCREMENT,SheetType VARCHAR(50),Year VARCHAR(4),Period TINYINT(1),ReleaseTime VARCHAR(50),PRIMARY KEY(Id_M))')
        try:
            self.cur.execute('ALTER TABLE '+code+' ADD CONSTRAINT uniqueSheet UNIQUE (SheetType,Year,Period)')
        except:
            pass
        self.cur.execute('CREATE TABLE IF NOT EXISTS '+code+'_detail(Id_D int NOT NULL AUTO_INCREMENT,Item VARCHAR(255),Data VARCHAR(255),Id_M int,PRIMARY KEY(Id_D))')
        try:
            self.cur.execute('ALTER TABLE '+code+'_detail ADD FOREIGN KEY(Id_M) REFERENCES '+code+'(Id_M)')
            self.cur.execute('ALTER TABLE '+code+'_detail ADD CONSTRAINT uniqueItem UNIQUE (Item,Id_M)')
        except:
            pass

    def drop_table(self,code):
        if code[0] == '6':
            exchange = 'sh'
        else:
            exchange = 'sz'
        code = exchange + code
        try: #因为detail表中有foreign key，所以要先drop它，先drop主表会失败
            self.cur.execute('DROP TABLE '+code+'_detail')
            self.cur.execute('DROP TABLE '+code)
            self.conn.commit()
        except:
            pass

    def get_detail(self,type,code,year,Id_M):
        URL = 'http://stock.quote.stockstar.com/stockinfo_finance/'+type+'.aspx?code='+code+'&dt='+year
        req = request.Request(URL,headers = header)
        success = False
        while (success == False):   #既然已经进到取具体的表，就肯定是存在的，取到成功为止
            try:
                IPandPort = self.randompickproxy(SpiderThread.proxylist)    #取代理
                proxy = {'http':IPandPort}
                proxy_support = request.ProxyHandler(proxy)
                opener = request.build_opener(proxy_support)
                request.install_opener(opener)
                #注意！下面不是request.urlopen，这是全局的，用opener.open可以每个线程使用不同代理
                with opener.open(req,data=None,timeout=3) as response:
                    htmlcontent = response.read()
                    try:
                        text = gzip.decompress(htmlcontent).decode('gb2312')    #证券之星的编码是gb2312，要解压就try一下
                    except:
                        text = htmlcontent.decode('gb2312')

                    soup = BeautifulSoup(text,'html.parser')
                    self.contents = soup.find_all(name = 'td',attrs={"class":re.compile(r".*align_left")})
                    #这里是依据网页源码里面项目对应的结构确定，因为class有bg_td_6 align_left与thead_1 align_left两种，故用正则表达式
                    #self.contents = soup.find_all('td',class_='bg_td_6 align_left') 这是旧版本的
                    if len(self.contents) > 0:  #有时抽风会无数据，要检验!!这一步很重要，不然总会偶发地漏数据
                        success = True  #到这里为止是获取具体某一张表的数据
                opener.close()
            except:
                pass
        #成功从网页取回数据，接下来写入数据库中
        if code[0] == '6':
            scode = 'sh'+code
        else:
            scode = 'sz'+code


        for i in range(len(self.contents)):
            Item = self.contents[i].contents[0]  #依次获取项目名称的文本
            while hasattr(Item,'contents'):  #这里的判断是针对现金流量表的特殊结构的，现金流量表中有的项目
                Item = Item.contents[0]
            if hasattr(self.contents[i].nextSibling,'contents'):    #利润表的'六、净利润（百万元）'很特别，无数据时就没有contents（网页显示中这一行也无表格）
                if len(self.contents[i].nextSibling.contents) != 0:  #有些项目根本就没有数据，处理一下
                    Data = self.contents[i].nextSibling.contents[0]  #这里是项目对应的数字
                else:
                    Data = '--'
            else:
                Data = '--'

            if (Data != '--'):  #如果该项目没有数字的话就不存了，省得浪费空间
                #data[contents[i].contents[0]]=contents[i].nextSibling.contents[0]
                Item = Item.strip() #可能偶尔多出空格，要删
                if type == 'balance':
                    dat = [SpiderThread.BalanceDict[Item],Data,Id_M]
                if type == 'cashflow':
                    dat = [SpiderThread.CashflowDict[Item],Data,Id_M]
                if type == 'profit':
                    dat = [SpiderThread.ProfitDict[Item],Data,Id_M]
                 #版本更新后，item改为中文对应的字典数字，以压缩

                #dat = [Item,Data,Id_M]
                #写数据，注意这里item是中文，如果在之前connect时没有注明charset=utf8，会报错
                try:
                    self.cur.execute("INSERT INTO "+scode+"_detail(Item,Data,Id_M) VALUES(%s,%s,%s)",dat)
                    self.conn.commit()
                except:
                    pass

    def set_finish(self,code):  #三种表都搞掂之后finish
        self.cur.execute("UPDATE Status SET Checked = 1 WHERE Code = %s",code)
        self.conn.commit()
        self.conn.close()   #搞定一支股票之后就close该次连接

    def get_year_by_type(self,type,code):
        URL = 'http://stock.quote.stockstar.com/finance/'+type+'_'+code+'.shtml'    #先依据sheettype，取有报表的年份
        req = request.Request(URL,headers = header)
        success = False
        while (success == False):
            try:
                IPandPort = self.randompickproxy(SpiderThread.proxylist)
                proxy = {'http':IPandPort}
                proxy_support = request.ProxyHandler(proxy)
                opener = request.build_opener(proxy_support)
                request.install_opener(opener)
                #注意用opener.open而不是全局的request.urlopen，这样每个线程都能使用单独的代理
                with opener.open(req,data=None,timeout=3) as response:
                    htmlcontent = response.read()
                    try:
                        text = gzip.decompress(htmlcontent).decode('gb2312')
                    except:
                        text = htmlcontent.decode('gb2312')

                    soup = BeautifulSoup(text,'html.parser')
                    self.years = soup.find_all('option')
                    #year就是形如2015-03-01之类的字符串
                    if len(self.years) > 0: #有时抽风会无数据，要检验!!这一步很重要，不然总会偶发地漏数据
                        success = True
                opener.close()
            except:
                pass

        if code[0] == '6':
            scode = 'sh' + code
        else:
            scode = 'sz' + code
        for x in range(len(self.years)-1):
            year = self.years[x+1].get('value')  #取得形如2015-09-01之类的文本
            y = year[0:4]   #这才是真正的year
            m = int(year[5:7])//3   #这是period
            dat = [type,y,m]
            self.cur.execute("INSERT INTO "+scode+"(SheetType,Year,Period) VALUES(%s,%s,%s)",dat)
            self.conn.commit()
            self.cur.execute("SELECT Id_M FROM "+scode+" WHERE SheetType = %s AND Year = %s AND Period = %s",dat)
            Id_M = self.cur.fetchone()[0]   #取主表中，该具体报表对应的Id_M，以在get_detail中构建foreign key关系
            self.get_detail(type,code,year,Id_M)

    def acquireData(self,code):
        self.connect_to_table(code)
        self.get_year_by_type('balance',code)
        self.get_year_by_type('cashflow',code)
        self.get_year_by_type('profit',code)
        self.set_finish(code)

    def run(self):
        self.Running = True
        while self.Running == True:
            SpiderThread.lock.acquire() #防止线程争抢而设的lock
            waitnum = len(SpiderThread.wait)
            if waitnum > 0:
                self.Code = SpiderThread.wait[waitnum-1]
                SpiderThread.wait.pop()
                SpiderThread.lock.release()
                self.acquireData(self.Code)
            else:
                self.Running = False
                SpiderThread.lock.release()


    @staticmethod
    def pushlist(code):     #送入待处理股票
        SpiderThread.lock.acquire()
        SpiderThread.wait.append(code)
        SpiderThread.lock.release()

    @staticmethod
    def getwaitlist(list):
        URL = 'http://quote.stockstar.com/search.aspx?keyword='    #先依据sheettype，取有报表的年份
        req = request.Request(URL,headers = header)
        success = False
        while (success == False):
            try:
                with request.urlopen(req,data=None,timeout=10) as response:
                    htmlcontent = response.read()
                    text = gzip.decompress(htmlcontent).decode('gbk') #此页面用gbk才能解，源码却写gb2312，莫名其妙
                    soup = BeautifulSoup(text,'html.parser')
                    tbody = soup.find_all('tbody')  #tbody[0]是股票，后面是债券基金啥的
                    codes = tbody[0].find_all('tr',class_='td3')
                    success = True
            except:
                pass
        confirm = ['000','001','002','600','601','603','300']
        for i in range(len(codes)):
            try:
                code = codes[i].contents[0].contents[0].contents[0]
                b = False
                for x in confirm:
                    if code[0:3] == x:
                        b = True
                if b == True:
                    list.append(code)
            except:
                pass
            try:
                code = codes[i].contents[5].contents[0].contents[0] #一行最多有两支股票，分别是contents[0]和[5]；预防单数故分开try
                b = False
                for x in confirm:
                    if code[0:3] == x:
                        b = True
                if b == True:
                    list.append(code)
            except:
                pass


#第一步：取出字典
f = open('R:/balancedict.txt','r')
for line in f.readlines():
    line = line.strip().split(',')
    SpiderThread.BalanceDict[line[1]] = line[0]
f.close()

f = open('R:/cashflowdict.txt','r')
for line in f.readlines():
    line = line.strip().split(',')
    SpiderThread.CashflowDict[line[1]] = line[0]
f.close()

f = open('R:/profitdict.txt','r')
for line in f.readlines():
    line = line.strip().split(',')
    SpiderThread.ProfitDict[line[1]] = line[0]
f.close()


#第二步，连接数据库，尝试建立数据库与status表，建status表需要一段时间的爬取网页
conn = pymysql.connect(host = 'localhost',user = 'root',passwd = '1234',port = 3306,charset='utf8')
#conn = pymysql.connect(host = '10.66.114.178',user = 'root',passwd = '1234abcd',port = 3306,charset='utf8')
cur = conn.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS financial_report')
conn.select_db('financial_report')
#这一段用来创建status表，用以确认哪支股票完成数据收集了(Checked不为0代表已搞掂，收集完成是1)

try:
    cur.execute('CREATE TABLE Status(Id int NOT NULL AUTO_INCREMENT,Code VARCHAR(6) UNIQUE,Checked TINYINT(1) DEFAULT 0,PRIMARY KEY(Id))')
    #status表三个字段，Id是主键，只是用于表顺序；Code是股票代码；Checked默认0，表示未确认，当线程中收集完一支股票就改为1，不存在改为-1
    list = []   #只在CREATE TABLE成功时才会执行到getwaitlist
    SpiderThread.getwaitlist(list)

    for code in list:
        cur.execute("INSERT IGNORE INTO Status(Code) VALUES(%s)",code)
        conn.commit()
except:
    pass

#如果是中断再开的话，前面try的部分是不会执行的，此时取出所有Checked = 0的待处理股票，再处理
number = cur.execute('SELECT Code FROM Status WHERE Checked = 0')
info = cur.fetchall()
for x in info:
    SpiderThread.pushlist(x[0])

#第三步，开启定时更换代理的进程
def proxythread():  #定时换代理
    while True:
        SpiderThread.proxylock.acquire()
        b = False
        while b == False:
            try:
                file = open('R:/proxylist.txt','r')
                #file = open('/home/ubuntu/proxylist.txt','r')
                SpiderThread.proxylist = []
                for line in file.readlines():
                    SpiderThread.proxylist.append(line.strip())
                file.close()
                b = True
                SpiderThread.proxylock.release()
            except:
                sleep(10)
        sleep(1800)

pthread = threading.Thread(target = proxythread)
pthread.start()
sleep(3)

#第四步，开启各个爬取报表的线程
threadNum = 15
thread_arr = []
for i in range(threadNum):
    t = SpiderThread(i)
    thread_arr.append(t)
for i in range(threadNum):
    thread_arr[i].start()
    sleep(1)
conn.close()