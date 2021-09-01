#! /usr/bin/env python3
'''
@file vote_weight.py
'''

import numpy as np
from matplotlib import pyplot as plt
from argparse import ArgumentParser
import csv
from scipy.special import comb
from scipy.stats import multinomial


def prCandidateWinsState(indvStateDict):
    '''
    prCandidateWinsState:
    Computes probability of a candidate winning a plurality in a given state
    modeled using a multinomial distribution
    
    Args:
    stateDict: dictionary of parameters for an individual state
    
    Returns:
    prCandidateWins
    '''
    
    #stateVotes = indvStateDict['PopularVotes']
    # Highly sensitive to the vote grid discretization
    stateVotes = 100
    prInd = 1.0 - indvStateDict['prBiden'] - indvStateDict['prTrump']
    if options.candidate == 'biden':
        prCand = indvStateDict['prBiden']
        prAlt = indvStateDict['prTrump']
    else:
        prCand = indvStateDict['prTrump']
        prAlt = indvStateDict['prBiden']
    
    
    
    
    prCandidateWins = 0
    # Use multinomial PMF to compute probabilites
    # kc, ka, ki index candidate, alt, ind respectively.
    # Build list of indices in which candidate wins
    voteGridPoints = stateVotes # Runs too slow with individual vote resolution
    voteGrid = np.round(np.linspace(0,stateVotes,voteGridPoints))
    
    candidateGrid = voteGrid[voteGrid > stateVotes/3.]
    
    for votesCand in candidateGrid:
        sumAltInd = stateVotes - votesCand
        altIndGrid = voteGrid[voteGrid<sumAltInd]
        for votesAlt in altIndGrid:
            votesInd = sumAltInd - votesAlt
            prVoteScenario = multinomial.pmf(x=[votesCand,votesAlt,votesInd], n=stateVotes, p=[prCand, prAlt, prInd])
            prCandidateWins += prVoteScenario
        
    
    return prCandidateWins


def buildStatesDict( inputCSV ):
    '''
    buildStatesDict:
    Get Dictionary of States with Electoral Votes and current polling. Estimates
    the expected voting population in each state.
    
    Args:
    inputCSV: input datafile. ArgumentParser() defaults this to StatePop.csv
    
    Returns:
    statesDict: nested dictionary of parameters for each state
    
    '''

    with open(inputCSV, mode='r') as infile:
        reader = csv.reader(infile)
        statesDict = {}
        for idx, line in enumerate(reader):
            if idx == 0:
                colHeaders = line
            else:
                indvStateDict = {}
                for fields in range(len(colHeaders)-1):
                    indvStateDict[colHeaders[fields+1]] = float(line[fields+1])
                statesDict[line[0]] = indvStateDict
    
    # Expected total votes as fraction of population
    voteFraction, totalPopulation = votingPop(statesDict)
    
    # Compute expected total votes and add to statesDict
    for state in statesDict:
        statesDict[state]['PopularVotes'] = np.round(voteFraction*statesDict[state]['Pop'])

    return statesDict

def totalPop( statesDict ):
# Get total population from statesDict
    population = 0
    for idx, state in enumerate(statesDict):
        population += statesDict[state]['Pop']
    return population
    
def votingPop( statesDict ):
# Get sum population of states 
    totalVotes_2016 = 128838342
    population_2016 = 323000000
    voteFraction = totalVotes_2016/population_2016
    
    totalPopulation_2019 = totalPop( statesDict )
    return voteFraction, totalPopulation_2019




if __name__=="__main__":
    
    parser = ArgumentParser()
    parser.add_argument("candidate", choices=['trump','biden'])
    parser.add_argument("-f", "--file", default="StatePop.csv", help="Data file to parse.")
    parser.add_argument("-s", "--states", nargs="*", help="State(s) to display info for. Defaults to print all")
    options = parser.parse_args()
    
    statesDict = buildStatesDict(options.file)    
    
    if not all(states in statesDict.keys() for states in options.states):
        print("Error, invalid state given. Remove spaces and use camelcase, i.e. Arizona or NewYork. Valid states are:")
        print(statesDict.keys())

    
    
    for state in options.states:
        statesDict[state]['prCandidateWins'] = prCandidateWinsState( statesDict[state] )
    
    
