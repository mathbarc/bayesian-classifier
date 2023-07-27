===================
Bayesian Classifier
===================

The bayesian classifier utilizes Bayes Theorem to implement a categorical classifier. The current package contains classes that implement both Full Bayes classifier and Naïve Bayes Classifier, providing a CLI interface as well.

------------------------------------
Runing Bayes Classifier on your data
------------------------------------

.. code-block:: bash

    bayesian_classifier full_bayes train resource/iristrain3.txt --sep ","

.. code-block:: bash

    bayesian_classifier full_bayes test full_bayes.model resource/iristest3.txt
