import tagger
import tagset
import sys

def  main(argv):
    if len(sys.argv) == 5:
        tagger.train(0,int(sys.argv[1]),tagset.tagset,int(sys.argv[2]))
        tagger.tag(int(sys.argv[3]),int(sys.argv[4]))
    elif len(sys.argv) == 1:
        tagger.train(0,50000,tagset.tagset,8)
        tagger.tag(50000,50500)


if __name__ == "__main__":
   main(sys.argv[1:])
