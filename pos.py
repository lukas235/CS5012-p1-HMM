from nltk.corpus import brown
from nltk.util import ngrams
#from collections import defaultdict
from nltk.probability import FreqDist




start = u'<s>'
end = u'</s>'

tag_sents = brown.tagged_sents()
#tagset = set([t for (_,t) in brown.tagged_words()[:50000]]) # spaeter aendern noch START UND END REIN

bigrams = []
unigrams = []
tagwords = []

##for sen in tag_sents[:500]:
##    curr_sen = [(start,u'START')] + sen + [(end, u'END')]
##    tagwords += [(tag,word) for (tag,word) in curr_sen]
##


for sen in tag_sents[:500]:
    tagwords += [(tag,word) for (tag,word) in sen]


# trenne die woerter je nach dem ob sie einmal oder nicht appearen
fd_tag = FreqDist(brown.tagged_words())

once = []
notonce = []

for e in fd_tag.iteritems():
	if e[1]==1:
		once.append(e[0])
	else:
		notonce.append(e)


# for every tuple that appears once, replace the word by UNK
##unklist = []
##for e in once:
##    unklist.append((u'UNK',e[1]))
##
##fd_unk = FreqDist(unklist)
##
##for e in fd_unk.iteritems():
##    notonce.append(e)

setonce = set(once)

tag_sents_unk = []

for sen in tag_sents:
    for wd in sen:
        if wd[0] in setonce:
            wd = (u'UNK', wd[1])

    





# get all tag unigrams and tag bigrams including start and end markers
##for sen in tag_sents[:500]:
##    curr_sen = [(start,'START')] + sen + [(end, 'END')]
##    curr_tags = [t for (_,t) in curr_sen]
##    bigrams += ngrams(curr_tags, 2)
##    unigrams += curr_tags
##    tagwords += [ (tag,word) for (tag,word) in curr_sen]

    

# calc the freqdists
fd_uni = FreqDist(unigrams)
fd_bi = FreqDist(bigrams)


# smooth unknown words
# transfer freqdist to lists
##fd_uni_list = [(k,v) for k,v in fd_uni.iteritems()]
##fd_bi_list = [(k,v) for k,v in fd_bi.iteritems()]
##fd_tag_list = [(k,v) for k,v in fd_tag.iteritems()]

#x = [(k,v+1) for k,v in fd_tag.iteritems()]



def getTransProb(key):
    return fd_bi[key]/1.0/fd_uni[key[0]]

