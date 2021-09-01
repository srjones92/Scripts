#! /usr/bin/env python3
'''
@file vote_weight.py
'''

import numpy as np
from matplotlib import pyplot as plt
from scipy.special import comb



# Computes the probability that >=1 person at an event is covid positive for 
# an event with N attendees

# True case probability - compute an estimate based on rolling num.
# of cases in the last 10 days * some factor of estimated true cases vs
# true cases.
# e.g. .005 population tested positive * 10 estimated cases per 1 reported case
# then PrI = 0.05
PrI_Range = [.008,.03,.06, .1]

# Max number of people at an event
maxN = 50


plt.figure()


for PrI in PrI_Range:
    PrOneInfectionPresent = np.zeros(maxN)
    PrH = 1 - PrI
    for nAttendees in range(1,maxN+1):
        for k in range(1,nAttendees+1):
            PrOneInfectionPresent[nAttendees-1] += PrH**(k-1)*sum([PrI**l for l in range(1,nAttendees-k+1)])

    plt.plot(list(range(1,maxN+1)), PrOneInfectionPresent, label='PrI = {}'.format(PrI))

plt.legend()
plt.show()
