#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pprint
from math import log

def uniq(seq): # Dave Kirby
    # Order preserving
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

index = {}
prob = {}
abbr = {}

started = False
with open('luna_pinyin.dict.yaml') as f:
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
            if len(l) == 3:
                if l[2][-1] == '%':
                    p = float(l[2][:-1])/100
                else:
                    p = float(l[2])
                prob[(w, c)] = log(p or 0.00005)
        elif ln == '...':
            started = True

for c in index:
    ws = index[c]
    if all(len(w) == 1 for w in ws):
        index[c] = ''.join(uniq(ws))
    else:
        index[c] = tuple(uniq(ws))

for c in abbr:
    abbr[c] = tuple(abbr[c])

header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Pinyin dictionary from librime/luna_pinyin
"""

p_index = '''

pf = pprint.PrettyPrinter(indent=0).pformat

with open('pinyinlookup.py', 'wb') as f:
    f.write(header)
    f.write(pf(index))
    f.write('\n\np_prob = ')
    f.write(pf(prob))
    f.write('\n\np_abbr = ')
    f.write(pf(abbr))
    f.write('\n')
