from nltk.corpus import brown
from nltk.util import ngrams
from nltk.probability import FreqDist




start = u'<s>'
end = u'</s>'

sents = []

# noch end tags und so auf die words packen?
#
# Look for words that occur only once
# replace them by artificial UNK
#
##fd_words = FreqDist(brown.tagged_words()[:5000])
##
##once = set([e[0] for e in fd_words.iteritems() if e[1] == 1])
##
##for sen in brown.tagged_sents()[:5000]:
##    tmp_sen = [(start,u'START')] # add start
##    for wd in sen:
##        if wd in once:
##            tmp_sen.append((u'UNK',wd[1]))
##        else:
##            tmp_sen.append(wd)
##    tmp_sen.append((end, u'END'))
##    sents.append(tmp_sen)

sents = brown.tagged_sents()[:5000]


# frequency of single tags
tag_uni = []
tag_bi = []
tag_wd = []

# [[wd[1] for wd in sen] for sen in sents] 
for sen in sents:
    for wd in sen:
        tag_uni.append(wd[1]) # tag only

fd_uni = FreqDist(tag_uni)

# freqencies of tag bigrams
for sen in sents:
    tags_only = [wd[1] for wd in sen]
    tag_bi+=ngrams(tags_only,2)

fd_bi = FreqDist(tag_bi)

# frequencies of the words tag tuples
for sen in sents:
    for wd in sen:
        tag_wd.append(wd)

fd_wd = FreqDist(tag_wd)

# get relative frequency distributions
ptt = {}

pwt = {}

for bi in fd_bi.iteritems():
    ptt[bi[0]] = bi[1]*1.0/fd_uni[bi[0][0]]

for wd in fd_wd.iteritems():
    pwt[wd[0]] = wd[1]*1.0/fd_uni[bi[0][0]]


    

    









    
