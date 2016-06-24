rawf = "E:/AllA.csv"
dupf = "E:/already.csv"

raw = open(rawf,"r")
dup = open(dupf,"r")

rawcontent = []
dupcontent = []

while True:
    content = raw.readline()
    if not content:
        break
    else:
        content = content.split("\n")[0]
        rawcontent.append(content)

while True:
    content = dup.readline()
    if not content:
        break
    else:
        content = content.split("\n")[0]
        dupcontent.append(content)
res = []
for x in range(len(rawcontent)):
    if rawcontent[x] in dupcontent:
        pass
    else:
        res.append(rawcontent[x])

re = open("C:/stocklist.csv","w")
for x in range(len(res)):
    re.write("%s\n"%res[x])
re.close()