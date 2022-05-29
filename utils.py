def subData(v1,v2):
    result = []
    for i in range(0,len(v1)):
        result.append(v1[i]-v2[i])
    return result

def sumData(v1,v2):
    for i in range(0,len(v1)):
        v1[i] = v1[i]+v2[i]
    

def constDiv(v,c):
    for i in range(0,len(v)):
        v[i] = v[i]/c


def convertLine(l):
    l = l[:-1]
    tmplist = l.split(",")
    rtnlist = []
    for i in range(0,len(tmplist)-1):
        rtnlist.append(float(tmplist[i]))
    label = tmplist[len(tmplist)-1]
    return rtnlist,label

def convertMatrix(l):
    l = l[:-1]
    tmplist = l.split(",")
    rtnlist = []
    for i in range(0,len(tmplist)):
        rtnlist.append(float(tmplist[i]))
    return rtnlist

def convertMean(l):
    l = l[:-1]
    tmplist = l.split(",")
    rtnlist = []
    for i in range(0,len(tmplist)):
        rtnlist.append(float(tmplist[i]))
    return rtnlist