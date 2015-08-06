#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pprint
import itertools
from math import log

import dawg

def uniq(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def pinyin(word):
    N = len(word)
    pos = 0
    result = []
    while pos < N:
        for i in range(N, pos, -1):
            frag = word[pos:i]
            if frag in chdict:
                result.append(sorted(chdict[frag], key=lambda x: -prob.get((frag, x), 0))[0])
                break
        pos = i
    return ''.join(result)

index = {}
prob = {}
abbr = {}

chdict = {}
pending = []
started = False
with open('luna_pinyin.dict.yaml', 'r', encoding='utf-8') as f:
    for ln in f:
        ln = ln.strip()
        if started and ln and ln[0] != '#':
            l = ln.split('\t')
            w, c = l[0], l[1].replace(' ', '')
            if c in index:
                index[c].append(w)
            else:
                index[c] = [w]
            if len(w) == 1:
                if c[0] in abbr:
                    abbr[c[0]].add(c)
                else:
                    abbr[c[0]] = set((c,))
            if w in chdict:
                chdict[w].append(c)
            else:
                chdict[w] = [c]
            if len(l) == 3:
                if l[2][-1] == '%':
                    p = float(l[2][:-1])/100
                else:
                    p = float(l[2])
                prob[(w, c)] = log(p or 0.00005)
        elif ln == '...':
            started = True

essay = {}
ltotal = 0
with open('essay.txt', 'r', encoding='utf-8') as f:
    for ln in f:
        word, freq = ln.strip().split('\t')
        freq = int(freq) + 1
        essay[word] = freq
        ltotal += freq
        if len(word) > 1:
            c = pinyin(word)
            if c in index:
                index[c].append(word)
            else:
                index[c] = [word]
    logtotal = log(ltotal)
    for word in essay:
        essay[word] = int((log(essay[word]) - logtotal) * -1000000)

for c in tuple(index.keys()):
    ws = index[c]
    index[c] = uniq(ws)
    for ch in range(len(c)):
        wfrag = c[:ch + 1]
        if wfrag not in index:
            index[wfrag] = ['']

p_index = dawg.BytesDAWG(itertools.chain.from_iterable(((k, v.encode('utf-8')) for v in vl) for k,vl in index.items()))
p_index.save('pyindex.dawg')
p_essay = dawg.IntDAWG(essay)
p_essay.save('essay.dawg')

for c in abbr:
    abbr[c] = tuple(abbr[c])

header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Pinyin dictionary from librime/luna_pinyin
"""

'''

pf = pprint.PrettyPrinter(indent=0).pformat

with open('pinyinlookup.py', 'w') as f:
    f.write(header)
    f.write('logtotal = %s\n\np_prob = ' % logtotal)
    f.write(pf(prob))
    f.write('\n\np_abbr = ')
    f.write(pf(abbr))
    f.write('\n')
