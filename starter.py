import tagger
import tagset

tagger.train(0,50000,tagset.tagset,0)
tagger.tag(50000,50500)
