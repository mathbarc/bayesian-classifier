import click
import os
from .dataset import CSVDataset
from .classifiers import NaiveBayes, FullBayes
from .evaluate import evaluate_model_performance


@click.group()
def cli():
    pass

@cli.group("naive_bayes")
def naive_bayes_group():
    pass

@naive_bayes_group.command(name="train")
@click.argument("dataset",nargs=1, type=str)
@click.option("--sep", required=False, type=str, default=",")
@click.option("--output", required=False, type=str, default="naive_bayes.model")
def train_naive_bayes(dataset, sep, output):
    if not os.path.exists(dataset):
        raise Exception(f"File {dataset} not found")

    dataset = CSVDataset(dataset, sep)
    classifier = NaiveBayes()
    classifier.fit(dataset.dataset, dataset.labels)
    classifier.save(output)
    
@naive_bayes_group.command(name="test")
@click.argument("model",nargs=1, type=str)
@click.argument("dataset",nargs=1, type=str)
@click.option("--sep", required=False, type=str, default=",")
def test_naive_bayes(model, dataset, sep):
    if not os.path.exists(model):
        raise Exception(f"File {model} not found")
    
    classifier = NaiveBayes()
    classifier.load(model)
    
    if not os.path.exists(dataset):
        raise Exception(f"File {dataset} not found")

    dataset = CSVDataset(dataset, sep)
    evaluate_model_performance(dataset, classifier)


@cli.group("full_bayes")
def full_bayes_group():
    pass

@full_bayes_group.command(name="train")
@click.argument("dataset",nargs=1, type=str)
@click.option("--sep", required=False, type=str, default=",")
@click.option("--output", required=False, type=str, default="full_bayes.model")
def train_full_bayes(dataset, sep, output):
    if not os.path.exists(dataset):
        raise Exception(f"File {dataset} not found")

    dataset = CSVDataset(dataset, sep)
    classifier = FullBayes()
    classifier.fit(dataset.dataset, dataset.labels)
    classifier.save(output)

@full_bayes_group.command(name="test")
@click.argument("model",nargs=1, type=str)
@click.argument("dataset",nargs=1, type=str)
@click.option("--sep", required=False, type=str, default=",")
def test_full_bayes(model, dataset, sep):
    if not os.path.exists(model):
        raise Exception(f"File {model} not found")
    
    classifier = FullBayes()
    classifier.load(model)
    
    if not os.path.exists(dataset):
        raise Exception(f"File {dataset} not found")

    dataset = CSVDataset(dataset, sep)
    evaluate_model_performance(dataset, classifier)


if __name__=="__main__":
    cli()