from WindPy import *
import datetime
w.start()

#codearray = [['884200.WI','886063.WI','884114.WI','884039.WI','884076.WI','884086.WI','884214.WI','884162.WI','884116.WI','884109.WI','884119.WI','884160.WI','884161.WI']]
#               高校、          半导体、     充电桩、     锂电池      新能源汽车     稀土永磁      OLED       智能汽车      苹果        石墨烯       3D打印     芯片国产化      传感器
codearray = [['CI005027.WI'],['886063.WI','884114.WI','884039.WI','884076.WI','884086.WI','884214.WI','884162.WI','884116.WI','884109.WI','884119.WI','884160.WI','884161.WI']]
#                 计算机          半导体、     充电桩       锂电池      新能源汽车    稀土永磁      OLED        智能汽车      苹果         石墨烯       3D打印    芯片国产化      传感器
constituentarray = ['计算机','概念股']

blacklist = []

dat = datetime.datetime.now().strftime("%Y%m%d")
stops = w.wset("tradesuspend", "startdate=" + dat + ";enddate=" + dat).Data[1]

for g in range(len(codearray)):
    codes = codearray[g]
    constituentname = constituentarray[g]
    tar = []
    tarname = []
    constituent = []

    for x in range(len(codes)):
        windcode = codes[x]
        rawdata = w.wset("sectorconstituent","date="+dat+";windcode="+windcode)

        cons = []
        name = []

        for i in range(len(rawdata.Data[1])):
            if rawdata.Data[1][i][0] in ['0','3','6']:
                cons.append(rawdata.Data[1][i])
                name.append(rawdata.Data[2][i])

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
                constituent.append(codes[x])


    fc = open("C:/CAT"+constituentname+dat+".csv","w")
    fx = open("C:/迅投"+constituentname+dat+".csv","w")
    fx.write("代码,名称,数量,权重,方向\n")
    weight = 1/len(tar)

    for i in range(len(tar)):
        str1 = tarname[i][0:1]
        str2 = tarname[i][0:2]
        str3 = tarname[i][0:3]
        str4 = tarname[i][0:4]
        flag = True
        if str1 == "S" or str2 == "ST" or str3 == "SST" or str3 == "*ST" or str4 == "S*ST":
            flag = False
        if tar[i][0:6] in blacklist:
            flag = False
        if flag == True:
            if i == len(tar)-1:
                fc.write("%s,%s,100,0,0,add"%(tar[i],tarname[i]))
                fx.write("%s,%s,,%.9f,0"%(tar[i][0:6],tarname[i],weight))
            else:
                fc.write("%s,%s,100,0,0,add\n" % (tar[i], tarname[i]))
                fx.write("%s,%s,,%.9f,0\n" % (tar[i][0:6], tarname[i], weight))
    fc.close()
    fx.close()