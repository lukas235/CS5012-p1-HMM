import re

# The function reduces the default tagsets in different ways
# The amount of tags excludes START and END tag
# mode 1 (105 tags): Reduce compound tags (e.g. 'JJR-HL' or 'FW-IN+NP-TL' to 'JJR' and 'FW')
# mode 2: Only remove $ and *
# mode 3: mode 1 + 2 combined
# mode 4: mode 3 + concentrate all most of the 3-letter tags to 2-letters
# mode 5: naive cut-off of the 3rd letter if existent
# mode 6: reduce most of the tags to one letter
# mode 7: concentrate non-word characters such as brackets, hyphens and quotation marks
# mode 8 (15 tags): extreme concentration of characters

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
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #! tmptag = re.sub(r"^C\w+$", "C", tmptag)
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
    elif mode == 9:
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?", "N", tmptag) # merge all nouns
            tmptag = re.sub(r"^P\w+", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 10:
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?\$?", "N", tmptag) # merge all nouns + $
            tmptag = re.sub(r"^P\w+\${,2}", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
##            tmptag = re.sub(r"^QLP$", "QL", tmptag) # merge QLP to QL
##            tmptag = re.sub(r"(^BEG$)|(^HVN$)", "VB", tmptag) # being and having to vbs
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 11:
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?\$?", "N", tmptag) # merge all nouns + $
            tmptag = re.sub(r"^P\w+\${,2}", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
            tmptag = re.sub(r"^BE.*$", "BE", tmptag) # merge be
            tmptag = re.sub(r"^HV.*$", "HV", tmptag) # merge have
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 12:
        for t in tagset:
            tmptag = re.sub(r"^JJ.*$", "JJ", t.encode('ascii', 'ignore'))
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 13:
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^[\,\.\:\'\-\)\(\`]{1,2}$", "punct", tmptag)
            tmptag = re.sub(r"(^A[BP]\w?$)|(^JJ\w?$)", "adj", tmptag)
            tmptag = re.sub(r"(^\*$)|(^EX$)|(^QL$)|(^RB[RT]?$)", "adv", tmptag)
            tmptag = re.sub(r"^RP$", "part", tmptag)
            tmptag = re.sub(r"(^CS$)|(^TO$)", "comp", tmptag)
            tmptag = re.sub(r"(^AT$)|(^DT[IS]?$)|(^PPL$)|(^PP$)|(^PPLS$)|(^WDT$)|(^WPO$)|(^WPS$)|(^WRB$)", "det", tmptag)
            tmptag = re.sub(r"^FW$", "fixed", tmptag)
##            tmptag = re.sub(r"^NP$", "name", tmptag)
            tmptag = re.sub(r"(^NN$)|(^NP$)(^NNS$)|(^NPS$)|(^NR$)|(^PN$)|(^PPO$)|(^PPS{1,2}$)", "noun", tmptag)
            tmptag = re.sub(r"(^CD$)|(^OD$)", "num", tmptag)
            tmptag = re.sub(r"^IN$", "prep", tmptag)
            tmptag = re.sub(r"(^BE\w{0,2}$)|(^DO[DZ]?$)|(^HV[DNZ]?$)|(^MD$)|(^VB[DGNZ]?$)", "verb", tmptag)
            tmptag = re.sub(r"^CC$", "vg", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    else:
        return set(tagset)

# This function updates the tags of the sentences in the training set according to the reduced tagset
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
    elif mode == 9:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*$", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?", "N", tmptag) # merge all nouns
            tmptag = re.sub(r"^P\w+", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 10:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?\$?", "N", tmptag) # merge all nouns + $
            tmptag = re.sub(r"^P\w+\${,2}", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
##            tmptag = re.sub(r"^QLP$", "QL", tmptag) # merge QLP to QL
##            tmptag = re.sub(r"(^BEG$)|(^HVN$)", "VB", tmptag) # being and having to vbs
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 11:
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^JJ\w*", "JJ", tmptag) # merge all adjectives
            tmptag = re.sub(r"^N[NPR]S?\$?", "N", tmptag) # merge all nouns + $
            tmptag = re.sub(r"^P\w+\${,2}", "P", tmptag) # merge all pronouns
            tmptag = re.sub(r"^R\w+", "R", tmptag) # merge all adverbs
            tmptag = re.sub(r"^VB\w*$", "VB", tmptag) # merge all verbs
            tmptag = re.sub(r"^BE.*$", "BE", tmptag) # merge be
            tmptag = re.sub(r"^HV.*$", "HV", tmptag) # merge have
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 12:
        for wd in sen:
            tmptag = re.sub(r"^JJ.*$", "JJ", wd[1].encode('ascii', 'ignore')) # merge all adjectives
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 13: # dutch
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^[\,\.\:\'\-\)\(\`]{1,2}$", "punct", tmptag)
            tmptag = re.sub(r"(^A[BP]\w?$)|(^JJ\w?$)", "adj", tmptag)
            tmptag = re.sub(r"(^\*$)|(^EX$)|(^QL$)|(^RB[RT]?$)", "adv", tmptag)
            tmptag = re.sub(r"^RP$", "part", tmptag)
            tmptag = re.sub(r"(^CS$)|(^TO$)", "comp", tmptag)
            tmptag = re.sub(r"(^AT$)|(^DT[IS]?$)|(^PPL$)|(^PP$)|(^PPLS$)|(^WDT$)|(^WPO$)|(^WPS$)|(^WRB$)", "det", tmptag)
            tmptag = re.sub(r"^FW$", "fixed", tmptag)
##            tmptag = re.sub(r"^NP$", "name", tmptag)
            tmptag = re.sub(r"(^NN$)|(^NP$)|(^NNS$)|(^NPS$)|(^NR$)|(^PN$)|(^PPO$)|(^PPS{1,2}$)", "noun", tmptag)
            tmptag = re.sub(r"(^CD$)|(^OD$)", "num", tmptag)
            tmptag = re.sub(r"^IN$", "prep", tmptag)
            tmptag = re.sub(r"(^BE\w{0,2}$)|(^DO[DZ]?$)|(^HV[DNZ]?$)|(^MD$)|(^VB[DGNZ]?$)", "verb", tmptag)
            tmptag = re.sub(r"^CC$", "vg", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    else:
        return sen

# Returns full tagset of the brown corpus. Hardcoded in order to save startup time
# Alternative command to extract full tagset:
# set([t for (w,t) in brown.tagged_words()])
##def getDefaultTagset():
##    return [u'BEDZ-NC', u'NP$', u'AT-TL', u'CS', u'NP+HVZ', u'IN-TL-HL', u'NR-HL', u'CC-TL-HL', u'NNS$-HL', u'JJS-HL',
##              u'JJ-HL', u'WRB-TL', u'JJT-TL', u'WRB', u'DOD*', u'BER*-NC', u')-HL', u'NPS$-HL', u'RB-HL', u'FW-PPSS',
##              u'NP+HVZ-NC', u'NNS$', u'--', u'CC-TL', u'FW-NN-TL', u'NP-TL-HL', u'PPSS+MD', u'NPS', u'RBR+CS', u'DTI',
##              u'NPS-TL', u'BEM', u'FW-AT+NP-TL', u'EX+BEZ', u'BEG', u'BED', u'BEZ', u'DTX', u'DOD*-TL', u'FW-VB-NC',
##              u'DTS', u'DTS+BEZ', u'QL-HL', u'NP$-TL', u'WRB+DOD*', u'JJR+CS', u'NN+MD', u'NN-TL-HL', u'HVD-HL',
##              u'NP+BEZ-NC', u'VBN+TO', u'*-TL', u'WDT-HL', u'MD', u'NN-HL', u'FW-BE', u'DT$', u'PN-TL', u'DT-HL',
##              u'FW-NR-TL', u'VBG', u'VBD', u'VBN', u'DOD', u'FW-VBG-TL', u'DOZ', u'ABN-TL', u'VB+JJ-NC', u'VBZ',
##              u'RB+CS', u'FW-PN', u'CS-NC', u'VBG-NC', u'BER-HL', u'MD*', u'``', u'WPS-TL', u'OD-TL', u'PPSS-HL',
##              u'PPS+MD', u'DO*', u'DO-HL', u'HVG-HL', u'WRB-HL', u'JJT', u'JJS', u'JJR', u'HV+TO', u'WQL', u'DOD-NC',
##              u'CC-HL', u'FW-PPSS+HV', u'FW-NP-TL', u'MD+TO', u'VB+IN', u'JJT-NC', u'WDT+BEZ-TL', u'---HL', u'PN$',
##              u'VB+PPO', u'BE-TL', u'VBG-TL', u'NP$-HL', u'VBZ-TL', u'UH', u'FW-WPO', u'AP+AP-NC', u'FW-IN', u'NRS-TL',
##              u'ABL', u'ABN', u'TO-TL', u'ABX', u'*-HL', u'FW-WPS', u'VB-NC', u'HVD*', u'PPS+HVD', u'FW-IN+AT',
##              u'FW-NP', u'QLP', u'FW-NR', u'FW-NN', u'PPS+HVZ', u'NNS-NC', u'DT+BEZ-NC', u'PPO', u'PPO-NC', u'EX-HL',
##              u'AP$', u'OD-NC', u'RP', u'WPS+BEZ', u'NN+BEZ', u'.-TL', u',', u'FW-DT+BEZ', u'RB', u'FW-PP$-NC', u'RN',
##              u'JJ$-TL', u'MD-NC', u'VBD-NC', u'PPSS+BER-N', u'RB+BEZ-NC', u'WPS-HL', u'VBN-NC', u'BEZ-HL', u'PPL-NC',
##              u'BER-TL', u'PP$$', u'NNS+MD', u'PPS-NC', u'FW-UH-NC', u'PPS+BEZ-NC', u'PPSS+BER-TL', u'NR-NC', u'FW-JJ',
##              u'PPS+BEZ-HL', u'NPS$', u'RB-TL', u'VB-TL', u'BEM*', u'MD*-HL', u'FW-CC', u'NP+MD', u'EX+HVZ', u'FW-CD',
##              u'EX+HVD', u'IN-HL', u'FW-CS', u'JJR-HL', u'FW-IN+NP-TL', u'JJ-TL-HL', u'FW-UH', u'EX', u'FW-NNS-NC',
##              u'FW-JJ-NC', u'VBZ-HL', u'VB+RP', u'BEZ-NC', u'PPSS+HV-TL', u'HV*', u'IN', u'PP$-NC', u'NP-NC', u'BEN',
##              u'PP$-TL', u'FW-*-TL', u'FW-OD-TL', u'WPS', u'WPO', u'MD+PPSS', u'WDT+BER', u'WDT+BEZ', u'CD-HL',
##              u'WDT+BEZ-NC', u'WP$', u'DO+PPSS', u'HV-HL', u'DT-NC', u'PN-NC', u'FW-VBZ', u'HVD', u'HVG', u'NN+BEZ-TL',
##              u'HVZ', u'FW-VBD', u'FW-VBG', u'NNS$-TL', u'JJ-TL', u'FW-VBN', u'MD-TL', u'WDT+DOD', u'HV-TL', u'NN-TL',
##              u'PPSS', u'NR$', u'BER', u'FW-VB', u'DT', u'PN+BEZ', u'VBG-HL', u'FW-PPL+VBZ', u'FW-NPS-TL', u'RB$',
##              u'FW-IN+NN', u'FW-CC-TL', u'RBT', u'RBR', u'PPS-TL', u'PPSS+HV', u'JJS-TL', u'NPS-HL', u'WPS+BEZ-TL',
##              u'NNS-TL-HL', u'VBN-TL-NC', u'QL-TL', u'NN+NN-NC', u'JJR-TL', u'NN$-TL', u'FW-QL', u'IN-TL', u'BED-NC',
##              u'NRS', u'.-HL', u'QL', u'PP$-HL', u'WRB+BER', u'JJ', u'WRB+BEZ', u'NNS$-TL-HL', u'PPSS+BEZ', u'(',
##              u'PPSS+BER', u'DT+MD', u'DOZ-TL', u'PPSS+BEM', u'FW-PP$', u'RB+BEZ-HL', u'FW-RB+CC', u'FW-PPS', u'VBG+TO',
##              u'DO*-HL', u'NR+MD', u'PPLS', u'IN+IN', u'BEZ*', u'FW-PPL', u'FW-PPO', u'NNS-HL', u'NIL', u'HVN',
##              u'PPSS+BER-NC', u'AP-TL', u'FW-DT', u'(-HL', u'DTI-TL', u'JJ+JJ-NC', u'FW-RB', u'FW-VBD-TL', u'BER-NC',
##              u'NNS$-NC', u'JJ-NC', u'NPS$-TL', u'VB+VB-NC', u'PN', u'VB+TO', u'AT-TL-HL', u'BEM-NC', u'PPL-TL',
##              u'ABN-HL', u'RB-NC', u'DO-NC', u'BE-HL', u'WRB+IN', u'FW-UH-TL', u'PPO-HL', u'FW-CD-TL', u'TO-HL',
##              u'PPS+BEZ', u'CD$', u'DO', u'EX+MD', u'HVZ-TL', u'TO-NC', u'IN-NC', u'.', u'WRB+DO', u'CD-NC',
##              u'FW-PPO+IN', u'FW-NN$-TL', u'WDT+BEZ-HL', u'RP-HL', u'CC', u'NN+HVZ-TL', u'FW-NNS-TL', u'DT+BEZ',
##              u'WPS+HVZ', u'BEDZ*', u'NP-TL', u':-TL', u'NN-NC', u'WPO-TL', u'QL-NC', u'FW-AT+NN-TL', u'WDT+HVZ',
##              u'.-NC', u'FW-DTS', u'NP-HL', u':-HL', u'RBR-NC', u'OD-HL', u'BEDZ-HL', u'VBD-TL', u'NPS-NC', u')',
##              u'TO+VB', u'FW-IN+NN-TL', u'PPL', u'PPS', u'PPSS+VB', u'DT-TL', u'RP-NC', u'VB', u'FW-VB-TL', u'PP$',
##              u'VBD-HL', u'DTI-HL', u'NN-TL-NC', u'PPL-HL', u'DOZ*', u'NR-TL', u'WRB+MD', u'PN+HVZ', u'FW-IN-TL',
##              u'PN+HVD', u'BEN-TL', u'BE', u'WDT', u'WPS+HVD', u'DO-TL', u'FW-NN-NC', u'WRB+BEZ-TL', u'UH-TL',
##              u'JJR-NC', u'NNS', u'PPSS-NC', u'WPS+BEZ-NC', u',-TL', u'NN$', u'VBN-TL-HL', u'WDT-NC', u'OD',
##              u'FW-OD-NC', u'DOZ*-TL', u'PPSS+HVD', u'CS-TL', u'WRB+DOZ', u'CC-NC', u'HV', u'NN$-HL', u'FW-WDT',
##              u'WRB+DOD', u'NN+HVZ', u'AT-NC', u'NNS-TL', u'FW-BEZ', u'CS-HL', u'WPO-NC', u'FW-BER', u'NNS-TL-NC',
##              u'BEZ-TL', u'FW-IN+AT-T', u'ABN-NC', u'NR-TL-HL', u'BEDZ', u'NP+BEZ', u'FW-AT-TL', u'BER*', u'WPS+MD',
##              u'MD-HL', u'BED*', u'HV-NC', u'WPS-NC', u'VBN-HL', u'FW-TO+VB', u'PPSS+MD-NC', u'HVZ*', u'PPS-HL',
##              u'WRB-NC', u'VBN-TL', u'CD-TL-HL', u',-NC', u'RP-TL', u'AP-HL', u'FW-HV', u'WQL-TL', u'FW-AT', u'NN',
##              u'NR$-TL', u'VBZ-NC', u'*', u'PPSS-TL', u'JJT-HL', u'FW-NNS', u'NP', u'UH-HL', u'NR', u':', u'FW-NN$',
##              u'RP+IN', u',-HL', u'JJ-TL-NC', u'AP-NC', u'*-NC', u'VB-HL', u'HVZ-NC', u'DTS-HL', u'FW-JJT', u'FW-JJR',
##              u'FW-JJ-TL', u'FW-*', u'RB+BEZ', u"''", u'VB+AT', u'PN-HL', u'PPO-TL', u'CD-TL', u'UH-NC', u'FW-NN-TL-NC',
##              u'EX-NC', u'PPSS+BEZ*', u'TO', u'WDT+DO+PPS', u'IN+PPO', u'AP', u'AT', u'DOZ-HL', u'FW-RB-TL', u'CD',
##              u'NN+IN', u'FW-AT-HL', u'PN+MD', u"'", u'FW-PP$-TL', u'FW-NPS', u'WDT+BER+PP', u'NN+HVD-TL', u'MD+HV',
##              u'AT-HL', u'FW-IN+AT-TL']
