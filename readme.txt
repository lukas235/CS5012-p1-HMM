POSTagger Readme
----------------
In order to run the code from the command-line, follow the subsequent steps:

1. Open a console window and navigate into the directory that contains the .py-files of the project.

2a. Type "python starter.py" in the console windows (without quotations). This will run the script with the default settings i.e. a training set of the first 50.000 words of the corpus, a full tagset and the subsequent 500 sentences as a test set

2b. In order to start the script with arguments, type "python starter.py a b c d" into the console, where

a is the size of the training set (in sentences) (e.g. 50000 for the first 50.000 sentences)
b is the selection of the tagset (0 is the default tagset); other tagsets can be found in the "tagset.py" file.
c start sentence of the test set (e.g. 50000)
d last sentence of the test set (e.g. 50500)


