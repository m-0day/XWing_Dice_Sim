import numpy as np 
import pandas as pd 
from itertools import combinations_with_replacement
from itertools import chain
import operator as op 
from functools import reduce
from _collections import defaultdict
import matplotlib.pyplot as plt 

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

# Find prob of hit "raw"
def find_PH_r(M):
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
    
# Find prob of hit "focus"
def find_PH_f(M):
    m = 0
    PH = np.zeros((1,M+1))
    hits = dict(list())
    hit_counts = list()
    fhit_counts = list()
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
    return PH

# Prob of n successes "focus". This is necessary for re-rolls.
def P_nsuccess_f(M, n, a_or_d = 'a'):
    #the probability of n successes in M dice rolled without modification or re-roll
    # M is the number of dice
    # n is the number of successes (hits or evades)
    # a_or_d is either 'a' or 'd'
    if a_or_d == 'a':
        P = find_PH_f(M)
        if n < len(P[0,:]):
            P_n = P[0, M-n]
    if a_or_d == 'd':
        P = find_PE_f(M)
        if n < len(P[0,:]):
            P_n = P[0, M-n]
    return P, P_n

# Prob of n successes "raw"
def P_nsuccess_r(M, n, a_or_d = 'a'):
    #the probability of n successes in M dice rolled without modification or re-roll
    # M is the number of dice
    # n is the number of successes (hits or evades)
    # a_or_d is either 'a' or 'd'
    if a_or_d == 'a':
        P = find_PH_r(M)
        if n < len(P[0,:]):
            P_n = P[0, M-n]
    if a_or_d == 'd':
        P = find_PE_r(M)
        if n < len(P[0,:]):
            P_n = P[0, M-n]
    return P, P_n


#### ATTACK ####
def Atk_P(M, focus = False, target_lock = False):
    PH = np.zeros((1,M+1))
    m = 0

    #Decision Branch
    #If no F and no TL then do Raw Roll
    #If F and no TL then do Focus
    #If TL do TL then Focus

    #### Raw Roll ####
    if (focus == False):
        PH = find_PH_r(M)
                    
    #### Calc the Focus ####
    if (focus == True) and (target_lock == False):
        PH = find_PH_f(M)

    #### Calc Target Lock Dice roll ####
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
                    ph, p_first_roll = P_nsuccess_r(M, N)
                    ph, p_second_roll = P_nsuccess_r(K, J)
                    p_holder = p_first_roll*p_second_roll + p_holder
                    if (N == n[-1]):
                        PH_rr[0, M-success] = p_holder
            PH = PH_rr[:]

        if focus == True:            
            for success in range(M+1):
                n = range(success, -1, -1)
                p_holder = 0
                for N in n:
                    
                    J = success - N
                    K = M-N
                    print("N =", N, "M = ", M, "J = ", J, "K = ", K, "successes = ", success)
                    ph, p_first_roll = P_nsuccess_f(M, N)
                    ph, p_second_roll = P_nsuccess_f(K, J)
                    p_holder = p_first_roll*p_second_roll + p_holder
                    if (N == n[-1]):
                        PH_rr[0, M-success] = p_holder
            PH = PH_rr[:]
            
    Atk_EV = 0
    m = M
    for i in range(len(PH[0,:])-1, -1, -1):
        Atk_EV = PH[0,i]*(m-i) + Atk_EV
    return PH[0,:], Atk_EV



#### EVADE ####
def find_PE_r(N, focus = False):
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
    return PE

def find_PE_f(M):
    m = 0
    PE = np.zeros((1,M+1))
    evades = dict(list())
    evade_counts = list()
    fevade_counts = list()
    for evade_combs in combinations_with_replacement(D_dice, M):
        print("roll combos", evade_combs)
        count_e = evade_combs.count('e') 
        count_f = evade_combs.count('f')
        count_b = evade_combs.count('b')
        fct_e = evade_combs.count('e')+evade_combs.count('f')
        fct_b = evade_combs.count('b')
        evade_counts.append((count_e, count_f, count_b))
        fevade_counts.append((fct_e, fct_b))
    evade_counts = list(dict.fromkeys(evade_counts))
    for i in range(len(evade_counts)):
        items = np.sort(evade_counts[i][:])
        items = items[::-1]
        P_holder = nCr(M, items[0])*nCr(M-items[0], items[1])*nCr(m-items[0]-items[1], items[2])* \
            (PEd**(evade_counts[i][0]))*(PFd**(evade_counts[i][1]))*(PBd**(evade_counts[i][2]))
        if str(fevade_counts[i][0]) in evades.keys():
            evades[str(fevade_counts[i][0])].append(P_holder)
        else:
            evades[str(fevade_counts[i][0])]= [P_holder]
    for key in evades.keys():
        PE[0, M- int(key)] = sum(evades[key])
    return PE

def find_PE_evade(N, focus = False, ev_cts = 0):
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
            #n is number of successes - 
            # if n <= ev_cts then n = ev_cts
            k = min(N - ev_cts, N - evade_counts[i][0])
            PE[0,k] = PE[0,k] + \
                nCr(N, items[0])*nCr(N-items[0], items[1])*nCr(N-items[0]-items[1], items[2])* \
                    (PEd**(evade_counts[i][0]))*(PFd**(evade_counts[i][1]))*(PBd**(evade_counts[i][2]))
            if (i < len(evade_counts)-1):
                if ((evade_counts[i+1][0]) < evade_counts[i][0]):
                    n = n + 1
        Def_EV = 0
    for i in range(len(PE[0,:])-1, -1, -1):
        Def_EV = PE[0,i]*(n-i) + Def_EV
    return PE

#Calc nominal evade dice rolls
def Def_P(M, focus = False, num_evade = 0):
    PE = np.zeros((1,M+1))
    m = 0

    #### Raw Roll ####
    if (focus == False):
        PE = find_PE_r(M)
                    
    #### Calc the Focus ####
    if (focus == True):
        PE = find_PE_f(M)

    # one for evade:
    if num_evade > 0:
        res_num_evade = min(M, num_evade)
        PE = find_PE_evade(M, ev_cts=res_num_evade)

    # need one for focus AND evade
    PE = PE.round(4)
    Def_EV = 0
    m = M
    for i in range(len(PE[0,:])-1, -1, -1):
        Def_EV = PE[0,i]*(m-i) + Def_EV
    return PE[0,:], Def_EV

def P_resolved_hits(M, N, atk_f = False, atk_tl = False, def_f = False, def_num_ev = 0):
    # This function returns an M+1 length array containing the pdf of resolved hits in a
    # given attack/def scenario.

    # M = num of Attack dice
    # N = num of Defense dice
    # 
    
    Ph_resolved = np.zeros(M+1)
 
    for m in range(M, -1, -1):
        n = m
        p_holder = 0
        hits = range(m,-1,-1)
        evades = range(n,-1,-1)

        ph, atk_ev = Atk_P(M, focus = atk_f, target_lock = atk_tl)
        pe, def_ev = Def_P(N, focus = def_f, num_evade = def_num_ev)
        #need to check the length of pe
        le = len(pe)
        lh = len(ph)
        if (le> len(ph)):
            # p_e = p_e.flip()
            p_e = pe[-1:lh-1:-1] #start from 0 evades (which is the end of the array) to whatever
        elif (le == len(ph)):
            p_e = pe[-1::-1]
        else:
            # p_e = p_e.flip()
            p_e = pe[-1::-1]
            p_e.extend(np.zeros(lh-le))

        for h in hits:
            
                #fill in the remainder of pe with zeros
                # for length of different ways to get h hits:
                #for M = 3, h = 3 there's one way
                #for M = 2, h = 2 there's two ways (3 hits, 1 evade + 2 hits, 0 evade)
            p_holder = 0
            for i in range(M, h-1, -1):
                p_holder = ph[M-i]*(p_e[M-i]) + p_holder
            Ph_resolved[M-h] = p_holder


    
    return Ph_resolved
M = 3
N = 3
P_resolved_hits(M, N, atk_f = False, atk_tl = False, def_f = False, def_num_ev = 0)


#### plots for hits ####

# fig, axes = plt.subplots(4, 5, sharey=True, sharex=True)
# fig.suptitle('X-wing Attack Dice Probability Density Functions (pdf)')
# axes[0,0].set_ylabel('Target Lock and Focus')
# axes[1,0].set_ylabel('Focus')
# axes[2,0].set_ylabel('Target Lock')
# axes[3,0].set_ylabel('No dice mods')
# axes.set_ylim(-0, 1)
# axes.set_xlim(-0.5,6.5)
# fig.text(0.35, 0.05, 'Number of Dice Rolled', va='center', rotation='horizontal')

# i = 0
# for f in (True, False):   
#     for tl in (True, False):
#         for M in range(1,6):
#             j = M-1
#             PH, Atk_EV = Atk_P(M, focus= f, target_lock= tl)
#             print ('Number of red dice =', M, ', Focus = ', f, ', Target Lock = ', tl, '\n', 'PH = ', PH, '. Expected number of hits = ', Atk_EV)
#             axes[i, j].bar(np.arange(len(PH)-1, -1, -1), PH, color = 'red', alpha = 0.7)
#             s = "Exp. Hits = " + str(Atk_EV)
#             axes[i,j].text(0.25, 0.85, s, color = 'black')
#         i = i + 1

# plt.show()

#### plots for evades ####

# fig, axes = plt.subplots(4, 5, sharey=True, sharex=True)
# fig.suptitle('X-wing Defense Dice Probability Density Functions (pdf)')
# axes[0,0].set_ylabel('Two Evade Tokens')
# axes[1,0].set_ylabel('One Evade Token')
# axes[2,0].set_ylabel('Focus')
# axes[3,0].set_ylabel('No dice mods')
# axes[0,0].set_ylim([0, 1])
# axes[0,0].set_xlim([-0.5,6.5])
# fig.text(0.35, 0.05, 'Number of Dice Rolled', va='center', rotation='horizontal')

# i = 0
# for ev in (range(2,0, -1)):
#     for M in range(1,6):
#         j = M-1
#         PE, Def_EV = Def_P(M, focus = False, num_evade = ev)
#         print ('Number of green dice =', M, ', Number of evades =', ev, '\n', 'PE = ', PE, '. Expected number of evades = ', Def_EV)
#         axes[i, j].bar(np.arange(len(PE)-1, -1, -1), PE, color = 'green', alpha = 0.7)
#         s = "Exp. Evades = " + str(Def_EV)
#         axes[i,j].text(0.25, 0.85, s, color = 'black')
#     i = i + 1

# for f in (True, False):   
#     for M in range(1,6):
#         j = M-1
#         PE, Def_EV = Def_P(M, focus = f, num_evade = 0)
#         print ('Number of green dice =', M, ', Focus = ', f, '\n', 'PE = ', PE, '. Expected number of evades = ', Def_EV)
#         axes[i, j].bar(np.arange(len(PE)-1, -1, -1), PE, color = 'green', alpha = 0.7)
#         s = "Exp. Evades = " + str(Def_EV)
#         axes[i,j].text(0.25, 0.85, s, color = 'black')
#     i = i + 1

# plt.show()

#### calculate and plot expected number of hits in a shootout ####
#
# several sheets of a grid of subplots of rows and columns
# each grid column is number of defense dice rolled: 1-6, each row is defender's token:
# 2 evades, 1 evade, 1 focus, or no mods
# there are 6 sheets, each one for the number of attack dice rolled in increasing number from 1-6

# 