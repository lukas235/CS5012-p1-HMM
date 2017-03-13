import tagger
import tagset as t
import sys

## Start the script either with 4 arguments (see readme.txt) or in default mode
def main(argv):
    if len(sys.argv) == 5:
        tagger.train(0,int(sys.argv[1]),t.getDefaultTagset(),int(sys.argv[2]))
        tagger.tag(int(sys.argv[3]),int(sys.argv[4]))
    if len(sys.argv) == 4:
        tagger.train(0,int(sys.argv[1]),int(sys.argv[2]))
        tagger.tag(int(sys.argv[3]),int(sys.argv[4]))
    elif len(sys.argv) == 1:
        tagger.train(0,0,5000,0)
        tagger.tag(50000,50500)
    else:
        print "Wrong parameters"

#7136, 15 tags
#6030, 289 tags
if __name__ == "__main__":
   main(sys.argv[1:])
