import numpy as np 
import pandas as pd 
from itertools import combinations_with_replacement
import operator as op 
from functools import reduce

PHa = 0.5
PFa = 0.25
PBa = 0.25

A_dice = ['h', 'f', 'b']
D_dice = ['e', 'b', 'f']

PEd = 3/8
PFd = 0.25
PBd = 3/8

def nCr(n,r):
    r = min(r, n-r)
    num = reduce(op.mul, range(n, n-r, -1), 1)
    den = reduce(op.mul, range(1, r+1, 1), 1)
    return num/den

def Atk_P(M, focus = False):
    hit_counts = list()
    fhit_counts = list()
    PH = np.zeros((1,M+1))
    m = 0
    if focus == False:
        for atk_combs in combinations_with_replacement(A_dice, M):
            print(atk_combs)
            count_h = atk_combs.count('h')
            count_f = atk_combs.count('f')
            count_b = atk_combs.count('b')
            hit_counts.append((count_h, count_f, count_b))
        for i in range(len(hit_counts)):
            items = np.sort(hit_counts[i][:])
            items = items[::-1]
            PH[0,m] = PH[0,m] + \
                nCr(M, items[0])*nCr(M-items[0], items[1])*nCr(m-items[0]-items[1], items[2])* \
                    (PHa**(hit_counts[i][0]))*(PFa**(hit_counts[i][1]))*(PBa**(hit_counts[i][2]))
            if (i < len(hit_counts)-1):
                if ((hit_counts[i+1][0]) < hit_counts[i][0]):
                    m = m + 1
    if focus == True:
        hits = dict()
        for atk_combs in combinations_with_replacement(A_dice, M):
            print(atk_combs)
            count_h = atk_combs.count('h') 
            count_f = atk_combs.count('f')
            count_b = atk_combs.count('b')
            fct_h = atk_combs.count('h')+atk_combs.count('f')
            fct_b = atk_combs.count('b')
            hit_counts.append((count_h, count_f, count_b))
            fhit_counts.append((fct_h, fct_b))
        hit_counts = list(dict.fromkeys(hit_counts))
        for i in range(len(hit_counts)):
            items = np.sort(hit_counts[i][:])
            items = items[::-1]
            P_holder = nCr(M, items[0])*nCr(M-items[0], items[1])*nCr(m-items[0]-items[1], items[2])* \
                (PHa**(hit_counts[i][0]))*(PFa**(hit_counts[i][1]))*(PBa**(hit_counts[i][2]))
            hits[str(fhit_counts[i])].append(P_holder)
            
            
    Atk_EV = 0
    for i in range(len(PH[0,:])-1, -1, -1):
        Atk_EV = PH[0,i]*(m-i) + Atk_EV
    return hit_counts, atk_combs, PH[0,:], Atk_EV

def Def_P(N, focus = False):
    evade_counts = list()
    PE = np.zeros((1,N+1))
    n = 0
    if focus == False:
        for def_combs in combinations_with_replacement(D_dice, N):
            print(def_combs)
            count_e = def_combs.count('e')
            count_f = def_combs.count('f')
            count_b = def_combs.count('b')
            evade_counts.append((count_e, count_f, count_b))
        for i in range(len(evade_counts)):
            items = np.sort(evade_counts[i][:])
            items = items[::-1]
            PE[0,n] = PE[0,n] + \
                nCr(N, items[0])*nCr(N-items[0], items[1])*nCr(N-items[0]-items[1], items[2])* \
                    (PEd**(evade_counts[i][0]))*(PFd**(evade_counts[i][1]))*(PBd**(evade_counts[i][2]))
            if (i < len(evade_counts)-1):
                if ((evade_counts[i+1][0]) < evade_counts[i][0]):
                    n = n + 1
        Def_EV = 0
        for i in range(len(PE[0,:])-1, -1, -1):
            Def_EV = PE[0,i]*(n-i) + Def_EV
    return evade_counts, def_combs, PE[0,:], Def_EV

hit_counts, atk_combs, PH, Atk_EV = Atk_P(3, focus= True)

evade_counts, def_combs, PE, Def_EV = Def_P(3, focus= False)