from nltk.corpus import brown
from nltk.util import ngrams
from nltk.probability import FreqDist
import datetime
import re
from math import exp, log
from sys import float_info

known_words = []
tagset = []
trans_probs = []
em_probs = []

def getSents(start, end):
    sents = []
    for sen in brown.tagged_sents()[start:end]:    
        sents += [[(u'<s>', u'START')] + updatetags(sen,smode) + [(u'</s>', u'END')]]
    return sents

def train():
    
    
    
# Viterbi as list of dicts
# Each obs in the list has a dict of state dicts
# Each state dict has a prob and a backpointer    
def viterbi(sen, known_wds, states, p_trans, p_emit):
    V = [{}]
    out = []
    # init
    curr_wd = u'UNK'
    if sen[0] in known_wds:
        curr_wd = sen[0]
    for s in states:
        V[0][s] = p_trans[('START', s)] + p_emit[(curr_wd, s)]

    # run
    for wd in range(1, len(sen)):
        V.append({})
        curr_wd = u'UNK'
        if sen[wd] in known_wds:
            curr_wd = sen[wd]
        for s in states:
            V[wd][s] = max([V[wd - 1][last_s] + p_trans[last_s,s] for last_s in states]) + p_emit[(curr_wd, s)]

    # backtrack
    maxptr = max(states, key=lambda last_s: V[len(sen)-1][last_s] + p_trans[(last_s,'END')])
    out += [(sen[len(sen) - 1], maxptr)]
    for wd in range(len(sen) - 1, 0, -1):
        maxptr = max(states, key=lambda last_s: V[wd-1][last_s] + p_trans[(last_s,maxptr)])
        out = [(sen[wd - 1], maxptr)] + out

    return out

def tag(start,end):
    start_time = datetime.datetime.now()
    print start_time
    
    ref = []
    for sen in brown.tagged_sents()[start:end]:
        ref += [updatetags(sen,smode)]
        
        total_words = 0
        right_words = 0
        tagged_sents = []

    for i in range(start,end):
        tagged_sentence = viterbi(brown.sents()[i], types, tagset, trans, em)
        reference = ref[i-start]
##        reference = brown.tagged_sents()[i]

        tagged_sents += [tagged_sentence]
        
        for wd in range(0,len(tagged_sentence)):
            if tagged_sentence[wd][1] == reference[wd][1]:
                right_words += 1
            else:
                print tagged_sentence[wd][1]
                print reference[wd][1]
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
    

def reducetagset(tagset, mode):
    tmpset = []

    if mode == 1: # 105
        for t in tagset:
            tmpset.append(re.sub(r"([\+\-][\*\w+].*$)", "", t.encode('ascii', 'ignore')))
        return set(tmpset)
    elif mode == 2: 
        for t in tagset:
            tmpset.append(re.sub(r"(\$)|(\b\*)|(\-\*)", "", t.encode('ascii', 'ignore')))
        return set(tmpset)
    elif mode == 3: # 81
        for t in tagset:
            tmpset.append(re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore')))
        return set(tmpset)
    elif mode == 4: # 47
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"DO\w$", "DO", tmptag)
            tmptag = re.sub(r"DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"HV\w$", "HV", tmptag)
            tmptag = re.sub(r"JJ\w$", "JJ", tmptag)
            tmptag = re.sub(r"NN\w+$", "NN", tmptag)
            tmptag = re.sub(r"NP\w+$", "NP", tmptag)
            tmptag = re.sub(r"NR\w+$", "NR", tmptag)
            tmptag = re.sub(r"PP\w+$", "PP", tmptag)
            tmptag = re.sub(r"QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"WP\w+$", "WP", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 5: # 43
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            if len(tmptag) > 2:
                tmpset.append(tmptag[:2])
            else:
                tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 6: # 29
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^A\w+$", "A", tmptag)
            tmptag = re.sub(r"^BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"^DO\w+$", "DO", tmptag)
            tmptag = re.sub(r"^DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"^HV\w+$", "HV", tmptag)
            tmptag = re.sub(r"^JJ\w+$", "JJ", tmptag)
            tmptag = re.sub(r"^N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"^P\w+$", "P", tmptag)
            tmptag = re.sub(r"^QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"^R\w+$", "R", tmptag)
            tmptag = re.sub(r"^VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"^W\w+$", "W", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 7: # 24
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^A\w+$", "A", tmptag)
            tmptag = re.sub(r"^BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"^DO\w+$", "DO", tmptag)
            tmptag = re.sub(r"^DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"^HV\w+$", "HV", tmptag)
            tmptag = re.sub(r"^JJ\w+$", "JJ", tmptag)
            tmptag = re.sub(r"^N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"^P\w+$", "P", tmptag)
            tmptag = re.sub(r"^QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"^R\w+$", "R", tmptag)
            tmptag = re.sub(r"^VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"^W\w+$", "W", tmptag)
            tmptag = re.sub(r"^[\'\-\)\(\`]{1,2}", "S", tmptag)
            tmptag = re.sub(r"^[\,\.\:]", ".", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 8: # 15
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^A\w*$", "A", tmptag)
            tmptag = re.sub(r"^BE\w*$", "VB", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"^DO\w*$", "VB", tmptag)
            tmptag = re.sub(r"^DT\w*$", "A", tmptag)
            tmptag = re.sub(r"^HV\w*$", "VB", tmptag)
            tmptag = re.sub(r"^JJ\w*$", "JJ", tmptag)
            tmptag = re.sub(r"^MD\w*$", "VB", tmptag)
            tmptag = re.sub(r"^N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"^P\w*$", "P", tmptag)
            tmptag = re.sub(r"^QL\w*$", "JJ", tmptag)
            tmptag = re.sub(r"^R\w*$", "R", tmptag)
            tmptag = re.sub(r"^TO$", "VB", tmptag)
            tmptag = re.sub(r"^UH$", "OD", tmptag)
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag)
            tmptag = re.sub(r"^W\w*$", "R", tmptag)
            tmptag = re.sub(r"^[\'\-\)\(\`]{1,2}", "S", tmptag)
            tmptag = re.sub(r"^[\,\.\:]", ".", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    else:
        return set(tagset)

def updatetags(sen, mode):
    tmpsen = []

    if mode == 1:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", wd[1].encode('ascii', 'ignore'))
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 2:
        for wd in sen:
            tmptag = re.sub(r"(\$)|(\b\*)|(\-\*)", "", wd[1].encode('ascii', 'ignore'))
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 3:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 4:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"DO\w$", "DO", tmptag)
            tmptag = re.sub(r"DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"HV\w$", "HV", tmptag)
            tmptag = re.sub(r"JJ\w$", "JJ", tmptag)
            tmptag = re.sub(r"NN\w+$", "NN", tmptag)
            tmptag = re.sub(r"NP\w+$", "NP", tmptag)
            tmptag = re.sub(r"NR\w+$", "NR", tmptag)
            tmptag = re.sub(r"PP\w+$", "PP", tmptag)
            tmptag = re.sub(r"QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"WP\w+$", "WP", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 5:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            if len(tmptag) > 2:
                tmpsen.append((wd[0],tmptag[:2]))
            else:
                tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 6:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"A\w+$", "A", tmptag)
            tmptag = re.sub(r"BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"DO\w+$", "DO", tmptag)
            tmptag = re.sub(r"DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"HV\w+$", "HV", tmptag)
            tmptag = re.sub(r"JJ\w+$", "JJ", tmptag)
            tmptag = re.sub(r"N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"P\w+$", "P", tmptag)
            tmptag = re.sub(r"QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"R\w+$", "R", tmptag)
            tmptag = re.sub(r"VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"W\w+$", "W", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 7:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"A\w+$", "A", tmptag)
            tmptag = re.sub(r"BE\w+$", "BE", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"DO\w+$", "DO", tmptag)
            tmptag = re.sub(r"DT\w+$", "DT", tmptag)
            tmptag = re.sub(r"HV\w+$", "HV", tmptag)
            tmptag = re.sub(r"JJ\w+$", "JJ", tmptag)
            tmptag = re.sub(r"N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"P\w+$", "P", tmptag)
            tmptag = re.sub(r"QL\w+$", "QL", tmptag)
            tmptag = re.sub(r"R\w+$", "R", tmptag)
            tmptag = re.sub(r"VB\w+$", "VB", tmptag)
            tmptag = re.sub(r"W\w+$", "W", tmptag)
            tmptag = re.sub(r"^[\'\-\)\(\`]{1,2}", "S", tmptag)
            tmptag = re.sub(r"^[\,\.\:]", ".", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 8:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^A\w*$", "A", tmptag)
            tmptag = re.sub(r"^BE\w*$", "VB", tmptag)
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #!
            tmptag = re.sub(r"^CD$", "A", tmptag) #!
            tmptag = re.sub(r"^DO\w*$", "VB", tmptag)
            tmptag = re.sub(r"^DT\w*$", "A", tmptag)
            tmptag = re.sub(r"^HV\w*$", "VB", tmptag)
            tmptag = re.sub(r"^JJ\w*$", "JJ", tmptag)
            tmptag = re.sub(r"^MD\w*$", "VB", tmptag)
            tmptag = re.sub(r"^N[NPR]\w*$", "N", tmptag)
            tmptag = re.sub(r"^P\w*$", "P", tmptag)
            tmptag = re.sub(r"^QL\w*$", "JJ", tmptag)
            tmptag = re.sub(r"^R\w*$", "R", tmptag)
            tmptag = re.sub(r"^TO$", "VB", tmptag)
            tmptag = re.sub(r"^UH$", "OD", tmptag)
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag)
            tmptag = re.sub(r"^W\w*$", "R", tmptag)
            tmptag = re.sub(r"^[\'\-\)\(\`]{1,2}", "S", tmptag)
            tmptag = re.sub(r"^[\,\.\:]", ".", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    else:
        return sen
