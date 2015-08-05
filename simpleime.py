#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import itertools
from math import log
from pinyinlookup import p_index, p_prob, p_abbr

essay = {}
logtotal = 0

_ig1 = lambda x: x[1]

def loaddict(filename='essay.txt'):
    global essay, logtotal, p_index
    ltotal = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for ln in f:
            word, freq = ln.strip().split('\t')
            freq = int(freq) + 1
            essay[word] = freq
            ltotal += freq
    logtotal = log(ltotal)
    for word in essay:
        essay[word] = log(essay[word]) - logtotal
    for code in tuple(p_index.keys()):
        for ch in range(len(code)):
            wfrag = code[:ch + 1]
            if wfrag not in p_index:
                p_index[wfrag] = ()

def pinyininput(sentence):
    DAG = {}
    edges = {}
    N = len(sentence)
    for k in range(N):
        tmplist = []
        i = k
        frag = sentence[k]
        while i < N and frag in p_index:
            words = p_index[frag]
            if words:
                tmplist.append(i)
                edges[(k, i)] = max(((w, essay.get(w, -logtotal) + p_prob.get((w, frag), 0)) for w in words), key=_ig1)
            i += 1
            frag = sentence[k:i + 1]
        if not tmplist:
            tmplist.append(k)
            abbr = p_abbr.get(sentence[k])
            if abbr:
                edges[(k, k)] = max(((w, essay.get(w, -logtotal) + p_prob.get((w, frag), 0)) for w, frag in itertools.chain.from_iterable(((wrd, c) for wrd in p_index.get(c, ())) for c in abbr)), key=_ig1)
        DAG[k] = tmplist

    route = {N: (0, 0)}
    for idx in range(N - 1, -1, -1):
        route[idx] = max((edges.get((idx,x), (None, -50))[1] + route[x + 1][0], x) for x in DAG[idx])

    result = []
    x = 0
    while x < N:
        y = route[x][1]
        result.append(edges.get((x, y), (sentence[x:y+1], -50))[0])
        x = y + 1
    return ''.join(result)



loaddict(filename='essay.txt')
print(-logtotal)

while 1:
    print(pinyininput(input('> ')))

'''

Graph g
Source s
top_sorted_list = top_sort(g)

cost = {} // A mapping between a node, the cost of it's shortest path, and it's parent in the shortest path

for each vertex v in top_sorted_list:
  cost[vertex].cost = inf
  cost[vertex].parent = None

cost[s] = 0

for each vertex v in top_sorted_list:
   for each edge e in adjacenies of v:
      if cost[e.dest].cost < cost[v].cost + e.weight:
        cost[e.dest].cost =  cost[v].cost + e.weight
        cost[e.dest].parent = v


'''
