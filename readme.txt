Readme
----------------
In order to run the code from the command-line, follow the subsequent steps:

1. Open a console window and navigate into the directory that contains the .py-files of the project.

2a. Type "python starter.py" in the console windows (without quotations). This will run the script with the default settings i.e. a training set of the first 50.000 words of the corpus, a full tagset and the subsequent 500 sentences as a test set

2b. In order to start the script with arguments, type "python starter.py a b c d e" into the console, where

The 5 parameters:
a: is for selecting the corpus: 0 for brown, 1 for alpino, 2 for cess_esp
b: is the size of the training set (in sentences) (e.g. 50000 for the first 50.000 sentences)
c: is the selection of the tagset (0 is the default (full) tagset); other tagset settings which were used for the tagset experiments for the brown corpus can be found in the "tagset.py" file. (e.g. 1 merges all the compound tags)
d: start sentence of the test set (e.g. 50000)
e: last sentence of the test set (e.g. 50500)


