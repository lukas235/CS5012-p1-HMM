import re

# This module reduces the default tagsets in different ways
# every mode 

# mode 0: NO CHANGES
# The amount of tags excludes START and END tag
# mode 1: (105 tags): Reduce compound tags (e.g. 'JJR-HL' or 'FW-IN+NP-TL' to 'JJR' and 'FW') (1st experiment)
# mode 2: Only remove $ and *
# mode 3: mode 1 + 2 combined (2nd experiment)
# mode 4: mode 3 + concentrate all most of the 3-letter tags to 2-letters
# mode 5: naive cut-off of the 3rd letter if existent
# mode 6: reduce most of the tags to one letter
# mode 7: concentrate non-word characters such as brackets, hyphens and quotation marks
# mode 8 (15 tags): extreme concentration of characters
# mode 9: merge all nouns, verbs, adjectives, pronouns and adverbs to their superclasses (3rd experiment)
# mode 10: just a test with QL/QLP
# mode 11: 9 + merge HAVING & BEING to HV_ and BE_
# mode 12: merge all the adjectives to see the impact on the
# mode 13: make brown tags compatible to alpino, by narrowing down

# mode 14: for alpino: merge name & nouns; fix for pron -> det


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
            tmptag = re.sub(r"^C[CS]$", "C", tmptag) #! tmptag = re.sub(r"^C\w+$", "C", tmptag) for naive merging of C (experiment)
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
    elif mode == 13: # make brown compatible to alpino
        for t in tagset:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"(^AB\w?$)", "ab", tmptag)
            tmptag = re.sub(r"(^JJ\w?$)", "adj", tmptag)
            tmptag = re.sub(r"(^QLP?$)|(^RB[RT]?$)", "adv", tmptag)
            tmptag = re.sub(r"(^TO$)", "comp", tmptag)
            tmptag = re.sub(r"(^A[PT]$)|(^DT[IS]?$)|(^WDT$)|(^WPO$)|(^WPS?$)|(^WRB$)", "det", tmptag)
            tmptag = re.sub(r"(^NN$)|(^NP$)|(^NNS$)|(^NPS$)|(^NR$)", "noun", tmptag)
            tmptag = re.sub(r"(^CD$)|(^OD$)", "num", tmptag)
            tmptag = re.sub(r"^RP$", "part", tmptag)
            tmptag = re.sub(r"^IN$", "prep", tmptag)
            tmptag = re.sub(r"(^PN$)|(^PP$)|(^PPO$)|(^PPL$)|(^PPLS$)|(^PPS{1,2}$)", "pron", tmptag)
            tmptag = re.sub(r"^[\,\.\:\'\-\)\(\`]{1,2}$", "punct", tmptag)
            tmptag = re.sub(r"^EX$", "tag", tmptag)
            tmptag = re.sub(r"(^BE\w{0,2}$)|(^DO[DZ]?$)|(^HV[DNZ]?$)|(^MD$)|(^VB[DGNZ]?$)", "verb", tmptag)
            tmptag = re.sub(r"^C[CS]$", "vg", tmptag)
            tmpset.append(tmptag)
        return set(tmpset)
    elif mode == 14: # make alpino comparable and fix pron
        for t in tagset:
            tmptag = re.sub(r"^name$", "noun", t.encode('ascii', 'ignore'))
            tmptag = re.sub(r"^pron$", "det", tmptag)
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
    elif mode == 13: # brown make compatible to alpino
        for wd in sen:
            tmptag = re.sub(r"([\+\-][\*\w+].*$)|(\b\*)|(\$+)", "", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"(^AB\w?$)", "ab", tmptag)
            tmptag = re.sub(r"(^JJ\w?$)", "adj", tmptag)
            tmptag = re.sub(r"(^QLP?$)|(^RB[RT]?$)", "adv", tmptag)
            tmptag = re.sub(r"(^TO$)", "comp", tmptag)
            tmptag = re.sub(r"(^A[PT]$)|(^DT[IS]?$)|(^WDT$)|(^WPO$)|(^WPS?$)|(^WRB$)", "det", tmptag)
            tmptag = re.sub(r"(^NN$)|(^NP$)|(^NNS$)|(^NPS$)|(^NR$)", "noun", tmptag)
            tmptag = re.sub(r"(^CD$)|(^OD$)", "num", tmptag)
            tmptag = re.sub(r"^RP$", "part", tmptag)
            tmptag = re.sub(r"^IN$", "prep", tmptag)
            tmptag = re.sub(r"(^PN$)|(^PP$)|(^PPO$)|(^PPL$)|(^PPLS$)|(^PPS{1,2}$)", "pron", tmptag)
            tmptag = re.sub(r"^[\,\.\:\'\-\)\(\`]{1,2}$", "punct", tmptag)
            tmptag = re.sub(r"^EX$", "tag", tmptag)
            tmptag = re.sub(r"(^BE\w{0,2}$)|(^DO[DZ]?$)|(^HV[DNZ]?$)|(^MD$)|(^VB[DGNZ]?$)", "verb", tmptag)
            tmptag = re.sub(r"^C[CS]$", "vg", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    elif mode == 14: # alpino fixes
        for wd in sen:
            tmptag = re.sub(r"^name$", "noun", wd[1].encode('ascii', 'ignore'))
            tmptag = re.sub(r"^pron$", "det", tmptag)
            tmpsen.append((wd[0],tmptag))
        return tmpsen
    else:
        return sen
