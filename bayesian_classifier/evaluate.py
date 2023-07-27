import numpy
from .dataset import CSVDataset
from .classifiers import Classifier


def evaluate_model_performance(dataset:CSVDataset, classifier:Classifier):
    confusion_matrix = numpy.zeros((len(dataset.labels), len(dataset.labels)),dtype=int)

    for i in range(0,len(dataset.labels)):
        for sample in dataset.dataset[i]:
            label_pred = classifier.classify(sample)
            j = dataset.labels.index(label_pred)
            confusion_matrix[i,j]+=1

    print(f"Confusion Matrix: \n{confusion_matrix}")


    all_correct = 0
    for i, label in enumerate(dataset.labels):
        correct = confusion_matrix[i,i]
        expected = confusion_matrix[i,:].sum()
        predicted = confusion_matrix[:,i].sum()

        all_correct += correct

        recall = correct/expected
        precision = correct/predicted
        f1score = 2*(recall*precision)/(recall+precision)
        print(label)
        print("Recall", recall)
        print("Precision", precision)
        print("F1Score", f1score)
        print()
    
    print("Accuracy", all_correct/confusion_matrix.sum())

