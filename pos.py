from nltk.corpus import brown
from nltk.util import ngrams
from nltk.probability import FreqDist


tagset = set([t for (w,t) in brown.tagged_words()[:50000]]) # spaeter aendern noch START UND END REIN
tagset = tagset.union(u'START')
tagset = tagset.union(u'END')


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

for sen in brown.tagged_sents()[:5000]:
    sents += [[(start,u'START')] + sen + [(end, u'END')]]



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

# get relative frequency distributions // ggf noch divby0 betrachten
##ptt = {}
##
##pwt = {}
##
##for bi in fd_bi.iteritems():
##    ptt[bi[0]] = bi[1]*1.0/fd_uni[bi[0][0]]
##
##for wd in fd_wd.iteritems():
##    pwt[wd[0]] = wd[1]*1.0/fd_uni[bi[0][0]]

#change the value of key (=[0] element) to relative prob
for bi in fd_bi.iteritems():
    fd_bi[bi[0]] = bi[1]*1.0/fd_uni[bi[0][0]]

for wd in fd_wd.iteritems():
    fd_wd[wd[0]] = wd[1]*1.0/fd_uni[wd[0][1]]


##     

def viterbi(sen, states, p_trans, p_emit):
    V = [{}] # Viterbi as list of dicts
    out = []
    # Each obs has a dict of states
    # Each state has a dict of probs and a backpointer
    
    # init
    for s in states:
        V[0][s] = {'p': 1.0 * p_trans[('START',s)] * p_emit[(sen[0],s)], 'bckptr': None}

    print V[0]
    print "x"
    print "x"
    print "x"
    print "x"

    # run
    for wd in range(1,len(sen)): # for every word in sentence until the last word
        V.append({})
        for s in states:
            maxp = 0
            maxptr = None
            for last_s in states:
                curr_p = 1.0 * V[wd-1][last_s]['p'] * p_trans[(last_s,s)] * p_emit[(sen[wd],s)]
                if curr_p > maxp:
                    maxp = curr_p
                    maxptr = last_s    
            V[wd][s] = {'p': maxp, 'backptr': maxptr}
        print V[wd]
        print 'x'
        print 'x'
        print 'x'

    print V[len(sen)-1]  
    # term & bt
    maxp = 0
    maxptr = None
    for last_s in states:
        curr_p = 1.0 * V[len(sen)-1][last_s]['p'] * p_trans[(last_s,'END')]
        if curr_p > maxp:
            maxp = curr_p
            maxptr = last_s
    #V[len(sen)]['END'] = {'p': maxp, 'backptr': maxptr}

    print maxptr
    for wd in range(len(sen)-1,0,-1):
        print V[wd][maxptr]['backptr']
        maxptr = V[wd][maxptr]['backptr']

# viterbi(brown.sents()[1], tagset, fd_bi, fd_wd)

def getOneBi(tag):
    a = 0
    for i in fd_bi.iteritems():
        if i[0][0] == tag:
            a+=i[1]
    return a

def getOneWd(tag):
    a=0
    for i in fd_wd.iteritems():
        if i[0][1] == tag:
            a+=i[1]
    return a
