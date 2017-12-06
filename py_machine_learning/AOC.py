import numpy as np
import re
from itertools import *
from collections import *
from operator import itemgetter

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]
    
def lshift(x):
    r = re.search('(\w+) LSHIFT (\d+) -> (\w+)', x)
    return r.groups() if r is not None else None
def rshift(x):
    r = re.search('(\w+) RSHIFT (\d+) -> (\w+)', x)
    return r.groups() if r is not None else None

def isand(x):
    r = re.search('(\w+) AND (\w+) -> (\w+)', x)
    return r.groups() if r is not None else None

def isor(x):
    r = re.search('(\w+) OR (\w+) -> (\w+)', x)
    return r.groups() if r is not None else None

def isnot(x):
    r = re.search('NOT (\w+) -> (\w+)', x)
    return r.groups() if r is not None else None

def assign(x):
    r = re.search('(\w+) -> (\w+)', x)
    return r.groups() if r is not None else None

with open("input.txt") as f:
    lines = [l.strip() for l in f.readlines()]

sym = {}
symval = {}
for l in lines:
    x= lshift(l)
    if x:
        sym[x[2]] = ['l'] + list(x)
        continue
    x= rshift(l)
    if x:
        sym[x[2]] = ['r'] + list(x)
        continue
    x= isand(l)
    if x:
        sym[x[2]] = ['a'] + list(x)
        continue
    x= isor(l)
    if x:
        sym[x[2]] = ['o'] + list(x)
        continue
    x= isnot(l)
    if x:
        sym[x[1]] = ['n'] + list(x)
        continue
    x= assign(l)
    if x:
        sym[x[1]] = ['x'] + list(x)
        continue


sym['b'] = ['x'] + [str(16076)]

def process(var):
    global sym,symval
    if var in symval:
        return symval[var]
    if(var.isdigit()):
        return np.ushort(var)

    ins = sym[var]
    i = ins[0]
    if(i == 'x'):
        symval[var] = process(ins[1])
        return np.ushort(symval[var])
    elif(i == 'n'):
        symval[var] = ~process(ins[1])
        return np.ushort(symval[var])
    elif(i == 'a'):
        symval[var] = process(ins[1]) &  process(ins[2])
        return np.ushort(symval[var])
    elif(i == 'o'):
        symval[var] = process(ins[1]) | process(ins[2])
        return np.ushort(symval[var])
    elif(i == 'l'):
        symval[var] = process(ins[1]) << process(ins[2])
        return np.ushort(symval[var])
    elif(i == 'r'):
        symval[var] = process(ins[1]) >> process(ins[2])
        return np.ushort(symval[var])


process('a')
print(symval['a'])
