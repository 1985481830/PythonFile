from WindPy import *
w.start()
RawData = w.wsd("399905.SZ", "open,high,low,close", "2005-01-04", "2016-04-06", "")
signN = []
signDay = []
Future = []

for i in range(5,len(RawData.Times)-10,1):
    flag = True

    MaxLast5H = max(RawData.Data[1][i - 1], RawData.Data[1][i - 2], RawData.Data[1][i - 3], RawData.Data[1][i - 4],RawData.Data[1][i - 5])
    if RawData.Data[1][i] <= MaxLast5H:
        flag = False

    if RawData.Data[0][i-1]>=RawData.Data[3][i-1]:
        flag = False
    else:
        if RawData.Data[0][i]<=RawData.Data[3][i]:
            flag = False
        else:
            if RawData.Data[0][i]<=RawData.Data[3][i-1]:
                flag = False
            else:
                LastLength = RawData.Data[3][i-1]-RawData.Data[0][i-1]
                Ubound = ((RawData.Data[0][i-1]+RawData.Data[3][i-1])/2)+(LastLength*0.2)
                Lbound = ((RawData.Data[0][i-1]+RawData.Data[3][i-1])/2)-(LastLength*0.2)
                if not (RawData.Data[3][i]>Lbound and RawData.Data[3][i]<Ubound):
                    flag =False
    if flag == True:
        signN.append(i)
        signDay.append(RawData.Times[i].strftime("%Y-%m-%d"))
        F1 = (RawData.Data[3][i+1]/RawData.Data[0][i+1]-1)*100
        F2 = (RawData.Data[3][i+2]/RawData.Data[0][i+2]-1)*100
        F3 = (RawData.Data[3][i+3]/RawData.Data[0][i+3]-1)*100
        F4 = (RawData.Data[3][i+4]/RawData.Data[0][i+4]-1)*100
        F5 = (RawData.Data[3][i+5]/RawData.Data[0][i+5]-1)*100
        F6 = (RawData.Data[3][i + 6] / RawData.Data[0][i + 6] - 1) * 100
        F7 = (RawData.Data[3][i + 7] / RawData.Data[0][i + 7] - 1) * 100
        F8 = (RawData.Data[3][i + 8] / RawData.Data[0][i + 8] - 1) * 100
        F9 = (RawData.Data[3][i + 9] / RawData.Data[0][i + 9] - 1) * 100
        F10 = (RawData.Data[3][i + 10] / RawData.Data[0][i + 10] - 1) * 100
        R10 = (RawData.Data[3][i + 10] / RawData.Data[0][i] - 1) * 100
        Future.append([F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,R10])

'''for i in range(5,len(RawData.Times)-5,1):
    flag = True
    MaxLast5H = max(RawData.Data[1][i-1],RawData.Data[1][i-2],RawData.Data[1][i-3],RawData.Data[1][i-4],RawData.Data[1][i-5])
    if RawData.Data[1][i]<=MaxLast5H:
        flag = False
    if RawData.Data[0][i]<=RawData.Data[1][i-1]:
        flag = False
    if RawData.Data[3][i]>=RawData.Data[2][i-1]:
        flag = False
    if flag == True:
        signN.append(i)
        signDay.append(RawData.Times[i].strftime("%Y-%m-%d"))
        F1 = (RawData.Data[3][i+1]/RawData.Data[0][i+1]-1)*100
        F2 = (RawData.Data[3][i+2]/RawData.Data[0][i+2]-1)*100
        F3 = (RawData.Data[3][i+3]/RawData.Data[0][i+3]-1)*100
        F4 = (RawData.Data[3][i+4]/RawData.Data[0][i+4]-1)*100
        F5 = (RawData.Data[3][i+5]/RawData.Data[0][i+5]-1)*100
        Future.append([F1,F2,F3,F4,F5])'''

f = open("D:/ZZ500result.txt","w")
for i in range(len(signN)):
    f.write("%s %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %3f\n"%(signDay[i],Future[i][0],Future[i][1],Future[i][2],Future[i][3],Future[i][4],Future[i][5],Future[i][6],Future[i][7],Future[i][8],Future[i][9],Future[i][10]))
f.close()