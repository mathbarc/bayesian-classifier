'''
Created on Apr 1, 2015

@author: Matheus
'''

import numpy
from utils import convertLine,convertMatrix,convertMean

class NaiveBayesianModel(object):
    def __init__(self, label, prior_probability, mean, cov):
        self.label = label
        self.pp = prior_probability
        self.mean = mean
        self.cov = cov
    
    def probability_density(self,x):
        f = 1.0
        for i in range(0,len(x)):
            f = f * (1/(numpy.sqrt(2*numpy.pi*self.cov[i])))*numpy.exp((-0.5*((x[i] - self.mean[i])**2)/self.cov[i]))
        return f
        


if __name__=="__main__":
    from optparse import OptionParser 
    parser = OptionParser();
    parser.add_option("-m", "--modelfile", dest="modelfile", help="Name of model file")
    parser.add_option("-t", "--testfile", dest="testfile", help="read test data from TESTFILENAME")
    options, args = parser.parse_args()

    if (options.modelfile):
        if(options.testfile):
        
            Classes = []
            modelfile = open(options.modelfile,'r')
            i = 0
            label = ""
            pp = 0.0
            mean = []
            labels = []
            referencelabelposition = []
            cov = []
            for line in modelfile:
                if (line[:-1] == "endclass"): 
                    Classes.append(NaiveBayesianModel(label,pp,mean,cov))
                    referencelabelposition.append(label)
                    i=0
                else:
                    if (i == 0):
                        label = line[:-1]
            
                    else:
                        if(i==1):
                            pp = float(line[:-1])
                        else:
                            if(i==2):
                                mean = numpy.array(convertMean(line))
                            else:
                                if(i==3):
                                    cov = numpy.array(convertMatrix(line))
                                
                            
                        
                    
                    i=i+1
            modelfile.close()
            prob = []
            predictedlabels = []
            ndataset = 0
            testfile = open(options.testfile,'r')
            for line in testfile:
                lp,label = convertLine(line)
                point = lp
                for c in Classes:
                    prob.append(c.probability_density(point)*c.pp)
                maxp = prob[0]
                pm = 0
                for i in range(1,len(prob)):
                    if(prob[i]>maxp):
                        pm = i
                        maxp = prob[i]
                predictedlabels.append(Classes[pm].label)
                labels.append(label)
                prob = []
                ndataset = ndataset + 1
            testfile.close()
            cm = []
            for i in range(0,len(Classes)):
                cm.append([])
                for j in range(0,len(Classes)):
                    cm[i].append(0)
            
            for il in range(0,len(predictedlabels)):
                pp = referencelabelposition.index(predictedlabels[il])
                rp = referencelabelposition.index(labels[il])
                cm[pp][rp] = cm[pp][rp] + 1
                
            
            
            precision = []
            for i in cm:
                tmp = float(i[0])
                maxv = i[0]
                for j in range(1,len(i)):
                    tmp = tmp + i[j]
                    if (i[j]>maxv):
                        maxv = i[j]
                if(tmp!=0):
                    precision.append(maxv/tmp)
                else:
                    precision.append(0)
            
            recall = []
            for j in range(0,len(cm[0])):
                tmp = float(cm[0][j])
                maxv = cm[0][j]
                for i in range(1,len(cm)):
                    tmp = tmp+cm[i][j]
                    if(cm[i][j]>maxv):
                        maxv = cm[i][j]
                if(tmp!=0):
                    recall.append(maxv/tmp)
                else:
                    recall.append(0)
            
            Fmeasure = []
            accuracy = 0.0
            for i in range(0,len(precision)):
                Fmeasure.append((2*precision[i]*recall[i])/(precision[i]+recall[i]))
                accuracy = cm[i][i] + accuracy
            accuracy = accuracy/ndataset
            
            print(referencelabelposition)
            print("Accuracy:", accuracy)
            print("Confusion Matrix:", numpy.matrix(cm))
            print("Precision:", numpy.matrix(precision))
            print("Recall:", numpy.matrix(recall))
            print("F-Measure:", numpy.matrix(Fmeasure))
        else:
            print("Options missing")
    else:
        print("Options missing")