import numpy

class CSVDataset:
    def __init__(self, csv_file_path, separator=","):
        self._data = []
        self._labels = []
        datafile = open(csv_file_path,'r')
        for i in datafile:
            point,clusterlabel = CSVDataset._convertLine(i, separator)
            if(clusterlabel in self._labels):
                ind = self._labels.index(clusterlabel)
                self._data[ind].append(point)
            else:
                self._labels.append(clusterlabel)
                self._data.append([])
                self._data[len(self._data)-1].append(point)
        
        for i in range(0,len(self._data)):
            self._data[i] = numpy.array(self._data[i])

        
        datafile.close()
    
    @staticmethod
    def _convertLine(l, separator=","):
        l = l[:-1]
        tmplist = l.split(separator)
        rtnlist = []
        for i in range(0,len(tmplist)-1):
            rtnlist.append(float(tmplist[i]))
        label = tmplist[len(tmplist)-1]
        return numpy.array(rtnlist),label

    @property
    def dataset(self):
        return self._data

    @property
    def labels(self):
        return self._labels
    
if __name__=="__main__":
    dataset = CSVDataset("resource/iristrain1.txt")
    print(numpy.mean(dataset.dataset[0],axis=0))
    cov = numpy.cov(numpy.array(dataset.dataset[0]).T)
    print(cov)
    ...