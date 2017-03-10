from nltk.corpus import brown
from nltk.util import ngrams
from nltk.probability import FreqDist
import datetime
import re
from math import exp, log
from sys import float_info

n = 50000
smode = 0


# set([t for (w,t) in brown.tagged_words()])
tagset = [u'BEDZ-NC', u'NP$', u'AT-TL', u'CS', u'NP+HVZ', u'IN-TL-HL', u'NR-HL', u'CC-TL-HL', u'NNS$-HL', u'JJS-HL',
              u'JJ-HL', u'WRB-TL', u'JJT-TL', u'WRB', u'DOD*', u'BER*-NC', u')-HL', u'NPS$-HL', u'RB-HL', u'FW-PPSS',
              u'NP+HVZ-NC', u'NNS$', u'--', u'CC-TL', u'FW-NN-TL', u'NP-TL-HL', u'PPSS+MD', u'NPS', u'RBR+CS', u'DTI',
              u'NPS-TL', u'BEM', u'FW-AT+NP-TL', u'EX+BEZ', u'BEG', u'BED', u'BEZ', u'DTX', u'DOD*-TL', u'FW-VB-NC',
              u'DTS', u'DTS+BEZ', u'QL-HL', u'NP$-TL', u'WRB+DOD*', u'JJR+CS', u'NN+MD', u'NN-TL-HL', u'HVD-HL',
              u'NP+BEZ-NC', u'VBN+TO', u'*-TL', u'WDT-HL', u'MD', u'NN-HL', u'FW-BE', u'DT$', u'PN-TL', u'DT-HL',
              u'FW-NR-TL', u'VBG', u'VBD', u'VBN', u'DOD', u'FW-VBG-TL', u'DOZ', u'ABN-TL', u'VB+JJ-NC', u'VBZ',
              u'RB+CS', u'FW-PN', u'CS-NC', u'VBG-NC', u'BER-HL', u'MD*', u'``', u'WPS-TL', u'OD-TL', u'PPSS-HL',
              u'PPS+MD', u'DO*', u'DO-HL', u'HVG-HL', u'WRB-HL', u'JJT', u'JJS', u'JJR', u'HV+TO', u'WQL', u'DOD-NC',
              u'CC-HL', u'FW-PPSS+HV', u'FW-NP-TL', u'MD+TO', u'VB+IN', u'JJT-NC', u'WDT+BEZ-TL', u'---HL', u'PN$',
              u'VB+PPO', u'BE-TL', u'VBG-TL', u'NP$-HL', u'VBZ-TL', u'UH', u'FW-WPO', u'AP+AP-NC', u'FW-IN', u'NRS-TL',
              u'ABL', u'ABN', u'TO-TL', u'ABX', u'*-HL', u'FW-WPS', u'VB-NC', u'HVD*', u'PPS+HVD', u'FW-IN+AT',
              u'FW-NP', u'QLP', u'FW-NR', u'FW-NN', u'PPS+HVZ', u'NNS-NC', u'DT+BEZ-NC', u'PPO', u'PPO-NC', u'EX-HL',
              u'AP$', u'OD-NC', u'RP', u'WPS+BEZ', u'NN+BEZ', u'.-TL', u',', u'FW-DT+BEZ', u'RB', u'FW-PP$-NC', u'RN',
              u'JJ$-TL', u'MD-NC', u'VBD-NC', u'PPSS+BER-N', u'RB+BEZ-NC', u'WPS-HL', u'VBN-NC', u'BEZ-HL', u'PPL-NC',
              u'BER-TL', u'PP$$', u'NNS+MD', u'PPS-NC', u'FW-UH-NC', u'PPS+BEZ-NC', u'PPSS+BER-TL', u'NR-NC', u'FW-JJ',
              u'PPS+BEZ-HL', u'NPS$', u'RB-TL', u'VB-TL', u'BEM*', u'MD*-HL', u'FW-CC', u'NP+MD', u'EX+HVZ', u'FW-CD',
              u'EX+HVD', u'IN-HL', u'FW-CS', u'JJR-HL', u'FW-IN+NP-TL', u'JJ-TL-HL', u'FW-UH', u'EX', u'FW-NNS-NC',
              u'FW-JJ-NC', u'VBZ-HL', u'VB+RP', u'BEZ-NC', u'PPSS+HV-TL', u'HV*', u'IN', u'PP$-NC', u'NP-NC', u'BEN',
              u'PP$-TL', u'FW-*-TL', u'FW-OD-TL', u'WPS', u'WPO', u'MD+PPSS', u'WDT+BER', u'WDT+BEZ', u'CD-HL',
              u'WDT+BEZ-NC', u'WP$', u'DO+PPSS', u'HV-HL', u'DT-NC', u'PN-NC', u'FW-VBZ', u'HVD', u'HVG', u'NN+BEZ-TL',
              u'HVZ', u'FW-VBD', u'FW-VBG', u'NNS$-TL', u'JJ-TL', u'FW-VBN', u'MD-TL', u'WDT+DOD', u'HV-TL', u'NN-TL',
              u'PPSS', u'NR$', u'BER', u'FW-VB', u'DT', u'PN+BEZ', u'VBG-HL', u'FW-PPL+VBZ', u'FW-NPS-TL', u'RB$',
              u'FW-IN+NN', u'FW-CC-TL', u'RBT', u'RBR', u'PPS-TL', u'PPSS+HV', u'JJS-TL', u'NPS-HL', u'WPS+BEZ-TL',
              u'NNS-TL-HL', u'VBN-TL-NC', u'QL-TL', u'NN+NN-NC', u'JJR-TL', u'NN$-TL', u'FW-QL', u'IN-TL', u'BED-NC',
              u'NRS', u'.-HL', u'QL', u'PP$-HL', u'WRB+BER', u'JJ', u'WRB+BEZ', u'NNS$-TL-HL', u'PPSS+BEZ', u'(',
              u'PPSS+BER', u'DT+MD', u'DOZ-TL', u'PPSS+BEM', u'FW-PP$', u'RB+BEZ-HL', u'FW-RB+CC', u'FW-PPS', u'VBG+TO',
              u'DO*-HL', u'NR+MD', u'PPLS', u'IN+IN', u'BEZ*', u'FW-PPL', u'FW-PPO', u'NNS-HL', u'NIL', u'HVN',
              u'PPSS+BER-NC', u'AP-TL', u'FW-DT', u'(-HL', u'DTI-TL', u'JJ+JJ-NC', u'FW-RB', u'FW-VBD-TL', u'BER-NC',
              u'NNS$-NC', u'JJ-NC', u'NPS$-TL', u'VB+VB-NC', u'PN', u'VB+TO', u'AT-TL-HL', u'BEM-NC', u'PPL-TL',
              u'ABN-HL', u'RB-NC', u'DO-NC', u'BE-HL', u'WRB+IN', u'FW-UH-TL', u'PPO-HL', u'FW-CD-TL', u'TO-HL',
              u'PPS+BEZ', u'CD$', u'DO', u'EX+MD', u'HVZ-TL', u'TO-NC', u'IN-NC', u'.', u'WRB+DO', u'CD-NC',
              u'FW-PPO+IN', u'FW-NN$-TL', u'WDT+BEZ-HL', u'RP-HL', u'CC', u'NN+HVZ-TL', u'FW-NNS-TL', u'DT+BEZ',
              u'WPS+HVZ', u'BEDZ*', u'NP-TL', u':-TL', u'NN-NC', u'WPO-TL', u'QL-NC', u'FW-AT+NN-TL', u'WDT+HVZ',
              u'.-NC', u'FW-DTS', u'NP-HL', u':-HL', u'RBR-NC', u'OD-HL', u'BEDZ-HL', u'VBD-TL', u'NPS-NC', u')',
              u'TO+VB', u'FW-IN+NN-TL', u'PPL', u'PPS', u'PPSS+VB', u'DT-TL', u'RP-NC', u'VB', u'FW-VB-TL', u'PP$',
              u'VBD-HL', u'DTI-HL', u'NN-TL-NC', u'PPL-HL', u'DOZ*', u'NR-TL', u'WRB+MD', u'PN+HVZ', u'FW-IN-TL',
              u'PN+HVD', u'BEN-TL', u'BE', u'WDT', u'WPS+HVD', u'DO-TL', u'FW-NN-NC', u'WRB+BEZ-TL', u'UH-TL',
              u'JJR-NC', u'NNS', u'PPSS-NC', u'WPS+BEZ-NC', u',-TL', u'NN$', u'VBN-TL-HL', u'WDT-NC', u'OD',
              u'FW-OD-NC', u'DOZ*-TL', u'PPSS+HVD', u'CS-TL', u'WRB+DOZ', u'CC-NC', u'HV', u'NN$-HL', u'FW-WDT',
              u'WRB+DOD', u'NN+HVZ', u'AT-NC', u'NNS-TL', u'FW-BEZ', u'CS-HL', u'WPO-NC', u'FW-BER', u'NNS-TL-NC',
              u'BEZ-TL', u'FW-IN+AT-T', u'ABN-NC', u'NR-TL-HL', u'BEDZ', u'NP+BEZ', u'FW-AT-TL', u'BER*', u'WPS+MD',
              u'MD-HL', u'BED*', u'HV-NC', u'WPS-NC', u'VBN-HL', u'FW-TO+VB', u'PPSS+MD-NC', u'HVZ*', u'PPS-HL',
              u'WRB-NC', u'VBN-TL', u'CD-TL-HL', u',-NC', u'RP-TL', u'AP-HL', u'FW-HV', u'WQL-TL', u'FW-AT', u'NN',
              u'NR$-TL', u'VBZ-NC', u'*', u'PPSS-TL', u'JJT-HL', u'FW-NNS', u'NP', u'UH-HL', u'NR', u':', u'FW-NN$',
              u'RP+IN', u',-HL', u'JJ-TL-NC', u'AP-NC', u'*-NC', u'VB-HL', u'HVZ-NC', u'DTS-HL', u'FW-JJT', u'FW-JJR',
              u'FW-JJ-TL', u'FW-*', u'RB+BEZ', u"''", u'VB+AT', u'PN-HL', u'PPO-TL', u'CD-TL', u'UH-NC', u'FW-NN-TL-NC',
              u'EX-NC', u'PPSS+BEZ*', u'TO', u'WDT+DO+PPS', u'IN+PPO', u'AP', u'AT', u'DOZ-HL', u'FW-RB-TL', u'CD',
              u'NN+IN', u'FW-AT-HL', u'PN+MD', u"'", u'FW-PP$-TL', u'FW-NPS', u'WDT+BER+PP', u'NN+HVD-TL', u'MD+HV',
              u'AT-HL', u'FW-IN+AT-TL']

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


tagset = reducetagset(tagset,smode)
tagset.add(u'START')
tagset.add(u'END')

sents = []

# append start and and tags
for sen in brown.tagged_sents()[:n]:    
    sents += [[(u'<s>', u'START')] + updatetags(sen,smode) + [(u'</s>', u'END')]]

# smooth unknown words
# first convert sentences to words
tokens = []
for sen in sents:
    for wd in sen:
        tokens.append(wd)

# get a freqdist & calc the hapax legomena
fd_tok = FreqDist(tokens)
hpx_lg = set([e[0] for e in fd_tok.items() if e[1] == 1])

# update sentences by adding the UNK word
new_sents = []
for sen in sents:
    tmp_sen = []
    for wd in sen:
        if wd in hpx_lg:
            tmp_sen.append((u'UNK', wd[1]))
        else:
            tmp_sen.append(wd)
    new_sents += [tmp_sen]
sents = new_sents

# create a list of types
types = []
for sen in sents:
    for wd in sen:
        types.append(wd[0])
types = set(types)
types.remove(u'UNK')


# get the freqdist of the unigrams in the corpus by iterating through every word in every sentence
# and copying it into a list
tag_uni = []
for sen in sents:
    for wd in sen:
        tag_uni.append(wd[1])  # tag only

fd_uni = FreqDist(tag_uni)

# get the freqdist of the bigram tags in the corpus
tag_bi = []
for sen in sents:
    tags_only = [wd[1] for wd in sen]
    tag_bi += ngrams(tags_only, 2)

fd_bi = FreqDist(tag_bi)

# get the freqdist of the word-tag tuples
tag_wd = []
for sen in sents:
    for wd in sen:
        tag_wd.append(wd)

fd_wd = FreqDist(tag_wd)

trans = {}
for t1 in tagset:
    for t2 in tagset:
        trans[(t1, t2)] = log(float_info.min)
# calculate transition probabilities & add LaPlace smoothing
for t1 in tagset:
    for t2 in tagset:
        prob = 1.0 * (fd_bi[(t1, t2)] + 1) / (fd_uni[t1] + len(tagset))
        if prob != 0:
            trans[(t1, t2)] = 1.0 * log(1.0 * (fd_bi[(t1, t2)] + 1) / (fd_uni[t1] + len(tagset)))

em = {}
types2 = types
types2.add(u'UNK')
for wd in types2:
    for tag in tagset:
        em[(wd,tag)] = log(float_info.min)

# calculate emission probabilities
for wd in fd_wd.items():
    prob = 1.0 * wd[1] / fd_uni[wd[0][1]]
    if prob != 0:
        em[wd[0]] = 1.0 * log(1.0 * wd[1] / fd_uni[wd[0][1]])


# add sent before unknown
def viterbi(sen, known_wds, states, p_trans, p_emit):
    # Viterbi as list of dicts
    # Each obs in the list has a dict of state dicts
    # Each state dict has a prob and a backpointer
    V = [{}]
    out = []

    # init
    curr_wd = u'UNK'
    if sen[0] in known_wds:
        curr_wd = sen[0]
    for s in states:
        p_start = 0.0 + p_trans[('START', s)] + p_emit[(curr_wd, s)]
        V[0][s] = {'p': p_start, 'bckptr': None}

    # run
    for wd in range(1, len(sen)):
        V.append({})
        curr_wd = u'UNK'
        if sen[wd] in known_wds:
            curr_wd = sen[wd]
        for s in states:
            maxptr = max(states, key=lambda last_s:0.0 + V[wd - 1][last_s]['p'] + p_trans[(last_s, s)])
            V[wd][s] = {'p': 0.0 + V[wd - 1][maxptr]['p'] + p_trans[(maxptr, s)] + p_emit[(curr_wd, s)], 'bckptr': maxptr}
                
    # terminate
    maxptr = max(states, key=lambda last_s:0.0 + V[len(sen) - 1][last_s]['p'] + p_trans[(last_s, 'END')])
    maxp = 0.0 + V[len(sen) - 1][maxptr]['p'] + p_trans[(maxptr, 'END')]

    # backtrack
    out += [(sen[len(sen) - 1], maxptr)]
    for wd in range(len(sen) - 1, 0, -1):
        out = [(sen[wd - 1], V[wd][maxptr]['bckptr'])] + out
        maxptr = V[wd][maxptr]['bckptr']

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
##        print i
##        print tagged_sentence
##        print reference
##        print total_words
##        print right_words

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
   
tag(50000,50500)

# viterbi(brown.sents()[1], tagset, fd_bi, fd_wd)
# brown.tagged_sents()[1]

##def tag_preproc(tagset):
##    for tag in tagset:
        

##def getOneBi(tag):
##    a = 0
##    for i in fd_bi.items():
##        if i[0][0] == tag:
##            a += i[1]
##    return a
##
##
##def getOneWd(tag):
##    a = 0
##    for i in fd_wd.items():
##        if i[0][1] == tag:
##            a += i[1]
##    return a

