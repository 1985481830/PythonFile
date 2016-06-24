from WindPy import *
w.start()

codes = ['CI005027.WI','884114.WI','884039.WI']
#codes = ['CI005027.WI']
tar = []
tarname = []

for x in range(len(codes)):
    windcode = codes[x]
    rawdata = w.wset("sectorconstituent","date=20160503;windcode="+windcode)
    cons = rawdata.Data[1]
    name = rawdata.Data[2]

    stops = w.wset("tradesuspend","startdate=20160503;enddate=20160503").Data[1]

    for i in range(len(cons)):
        flag = True
        for j in range(len(stops)):
            if stops[j] == cons[i]:
                flag = False
        for j in range(len(tar)):
            if tar[j]==cons[i]:
                flag = False
        if flag == True:
            tar.append(cons[i])
            tarname.append(name[i])

ret = []
for i in range(len(tar)):
    temp = w.wsd(tar[i], "close,pre_close", "2016-05-03", "2016-05-03", "")
    ret.append((temp.Data[0][0]/temp.Data[1][0])-1)
total = 0
for i in range(len(ret)):
    total = total + ret[i]
total = total/len(ret)
print(total)