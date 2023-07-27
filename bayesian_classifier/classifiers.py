import abc
import numpy

class Classifier(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def fit(self, dataset):
        pass

    @abc.abstractmethod
    def save(self, model_file_path):
        pass

    @abc.abstractmethod
    def load(self, model_file_path):
        pass

    @abc.abstractmethod
    def classify(self, sample):
        pass


class FullBayes(Classifier):

    class Group:
        def __init__(self):
            self.label = ""
            self.prior = 0
            self.mean = 0
            self.cov = []
        
        def fit(self, data, label, dataset_size):
            self.mean = numpy.mean(data, axis=0)
            self.label = label
            self.cov = numpy.cov(data.T)
            self.prior = len(data)/dataset_size
        
        def belong_prob(self, sample):
            centered = (sample-self.mean)
            f = (1/( ((numpy.sqrt(2*numpy.pi))**(sample.size) * (numpy.sqrt(numpy.linalg.det(self.cov)))))) * numpy.exp( -0.5*numpy.matmul((numpy.matmul(centered, numpy.linalg.inv(self.cov))), numpy.transpose(centered)))
            return float(f)

    def __init__(self):
        self.groups = []

    def fit(self, dataset, labels):
        self.groups = []
        n_samples = 0
        for data in dataset:
            n_samples += len(data)

        for i, data in enumerate(dataset):
            group = FullBayes.Group()
            group.fit(data, labels[i], n_samples)
            self.groups.append(group)


    def save(self, model_file_path):
        file = open(model_file_path,'w')
        
        for group in self.groups:
            file.write(group.label)
            file.write('\n')
            file.write(str(group.prior))
            file.write('\n')
            file.write(str(group.mean[0]))
            for k in range(1,len(group.mean)):
                file.write(", "+ str(group.mean[k]))
            file.write('\n')
            for j in group.cov:
                line = str(j[0])
                for k in range(1, len(j)):
                    line = line+", "+ str(j[k])
                file.write(line)
                file.write('\n')
            file.write("endclass")
            file.write('\n')
        
        file.close()
    
    @staticmethod
    def convertMatrix(l):
        l = l[:-1]
        tmplist = l.split(",")
        rtnlist = []
        for i in range(0,len(tmplist)):
            rtnlist.append(float(tmplist[i]))
        return rtnlist

    @staticmethod
    def convertMean(l):
        l = l[:-1]
        tmplist = l.split(",")
        rtnlist = []
        for i in range(0,len(tmplist)):
            rtnlist.append(float(tmplist[i]))
        return rtnlist

    def load(self, model_file_path):
        modelfile = open(model_file_path, "r")
        group = FullBayes.Group()
        i=0
        for line in modelfile:
            if (line[:-1] == "endclass"):
                group.cov = numpy.array(group.cov) 
                self.groups.append(group)
                group = FullBayes.Group()
                i=0
            else:
                if (i == 0):
                    group.label = line[:-1]
                else:
                    if(i==1):
                        group.prior = float(line[:-1])
                    else:
                        if(i==2):
                            group.mean = numpy.array(FullBayes.convertMean(line))
                        else:
                            if(i>2):
                                group.cov.append(FullBayes.convertMatrix(line))
                i+=1
    
    def classify(self, sample):
        max_prob = 0
        max_prob_label = ""
        for group in self.groups:
            prob = group.belong_prob(sample)
            if max_prob < prob:
                max_prob_label = group.label
                max_prob = prob
        return max_prob_label



class NaiveBayes(Classifier):

    class Group:
        def __init__(self):
            self.label = ""
            self.prior = 0
            self.mean = 0
            self.var = 0
        
        def fit(self, data, label, dataset_size):
            self.mean = numpy.mean(data, axis=0)
            self.label = label
            self.var = numpy.var(data,axis=0)
            self.prior = len(data)/dataset_size
        
        def belong_prob(self, sample):
            d = len(sample)
            const = 1
            expn = 0
            centered = sample - self.mean
            for i in range(0,len(sample)):
                const *= self.var[i]
                expn += numpy.power(centered[i],2)/(self.var[i]*2)
                
            return self.prior * (1./(numpy.power(numpy.sqrt(2*numpy.pi),d)*numpy.sqrt(const)))*numpy.exp(-expn)


    def __init__(self):
        self.groups = []

    def fit(self, dataset, labels):
        self.groups = []
        n_samples = 0
        for data in dataset:
            n_samples += len(data)

        for i, data in enumerate(dataset):
            group = NaiveBayes.Group()
            group.fit(data, labels[i], n_samples)
            self.groups.append(group)


    def save(self, model_file_path):
        file = open(model_file_path,'w')
        
        for group in self.groups:
            file.write(group.label)
            file.write('\n')
            file.write(str(group.prior))
            file.write('\n')
            file.write(str(group.mean[0]))
            for k in range(1,len(group.mean)):
                file.write(", "+ str(group.mean[k]))
            file.write('\n')
            file.write(str(group.var[0]))
            for k in range(1,len(group.var)):
                file.write(", "+ str(group.var[k]))
            file.write('\n')
            file.write("endclass")
            file.write('\n')
        
        file.close()
    
    @staticmethod
    def convertMatrix(l):
        l = l[:-1]
        tmplist = l.split(",")
        rtnlist = []
        for i in range(0,len(tmplist)):
            rtnlist.append(float(tmplist[i]))
        return rtnlist

    @staticmethod
    def convertMean(l):
        l = l[:-1]
        tmplist = l.split(",")
        rtnlist = []
        for i in range(0,len(tmplist)):
            rtnlist.append(float(tmplist[i]))
        return rtnlist

    def load(self, model_file_path):
        modelfile = open(model_file_path, "r")
        group = NaiveBayes.Group()
        i=0
        for line in modelfile:
            if (line[:-1] == "endclass"): 
                self.groups.append(group)
                group = NaiveBayes.Group()
                i=0
            else:
                if (i == 0):
                    group.label = line[:-1]
                else:
                    if(i==1):
                        group.prior = float(line[:-1])
                    else:
                        if(i==2):
                            group.mean = numpy.array(NaiveBayes.convertMean(line))
                        else:
                            if(i==3):
                                group.var = numpy.array(NaiveBayes.convertMatrix(line))
                i+=1
    
    def classify(self, sample):
        max_prob = 0
        max_prob_label = ""
        for group in self.groups:
            prob = group.belong_prob(sample)
            if max_prob < prob:
                max_prob_label = group.label
                max_prob = prob
        return max_prob_label



if __name__=="__main__":

    from dataset import CSVDataset
    dataset = CSVDataset("resource/iris.txt.shuffled")
    
    classifier = FullBayes()
    classifier.fit(dataset.dataset, dataset.labels)
    classifier.save("test.model")

    classifier2 = FullBayes()
    classifier2.load("test.model")

    correct = 0
    total = 0

    dataset = CSVDataset("resource/iristest3.txt")

    for i in range(0,len(dataset.labels)):
        label = dataset.labels[i]
        for sample in dataset.dataset[i]:
            label_pred = classifier2.classify(sample)
            if label == label_pred:
                correct+=1
            total+=1
    
    print(correct/total)