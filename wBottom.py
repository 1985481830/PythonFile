from WindPy import *

def FindExtremumH(Before,After,EH,EHPlusDay):
    for i in range(Before,len(Time)-After,1):
        flagH = True
        for j in range(i-Before,i,1):
            if H[j]>H[i]:
                flagH = False
        if flagH == True:
            flagH = False
            plusDay = 0
            for j in range(i+After,i,-1):
                if L[i]>C[j]:
                    flagH = True
                    plusDay = j-i
        if flagH == True:
            EH.append(i)
            EHPlusDay.append(plusDay)

def FindExtremumL(Before,After,EL,ELPlusDay):
    for i in range(Before,len(Time)-After,1):
        flagL = True
        for j in range(i-Before,i,1):
            if L[j]<L[i]:
                flagL = False
        if flagL == True:
            flagL = False
            plusDay = 0
            for j in range(i+After,i,-1):
                if C[j]>H[i]:
                    flagL = True
                    plusDay = j-i
        if flagL == True:
            EL.append(i)
            ELPlusDay.append(plusDay)


if __name__ == '__main__':
    O = []
    H = []
    L = []
    C = []
    Time = []

    f = open('E:/ZZ500.csv', 'r')
    while True:
        contents = f.readline()
        if not contents:
            break
        else:
            contents = contents.split("\n")[0]
            content = contents.split(",")
            Time.append(content[0])
            O.append(float(content[1]))
            H.append(float(content[2]))
            L.append(float(content[3]))
            C.append(float(content[4]))
    f.close()

    '''w.start()
    KSeries = w.wsd("399905.SZ", "open,high,low,close", "2007-01-01", "2016-03-31", "")

    for i in range(len(KSeries.Data[0])):
        Time.append(KSeries.Times[i].strftime("%Y-%m-%d"))
        O.append(KSeries.Data[0][i])
        H.append(KSeries.Data[1][i])
        L.append(KSeries.Data[2][i])
        C.append(KSeries.Data[3][i])'''

    ExtremumH = []
    ExtremumHPlusDay = []
    ExtremumL = []
    ExtremumLPlusDay = []
    FindExtremumL(6,2,ExtremumL,ExtremumLPlusDay)
    FindExtremumH(6,2,ExtremumH,ExtremumHPlusDay)

    Fund = 100000000
    Future = 0
    MarketValue = 0
    Status = 0  # 0未开仓,1多仓中,-1空仓中
    HSum = 0
    LSum = 0
    Operation = []
    Date = 0

    LLongW = 0
    LShortW = 0
    HLongW = 0
    HShortW = 0
    XBeg = 10770
    XEnd = 13536
    Weight = [0.7,0.5,0.4,0.2]
    XWeight = [-0.7,-0.5,0.4,0.2]

    while Date < len(Time):
        if Status == 0:
            if Date in ExtremumL: #当前是低点
                LSum = LSum + 1
            if Date in ExtremumH:
                HSum = HSum + 1

            if LSum == 2:
                LPos = 0
                for x in range(len(ExtremumL)):
                    if ExtremumL[x] == Date:
                        LPos = x

                if (ExtremumL[LPos] - ExtremumL[LPos - 1]) < 24 and (0.97 < C[ExtremumL[LPos]] / C[ExtremumL[LPos - 1]]) and (C[ExtremumL[LPos]] / C[ExtremumL[LPos - 1]] < 1.03):
                    LSum = 0
                    HSum = 0 #决定开仓，全部清零

                    Date = Date + ExtremumLPlusDay[LPos]

                    HLongW = Weight[0]
                    HShortW = Weight[1]
                    LLongW = Weight[2]
                    LShortW = Weight[3]

                    if Date>=XBeg and Date<=XEnd:
                        HLongW = XWeight[0]
                        HShortW = XWeight[1]
                        LLongW = XWeight[2]
                        LShortW = XWeight[3]


                    if Fund > 110000000:
                        MarketValue = Fund * HLongW
                        Future = Fund * HLongW / C[Date]
                        Fund = Fund * (1-HLongW)
                        Operation.append([Time[Date], '7成开多仓', C[Date], Fund, Future, MarketValue, Date,1])
                    else:
                        MarketValue = Fund * LLongW
                        Future = Fund * LLongW / C[Date]
                        Fund = Fund * (1-LLongW)
                        Operation.append([Time[Date], '4成开多仓', C[Date], Fund, Future, MarketValue, Date,1])
                    Status = 1
                    continue

                else:
                    LSum = 1 #不符合双低点，重新计当前低点为第一个低点

            if HSum == 2:
                HPos = 0
                for x in range(len(ExtremumH)):
                    if ExtremumH[x] == Date:
                        HPos = x

                if (ExtremumH[HPos] - ExtremumH[HPos - 1]) < 24 and (0.97 < C[ExtremumH[HPos]] / C[ExtremumH[HPos - 1]]) and (C[ExtremumH[HPos]] / C[ExtremumH[HPos - 1]] < 1.03):
                    HSum = 0
                    LSum = 0

                    Date = Date + ExtremumHPlusDay[HPos]

                    HLongW = Weight[0]
                    HShortW = Weight[1]
                    LLongW = Weight[2]
                    LShortW = Weight[3]

                    if Date>=XBeg and Date<=XEnd:
                        HLongW = XWeight[0]
                        HShortW = XWeight[1]
                        LLongW = XWeight[2]
                        LShortW = XWeight[3]

                    if Fund > 110000000:
                        MarketValue = Fund * HShortW
                        Future = Fund * HShortW / C[Date]
                        Fund = Fund * (1-HShortW)
                        Operation.append([Time[Date], '5成开空仓', C[Date], Fund, Future, MarketValue, Date,-1])
                    else:
                        MarketValue = Fund * LShortW
                        Future = Fund * LShortW / C[Date]
                        Fund = Fund * (1-LShortW)
                        Operation.append([Time[Date], '2成开空仓', C[Date], Fund, Future, MarketValue, Date,-1])
                    Status = -1
                    continue

                else:
                    HSum = 1

        if Status == 1:
            if Date in ExtremumH:
                HSum = HSum + 1

            CurReturn = H[Date] / Operation[len(Operation) - 1][2]

            if CurReturn >= 1.04:
                Fund = Fund + MarketValue * 1.04
                Future = 0
                MarketValue = 0
                Operation.append([Time[Date], '止盈平多仓', Operation[len(Operation) - 1][2] * 1.04, Fund, Future, MarketValue, Date,0])
                Status = 0
                HSum = 0
                continue

            if CurReturn<=0.98:
                Fund = Fund + MarketValue*0.98
                Future = 0
                MarketValue = 0
                Operation.append([Time[Date], '止损平多仓', Operation[len(Operation)-1][2]*0.98, Fund, Future,MarketValue, Date,0])
                Status = 0
                HSum = 0
                continue

            if HSum == 2: #出现反向信号
                HPos = 0
                for x in range(len(ExtremumH)):
                    if ExtremumH[x] == Date:
                        HPos = x

                if (ExtremumH[HPos] - ExtremumH[HPos-1]) < 24 and (0.97 < C[ExtremumH[HPos]] / C[ExtremumH[HPos-1]]) and (C[ExtremumH[HPos]] / C[ExtremumH[HPos-1]] < 1.03):
                    HSum = 0

                    Fund = Fund + Future * C[Date]
                    Future = 0
                    MarketValue = 0
                    Operation.append([Time[Date], '反向信号出现平多仓', C[Date], Fund, Future, MarketValue, Date,0])
                    Status = 0

                    Date = Date + ExtremumHPlusDay[HPos]

                    HLongW = Weight[0]
                    HShortW = Weight[1]
                    LLongW = Weight[2]
                    LShortW = Weight[3]

                    if Date>=XBeg and Date<=XEnd:
                        HLongW = XWeight[0]
                        HShortW = XWeight[1]
                        LLongW = XWeight[2]
                        LShortW = XWeight[3]

                    if Fund > 110000000:
                        MarketValue = Fund * HShortW
                        Future = Fund * HShortW / C[Date]
                        Fund = Fund * (1-HShortW)
                        Operation.append([Time[Date], '5成开空仓', C[Date], Fund, Future, MarketValue, Date,-1])
                    else:
                        MarketValue = Fund * LShortW
                        Future = Fund * LShortW / C[Date]
                        Fund = Fund * (1-LShortW)
                        Operation.append([Time[Date], '2成开空仓', C[Date], Fund, Future, MarketValue, Date,-1])
                    Status = -1
                    continue

                else:
                    HSum = 1



        if Status == -1:
            if Date in ExtremumL:
                LSum = LSum + 1

            CurReturn = L[Date] / Operation[len(Operation) - 1][2]

            if CurReturn <= 0.96:
                Fund = Fund + MarketValue * 1.04
                Future = 0
                MarketValue = 0
                Operation.append([Time[Date], '止盈平空仓', Operation[len(Operation) - 1][2] * 0.96, Fund, Future, MarketValue, Date,0])
                Status = 0
                LSum = 0
                continue

            if CurReturn >= 1.02:
                Fund = Fund + MarketValue * 0.98
                Future = 0
                MarketValue = 0
                Operation.append([Time[Date], '止损平空仓', Operation[len(Operation) - 1][2] * 1.02, Fund, Future, MarketValue, Date,0])
                Status = 0
                LSum = 0
                continue

            if LSum == 2:
                LPos = 0
                for x in range(len(ExtremumL)):
                    if ExtremumL[x] == Date:
                        LPos = x

                if (ExtremumL[LPos] - ExtremumL[LPos - 1]) < 24 and (0.97 < C[ExtremumL[LPos]] / C[ExtremumL[LPos - 1]]) and (C[ExtremumL[LPos]] / C[ExtremumL[LPos - 1]] < 1.03):
                    LSum = 0

                    Fund = Fund + Future * C[Date]
                    Future = 0
                    MarketValue = 0
                    Operation.append([Time[Date], '反向信号出现平空仓', C[Date], Fund, Future, MarketValue, Date,0])
                    Status = 0

                    Date = Date + ExtremumLPlusDay[LPos]

                    HLongW = Weight[0]
                    HShortW = Weight[1]
                    LLongW = Weight[2]
                    LShortW = Weight[3]

                    if Date>=XBeg and Date<=XEnd:
                        HLongW = XWeight[0]
                        HShortW = XWeight[1]
                        LLongW = XWeight[2]
                        LShortW = XWeight[3]

                    if Fund > 110000000:
                        MarketValue = Fund * HLongW
                        Future = Fund * HLongW / C[Date]
                        Fund = Fund * (1-HLongW)
                        Operation.append([Time[Date], '7成开多仓', C[Date], Fund, Future, MarketValue, Date,1])
                    else:
                        MarketValue = Fund * LLongW
                        Future = Fund * LLongW / C[Date]
                        Fund = Fund * (1-LLongW)
                        Operation.append([Time[Date], '4成开多仓', C[Date], Fund, Future, MarketValue, Date,1])
                    Status = 1
                    continue

                else:
                    LSum = 1

        Date = Date + 1

    dat = 0
    OperationPos = 0
    MK = 0
    Fut = 0
    AFut = 0
    Fun = 100000000
    Value = []
    for dat in range(len(Time)):
        Value.append([Time[dat], Fun + Fut * C[dat], AFut])
        try:
            if dat == Operation[OperationPos][6]:
                Fun = Operation[OperationPos][3]
                Fut = Operation[OperationPos][4]
                AFut = Operation[OperationPos][4]*Operation[OperationPos][7]
                OperationPos = OperationPos + 1
        except:
            pass


    f = open("C:/交易明细.txt","w")
    for i in range(len(Operation)):
        f.write("%s %s %.2f %.2f %.2f %.2f %.2f\n"%(Operation[i][0],Operation[i][1],Operation[i][2],Operation[i][3],Operation[i][4],Operation[i][5],Operation[i][3]+Operation[i][5]))
    f.close()

    f = open("C:/回测结果.txt","w")
    for i in range(len(Time)):
        if (i+1)%8 == 0:
            f.write("%s %.2f %.2f\n"%(Value[i][0],Value[i][1],Value[i][2]))
    f.close()







