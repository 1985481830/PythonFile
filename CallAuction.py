from WindPy import *
import datetime
import time
import collections
begintime = datetime.datetime.strptime("10:26:00","%H:%M:%S")
endtime = datetime.datetime.strptime("10:28:00","%H:%M:%S")
Lock = threading.Lock()

DataSet = collections.OrderedDict()
codestring = []
codeseg = []

seg = 1
targetpercent = 0.6

class CycleGetData(threading.Thread):
    def __init__(self):
        super(CycleGetData,self).__init__()

    def WSQCallback(self,inData):
        if len(inData.Fields) == 1:
            if inData.Fields[0] == "RT_LAST":
                for i in range(len(inData.Codes)):
                    DataSet[inData.Codes[i]].append([inData.Data[0][i],0])
        else:
            for i in range(len(inData.Codes)):
                try:
                    DataSet[inData.Codes[i]].append([inData.Data[0][i],inData.Data[1][i]])
                except:
                    print("%s %s %s"%(inData.Codes[0],inData.Data[0][0],inData.Data[1][0]))

    def run(self):
        Lock.acquire()
        w.wsq(codestring[seg],"rt_last,rt_time",func=self.WSQCallback)

    def stop(self):
        w.cancelRequest(0)
        Lock.release()

w.start()

dat = datetime.datetime.now().strftime("%Y-%m-%d")
AllA = w.wset("sectorconstituent","date="+dat+";windcode=881001.WI").Data[1]

codes = ""
tempseg = []
for x in range(int(len(AllA)/2)-1):
    codes = codes + AllA[x]+ ','
    tempseg.append(AllA[x])
codes = codes + AllA[int(len(AllA)/2)-1]
tempseg.append(AllA[int(len(AllA)/2)-1])
codeseg.append(tempseg)
codestring.append(codes)

codes = ""
tempseg = []
for x in range(int(len(AllA)/2),len(AllA)-1,1):
    codes = codes + AllA[x] + ','
    tempseg.append(AllA[x])
codes = codes + AllA[len(AllA)-1]
tempseg.append(AllA[len(AllA)-1])
codeseg.append(tempseg)
codestring.append(codes)

for x in range(len(codeseg[seg])):
    DataSet[codeseg[seg][x]] = []

datas = w.wsq(codestring[seg],"rt_last,rt_time")

GetDataThread = CycleGetData()
GetDataThread.start()

while True:
    time.sleep(2)
    nowtime = datetime.datetime.strptime(datetime.datetime.now().strftime("%H%M%S"),"%H%M%S")
    if nowtime>endtime:
        GetDataThread.stop()
        Lock.acquire()
        break

MaxUp = w.wsq(codeseg[seg],"rt_high_limit").Data[0]
Res = []

for x in range(len(codeseg[seg])):
    MaxUpTime = datetime.timedelta(0)
    for i in range(len(DataSet[codeseg[seg][x]])-1):
        if abs(DataSet[codeseg[seg][x]][i][0]-MaxUp[x])<0.0001:
            nowtime = datetime.datetime.strptime("%.0f"%DataSet[codeseg[seg][x]][i][1],"%H%M%S")
            nexttime = datetime.datetime.strptime("%.0f"%DataSet[codeseg[seg][x]][i+1][1],"%H%M%S")
            if nowtime > begintime and nexttime < endtime:
                MaxUpTime = MaxUpTime + (nexttime - nowtime)
    i = len(DataSet[codeseg[seg][x]])-1
    if abs(DataSet[codeseg[seg][x]][i][0] - MaxUp[x]) < 0.0001:
        nowtime = datetime.datetime.strptime("%.0f" % DataSet[codeseg[seg][x]][i][1], "%H%M%S")
        if nowtime > begintime and nowtime < endtime:
            MaxUpTime = MaxUpTime + (endtime - nowtime)
    percent = MaxUpTime.total_seconds()/(endtime-begintime).total_seconds()
    if percent >= targetpercent:
        Res.append(codeseg[seg][x])

f = open("C:/Res"+str(seg)+".txt","w")
for x in range(len(Res)):
    f.write("%s\n"%Res[x])
f.close()