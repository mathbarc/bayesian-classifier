'''
Created on Mar 31, 2015

@author: Matheus
'''
from optparse import OptionParser

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

class Cluster(object):

    def __init__(self, label, points):
        self.label = label
        self.data = points
        self.clustersize = len(self.data)
        self.mean = [0]*len(self.data[0])
        for i in range(0,len(self.data)):
            sumData(self.mean,self.data[i])
        constDiv(self.mean, self.clustersize)
        z = []
        for i in self.data:
            z.append(subData(i,self.mean))
        inz = []
        for i in range(0,len(z[0])):
            inz.append([])
            for j in range(0,len(z)):
                inz[i].append(z[j][i])
        self.cov = []
        for i in range(0,len(z[0])):
            self.cov.append([])
            for j in range(0,len(z[0])):
                s=0
                for k in range(0,len(z)):
                    s = inz[i][k] * z[k][j] + s
                self.cov[i].append(round(s/self.clustersize,2))
            
            
        
    
    
        

def convertLine(l):
    l = l[:-1]
    tmplist = l.split(",")
    rtnlist = []
    for i in range(0,len(tmplist)-1):
        rtnlist.append(float(tmplist[i]))
    label = tmplist[len(tmplist)-1]
    return rtnlist,label

parser = OptionParser();
parser.add_option("-d", "--datafile", dest="datafilename", help="read data from DATAFILENAME")
parser.add_option("-m", "--modelfile", dest="modelfile", help="Name of resulting model file")
options, args = parser.parse_args()

if (options.modelfile):
    if(options.datafilename):
        clusters = []
        data = []
        labels = []
        datafile = open(options.datafilename,'r')
        ndata = 0
        for i in datafile:
            point,clusterlabel = convertLine(i)
            ndata = ndata + 1
            if(clusterlabel in labels):
                ind = labels.index(clusterlabel)
                data[ind].append(point)
            else:
                labels.append(clusterlabel)
                data.append([])
                data[len(data)-1].append(point)
        
        datafile.close()
        for i in range(0,len(labels)):
            clusters.append(Cluster(labels[i],data[i]))
        
        outfile = open(options.modelfile,'w')
        
        for i in clusters:
                outfile.write(i.label)
                outfile.write('\n')
                p = i.clustersize/float(ndata)
                outfile.write(str(round(p,2)))
                outfile.write('\n')
                outfile.write(str(round(i.mean[0],2)))
                for k in range(1,len(i.mean)):
                    outfile.write(", "+ str(round(i.mean[k],2)))
                outfile.write('\n')
                for j in i.cov:
                    line = str(j)[1:-1]
                    outfile.write(line)
                    outfile.write('\n')
                outfile.write("endclass")
                outfile.write('\n')
        
        outfile.close()
    else:
        print("Options missing")
else:
    print("Options missing")