import numpy as np 
import pandas as pd 
from itertools import combinations_with_replacement
from itertools import chain
import operator as op 
from functools import reduce
from _collections import defaultdict

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

def find_PH(M):
    hit_counts = list()
    PH = np.zeros((1,M+1))
    m = 0
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
            nCr(M, items[0])*nCr(M-items[0], items[1])*nCr(M-items[0]-items[1], items[2])* \
                (PHa**(hit_counts[i][0]))*(PFa**(hit_counts[i][1]))*(PBa**(hit_counts[i][2]))
        if (i < len(hit_counts)-1):
            if ((hit_counts[i+1][0]) < hit_counts[i][0]):
                m = m + 1
        elif (i == 0):
            m = m + 1
    return PH


def P_nsuccess(M, n, a_or_d = 'a'):
    #the probability of n successes in M dice rolled without modification or re-roll
    # M is the number of dice
    # n is the number of successes (hits or evades)
    # a_or_d is either 'a' or 'd'
    if a_or_d == 'a':
        PH = find_PH(M)
        if n < len(PH[0,:]):
            P_n = PH[0, M-n]
    return PH, P_n


#Calc nominal dice roll probs
def Atk_P(M, focus = False, target_lock = False):
    hit_counts = list()
    fhit_counts = list()
    m = 0

    #Decision Branch
    #If no F and no TL then do Raw Roll
    #If F and no TL then do Focus
    #If TL do TL then Focus

    #### Raw Roll ####
    if focus == False:
        PH = find_PH(M)
                    
    #Calc the Focus hocus pocus
    if (focus == True) and (target_lock == False):
        hits = dict(list())
        for atk_combs in combinations_with_replacement(A_dice, M):
            print("roll combos", atk_combs)
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
            if str(fhit_counts[i][0]) in hits.keys():
                hits[str(fhit_counts[i][0])].append(P_holder)
            else:
                hits[str(fhit_counts[i][0])]= [P_holder]
        for key in hits.keys():
            PH[0, M- int(key)] = sum(hits[key])

    #Calc Target Lock Dice roll
    if target_lock == True:
        PH_rr = PH.copy()
        if focus == False:
            
            #P(0 in 3) = P(0 in 3)*P(0 in 3)
            #P(1 in 3) = P(1 in 3)*P(0 in 2) + P(0 in 3)*P(1 in 3)
            #P(2 in 3) = P(2 in 3)*P(0 in 1) + P(1 in 3)*P(1 in 2) + P(0 in 3)*P(2 in 3)
            #P(3 in 3) = P(3 in 3)*P(0 in 0) + P(2 in 3)*P(1 in 1) + P(1 in 3)*P(2 in 2) + P(0 in 3)*P(3 in 3) 
            #for l in range(len(PH[0, :])) (0, 1, 2, 3)
                #for k in range(len(PH[0,:]),-1, -1): (3, 2, 1, 0)
                    #for j in range(M-k):   (0), (0,1), (0, 1, 2), (1, 2, 3)
                        #Take the kth element in PH, multiply by P_n(n im M) where n is j and M is 
            # then the 2 and third, then third second and 1st, then third second first and zeroth

            #as in P(N in M)*P(J in K)
            #PH is listed from max hits to zero
            for success in range(M+1):
                n = range(success, -1, -1)
                p_holder = 0
                for N in n:
                    
                    J = success - N
                    K = M-N
                    print("N =", N, "M = ", M, "J = ", J, "K = ", K, "successes = ", success)
                    ph, p_first_roll = P_nsuccess(M, N)
                    ph, p_second_roll = P_nsuccess(K, J)
                    p_holder = p_first_roll*p_second_roll + p_holder
                    if (N == n[-1]):
                        PH_rr[0, M-success] = p_holder
            PH = PH_rr[:]


            
    Atk_EV = 0
    m = M
    for i in range(len(PH[0,:])-1, -1, -1):
        Atk_EV = PH[0,i]*(m-i) + Atk_EV
    return PH[0,:], Atk_EV

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

hit_counts, atk_combs, PH, Atk_EV = Atk_P(3, focus= False, target_lock=True)

# evade_counts, def_combs, PE, Def_EV = Def_P(3, focus= False)