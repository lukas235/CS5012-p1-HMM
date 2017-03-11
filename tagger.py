from nltk.corpus import brown
from nltk.util import ngrams
from nltk.probability import FreqDist
import datetime
import re
from math import exp, log
from sys import float_info
import tagset


def train(m,n,t,s):
    global smode
    smode = s
    
    global tags
    tags = tagset.reducetagset(t,smode)
    tags.add('START')
    tags.add('END')

    print "Preparing and re-tagging sentences..."
    global sents
    sents = prepareSents(m,n)
    print "Extracting words..."
    global words
    words = getWords(sents)
    print "Getting tokens..."
    global tokens
    tokens = getTokens(words)
    print "Calculating Types..."
    global types
    types = getTypes(tokens)
    print "Counting Unigram Tags..."
    global fd_uni
    fd_uni = getTagFreqDist(words)
    print "Calculating Transition probabilities..."
    global trans
    trans = getTransitionProbs(sents, tags, fd_uni)
    print "Calculating Emission probabilities..."
    global em
    em = getEmissionProbs(words, types, tags, fd_uni)
    print "Creating dictionary of known words..."
    global known_wds
    known_wds = getKnownWords(types)


def prepareSents(m,n):
    tmp_sents = brown.tagged_sents()[m:n]
    sents = []
    # append start and and tags
    for sen in tmp_sents:
        sents += [[('<s>', 'START')] + tagset.updatetags(sen,smode) + [('</s>', 'END')]]

    # smooth unknown words
    # first convert sentences to words
    tokens = []
    for sen in sents:
        for wd in sen:
            tokens.append(wd[0])

    # get a freqdist & calc the hapax legomena
    fd_tok = FreqDist(tokens)
    hpx_lg = set([e[0] for e in fd_tok.items() if e[1] == 1])

    # update sentences by adding the UNK word
    new_sents = []
    for sen in sents:
        tmp_sen = []
        for wd in sen:
            if wd[0] in hpx_lg:
                tmp_sen.append(('UNK', wd[1]))
            else:
                tmp_sen.append(wd)
        new_sents += [tmp_sen]
    return new_sents

def getWords(sents):
    words = []
    for sen in sents:
        for wd in sen:
            words.append(wd)
    return words

def getTokens(words):
    # create a list of types
    tokens = []
    for wd in words:
        tokens.append(wd[0])
    return tokens

def getTypes(tokens):
    # create a set of types
    return set(tokens)

def getTagFreqDist(words):
    tag_uni = []
    for wd in words:
        tag_uni.append(wd[1])
    return FreqDist(tag_uni)

def getKnownWords(types):
##    known_words = types.copy()
    known_words = types
    known_words.remove('UNK')
    return known_words

    # get the freqdist of the unigrams in the corpus by iterating through every word in every sentence
    # and copying it into a list

    # get the freqdist of the bigram tags in the corpus
def getTransitionProbs(sents, tags, fd_uni):
    tag_bi = []
    for sen in sents:
        tags_only = [wd[1] for wd in sen]
        tag_bi += ngrams(tags_only, 2)

    fd_bi = FreqDist(tag_bi)

    trans = {}
    for t1 in tags:
        for t2 in tags:
            trans[(t1, t2)] = log(float_info.min)
    # calculate transition probabilities & add LaPlace smoothing
    for t1 in tags:
        for t2 in tags:
            prob = 1.0 * (fd_bi[(t1, t2)] + 1) / (fd_uni[t1] + len(tags))
            if prob != 0:
                trans[(t1, t2)] = 1.0 * log(1.0 * (fd_bi[(t1, t2)] + 1) / (fd_uni[t1] + len(tags)))
    return trans

    

    # get the freqdist of the word-tag tuples
def getEmissionProbs(words, types, tags, fd_uni):
    fd_wd = FreqDist(words)
    
    em = {}
    for wd in types:
        for tag in tags:
            em[(wd,tag)] = log(float_info.min)

    # calculate emission probabilities
    for wd in fd_wd.items():
        prob = 1.0 * wd[1] / fd_uni[wd[0][1]]
        if prob != 0:
            em[wd[0]] = 1.0 * log(1.0 * wd[1] / fd_uni[wd[0][1]])
    return em


# add sent before unknown
def viterbi(sen, known_wds, states, p_trans, p_emit):
    # Viterbi as list of dicts
    # Each obs in the list has a dict of state dicts
    # Each state dict has a prob and a backpointer
    V = [{}]
    out = []

    # init
    curr_wd = 'UNK'
    if sen[0] in known_wds:
        curr_wd = sen[0]
    for s in states:
        V[0][s] = p_trans[('START', s)] + p_emit[(curr_wd, s)]

    # run
    for wd in xrange(1, len(sen)):
        V.append({})
        curr_wd = 'UNK'
        if sen[wd] in known_wds:
            curr_wd = sen[wd]
        for s in states:
            V[wd][s] = max(V[wd - 1][last_s] + p_trans[last_s,s] for last_s in states) + p_emit[(curr_wd, s)]

    # backtrack
    maxptr = max(states, key=lambda last_s: V[len(sen)-1][last_s] + p_trans[(last_s,'END')])
    out += [(sen[len(sen) - 1], maxptr)]
    for wd in xrange(len(sen) - 1, 0, -1):
        maxptr = max(states, key=lambda last_s: V[wd-1][last_s] + p_trans[(last_s,maxptr)])
        out = [(sen[wd - 1], maxptr)] + out
    return out

def tag(start,end):
    ref = []
    untagged = brown.sents()[start:end]
    for sen in brown.tagged_sents()[start:end]:
        ref += [tagset.updatetags(sen,smode)]
        
        total_words = 0
        right_words = 0
        tagged_sents = []

    start_time = datetime.datetime.now()
    print start_time
    for i in xrange(start,end):
        tagged_sentence = viterbi(untagged[i-start], types, tags, trans, em)
        reference = ref[i-start]
        tagged_sents += [tagged_sentence]
        
        for wd in xrange(0,len(tagged_sentence)):
            if tagged_sentence[wd][1] == reference[wd][1]:
                right_words += 1
##            else:
##                print tagged_sentence[wd][1]
##                print reference[wd][1]
            total_words += 1

        print "{} / {}".format(i-start+1, end-start)
        print 1.0 * right_words/total_words
        totime = 100 * ((datetime.datetime.now()-start_time).seconds)/60 * (end-start)/(i-start+1)
        print "estimated total time: {}min".format(totime / 100.0)

    end_time = datetime.datetime.now()
    print end_time
    with open("small_tagset_.txt", "w") as f:
        f.write(str(total_words))
        f.write("|")
        f.write(str(right_words))
        f.write("|")
        f.write(str(1.0 * right_words/total_words))
        f.write("\n")
        f.write(str(start_time))
        f.write("\n")
        f.write(str(end_time))
        f.write("\n")

        for sen in tagged_sents:
            f.write("\n")
            f.write(str(sen))
