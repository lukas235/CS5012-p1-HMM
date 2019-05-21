import tagger
import tagset as t
import sys

## Start the script either with 4 arguments (see readme.txt) or in default mode

# arg 1: choose corpus, 0 brown, 1 alpino, 2 cess_esp
# arg 2: choose size of training set e.g. 50000
# arg 3: select reduction mode for tagset; 0 is the full tagset, 1 without compounds ... (see tagset.py)
# arg 4: start sentence to tag
# arg 5: end sentence to tag

def main(argv):
    if len(sys.argv) == 6:
        tagger.train(int(sys.argv[1]),0,int(sys.argv[2]),int(sys.argv[3]))
        tagger.tag(int(sys.argv[4]),int(sys.argv[5]))
    elif len(sys.argv) == 1:
        tagger.train(0,0,50000,0)
        tagger.tag(50000,50500)
    else:
        print "Wrong parameters"

if __name__ == "__main__":
   main(sys.argv[1:])
