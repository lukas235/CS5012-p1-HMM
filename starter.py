import tagger
import tagset as t
import sys

## Start the script either with 4 arguments (see readme.txt) or in default mode
def main(argv):
    if len(sys.argv) == 5:
        tagger.train(0,int(sys.argv[1]),t.getDefaultTagset(),int(sys.argv[2]))
        tagger.tag(int(sys.argv[3]),int(sys.argv[4]))
    elif len(sys.argv) == 1:
        tagger.train(0,50000,t.getDefaultTagset(),12)
        tagger.tag(50000,50500)
    else:
        print "Wrong parameters"


if __name__ == "__main__":
   main(sys.argv[1:])
