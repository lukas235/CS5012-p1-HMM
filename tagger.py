from nltk.corpus import brown
from nltk.corpus import alpino
from nltk.corpus import cess_esp
from nltk.util import ngrams
from nltk.probability import FreqDist
from math import exp, log
from sys import float_info
from collections import defaultdict
import operator
import datetime
import re
import tagset


# Initiate the training sequence
# m: start sentence of the training set
# n: end sentence of the training set
# t: tagset which shall be used
# s: selection mode of the tags from the original tagset t (see tagset.py)
def train(c,m,n,s):
    global corp
    if c == 0:
        corp = brown
    elif c == 1:
        corp = alpino
    elif c == 2:
        corp = cess_esp
    
    
    global smode
    smode = s

    print "Getting full tagset from corpus"
    global full_tags
    full_tags = list(set([t for (w,t) in corp.tagged_words()[:n]]))
    global tags
    if smode != 0:
        print "Reducing tagset..."
    tags = tagset.reducetagset(full_tags,smode)
    tags.add('START')
    tags.add('END')

    print "Preparing and re-tagging sentences..."
    global sents
    sents = prepareSents(m,n)
    
    print "Extracting word-tag tuples from sentences..."
    global words
    words = getWords(sents)
    
    print "Extracting words from tuples..."
    global tokens
    tokens = getTokens(words)
    
    print "Getting word types..."
    global types
    types = getTypes(tokens)
    
    print "Counting tag unigrams..."
    global fd_uni
    fd_uni = getTagFreqDist(words)
    
    print "Calculating Transition probabilities..."
    global trans
    trans = getTransitionProbs(sents, tags, fd_uni)
    
    print "Calculating Emission probabilities..."
    global em
    em = getEmissionProbs(words, types, tags, fd_uni)
    
    print "Creating lexicon of known words..."
    global known_wds
    known_wds = getKnownWords(types)

# Preprocess sentences
# 1. Modify tagset in terms of size and add start, and end tags
# 2. Deal with unknown words by extracting the hapax legomena and replace every hapax legomenon in the training set with UNK
def prepareSents(m,n):
    tmp_sents = corp.tagged_sents()[m:n]
    sents = []
    for sen in tmp_sents:
        sents += [[('<s>', 'START')] + tagset.updatetags(sen,smode) + [('</s>', 'END')]]

    # handle unknown words
    # first convert sentences to words and only get the word itself from the tuple
    tokens = []
    for sen in sents:
        for wd in sen:
            tokens.append(wd[0])

    # calculate a freqdist & calc the hapax legomena
    fd_tok = FreqDist(tokens)
    hpx_lg = set([e[0] for e in fd_tok.items() if e[1] == 1])

    # update sentences by replacing all words with UNK that are in the hpx_lg set
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

# Return (word, tag) tuples from sentences
def getWords(sents):
    words = []
    for sen in sents:
        for wd in sen:
            words.append(wd)
    return words

# Return word-only tokens from (word, tag) tuples
def getTokens(words):
    tokens = []
    for wd in words:
        tokens.append(wd[0])
    return tokens

# Create a set of types from the tokens
def getTypes(tokens):
    return set(tokens)

# Get absolute frequency distribution of the tag unigrams
def getTagFreqDist(words):
    tag_uni = []
    for wd in words:
        tag_uni.append(wd[1])
    return FreqDist(tag_uni)

# Return the lexicon of known words
def getKnownWords(types):
##    known_words = types.copy()
    known_words = types
    known_words.remove('UNK')
    return known_words

# Calculate the transition probabilities in the log domain
# For the count of every tag bigram divide through the unigram count of the first tag in the tuple
# Smooth with LaPlace
def getTransitionProbs(sents, tags, fd_uni):
    tag_bi = []
    for sen in sents:
        tags_only = [wd[1] for wd in sen]
        tag_bi += ngrams(tags_only, 2)
    fd_bi = FreqDist(tag_bi)

    # Initialise transitions table
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

    

# Calculate the emission probabilities in the log domain
# For the count of every word-tag tuple divide by the count of the tag unigram
def getEmissionProbs(words, types, tags, fd_uni):
    fd_wd = FreqDist(words)

    # Initialise emissions table
    em = {}
    for wd in types:
        for tag in tags:
            em[(wd,tag)] = log(float_info.min)

    # calculate emission probabilities in the log domain
    for wd in fd_wd.items():
        prob = 1.0 * wd[1] / fd_uni[wd[0][1]]
        if prob != 0:
            em[wd[0]] = 1.0 * log(1.0 * wd[1] / fd_uni[wd[0][1]])
    return em


# Implementation of the Viterbi algorithm as list of dicts
# Every word is represented as an entry in a list with a dictionary of states (i.e. tags)
# The viterbi algorithm is extended by checking if each word exists in the lexicon of known words
def viterbi(sen, known_wds, states, p_trans, p_emit):
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

    # terminate
    maxptr = max(states, key=lambda last_s: V[-1][last_s] + p_trans[(last_s,'END')])

    # backtrack
    out += [(sen[len(sen) - 1], maxptr)]
    for wd in xrange(len(sen) - 1, 0, -1):
        maxptr = max(states, key=lambda last_s: V[wd-1][last_s] + p_trans[(last_s,maxptr)])
        out = [(sen[wd - 1], maxptr)] + out
    return out

# Start tagging a 
def tag(start,end):
    ref = [] # tagged reference sentences
    untagged = corp.sents()[start:end] # untagged sentences which shall be tagged
    
    for sen in corp.tagged_sents()[start:end]:
        ref += [tagset.updatetags(sen,smode)]
        
    total_words = 0
    right_words = 0
    tagged_sents = []

    start_time = datetime.datetime.now()
    print start_time

    # Run Viterbi for every sentence in the test set
    for i in xrange(start,end):
        tagged_sentence = viterbi(untagged[i-start], types, tags, trans, em)
        reference = ref[i-start]
        tagged_sents += [tagged_sentence]

        # Count total words and right words
        for wd in xrange(0,len(tagged_sentence)):
            if tagged_sentence[wd][1] == reference[wd][1]:
                right_words += 1
            total_words += 1

        
        print "{} / {}".format(i-start+1, end-start)
        print 1.0 * right_words/total_words
        totime = 100 * ((datetime.datetime.now()-start_time).seconds)/60 * (end-start)/(i-start+1)
        print "estimated total time: {}min".format(totime / 100.0)

    end_time = datetime.datetime.now()
    print end_time
    
    # Save result as txt
    with open("result.txt", "w") as f:
        f.write("{}/{}|{}\n".format(str(right_words), str(total_words), str(1.0 * right_words/total_words)))
        f.write(str(start_time))
        f.write("\n")
        f.write(str(end_time))
        f.write("\n")
        for sen in tagged_sents:
            f.write("\n")
            f.write(str(sen))
            
    test(ref, tagged_sents)

def test(reference, tagged_sents):
    acc = defaultdict(float)
    acc_tot = defaultdict(float)
    
    for sent in xrange(0,len(tagged_sents)):
        for wd in xrange(0,len(tagged_sents[sent])):
            if tagged_sents[sent][wd][1] == reference[sent][wd][1]:
                acc[tagged_sents[sent][wd][1]] += 1
            acc_tot[tagged_sents[sent][wd][1]] += 1

    acc_rel = defaultdict(float)
    for ac in acc.items():
        acc_rel[ac[0]] = 1.0 * ac[1] / acc_tot[ac[0]]
    sorted_acc_rel = sorted(acc_rel.items(), key=operator.itemgetter(1))

    for i in sorted_acc_rel:
        print "{} {}".format(i[0], i[1])
