# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 18:04:45 2018

@author: Chris
"""

#ODI Match

from time import sleep
import os
import csv
import pandas as pd
import random
import pylab as pl
from scipy import stats, integrate
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import seaborn as sns
from os import rename, listdir
import collections
import matplotlib.patches as mpatches
import sys



os.chdir('C:\Users\Chris\Documents\Python Projects\ODI\matchdata\short')
data = pd.read_csv('out.csv')



#%% TEAMS
australia = ['David Warner', 'Travis Head', 'Steven Smith', 'Mitchell Marsh', 'Glenn Maxwell', 'Tim Paine', 'Mitchell Starc', 'Andrew Tye', 'Adam Zampa', 'Josh Hazlewood']
south_africa = ['Dean Elgar', 'Aiden Markram', 'Hashim Amla', 'AB de Villiers', 'Faf du Plessis', 'Quinton de Kock', 'Vernon Philander', 'Keshav Maharaj', 'Kagiso Rabada', 'Morne Morkel', 'Lungi Ngidi']
india = ['Shikhar Dhawan', 'Rohit Sharma', 'Suresh Raina', 'Virat Kohli', 'Manish Pandey', 'MS Dhoni', 'Hardik Pandya', 'Bhuvneshwar Kumar', 'Jaydev Unadkat', 'Yuzvendra Chahal', 'Shardul Thakur']
england = ['Jason Roy', 'Jonny Bairstow', 'Alex Hales', 'Joe Root', 'Eoin Morgan', 'Jos Buttler', 'Moeen Ali', 'Chris Woakes', 'Adil Rashid', 'Tom Curran', 'Mark Wood']
new_zealand = ['Kane Williamson', 'Martin Guptill', 'Colin Munro', 'Ross Taylor', 'Tom Latham', 'Henry Nicholls', 'Colin de Grandhomme', 'Mitchell Santner', 'Todd Astle', 'Tim Southee', 'Trent Boult']
#%% SELECTION

print 'Team 1 name?'
team1 = raw_input()
print 'Team 2 name?'
team2 = raw_input()

print 'Number of simulations to run: '
sims = raw_input()
sims = int(sims)

teams = {'australia': australia, 'south_africa': south_africa, 'india': india, 'england': england, 'new_zealand': new_zealand}

if team1 in teams:
    teamA = teams[team1]
if team2 in teams:
    teamB = teams[team2]
    
else:
    print("Uh oh, I don't know about that team")
    print ' '
    sleep(2)
    sys.exit()

print 'Sample size: (recommended: 1000)'
sample_size = raw_input()
sample_size = int(sample_size)

print 'Blara running simulations...'

default_scores = [
                30, # 1
                30, # 2
                30, # 3
                33, # 4
                30, # 5
                22, # 6
                15, # 7
                10, # 8
                10, # 9
                7,  # 10
                5]  # 11

"""
place_taker_score1 = 30
place_taker_score2 = 30
place_taker_score3 = 30
place_taker_score4 = 33
place_taker_score5 = 30
place_taker_score6 = 22
place_taker_score7 = 15
place_taker_score8 = 10
place_taker_score9 = 10
place_taker_score10 = 7
place_taker_score11 = 5
"""

#%% Creating variables

players = teamA



for player in players: 
    count = 0
    full_container = []
    for ball in data.batsman:    
        count += 1
        if ball == player:
          result = data.score[count]
          full_container.append(result)
    full_container = full_container[-sample_size:-1]
    #print full_container
    globals()[str(player) + '_stack'] = full_container
    
    
player_stacks = {} 
    
num = -1
for player in players:
    num += 1
    if num > 9:
        num = 'z'
    player_stacks[str(num) + str(player) + '_stack'] = globals()[str(player) + '_stack']

    
player_stacks = collections.OrderedDict(sorted(player_stacks.items()))



#%% scoring  

# NEED TO WORK OUT HOW TO SORT THE DICTIONARY


batting_no = 0
team_gen_scores = []


def simulate_innings(player_stacks):
    batting_no = 0
    balls_remaining = 300
    team_stacks_missing = 0
    team_score = 0
    for player in player_stacks:
        player_gen_scores = []
        over_stamp = 0
        batting_no += 1
        #print number
            
        player_innings = []
        player_running_score = []
        player_score = 0
        balls_faced = 0
        over = 1
        
        while True:
            balls_remaining -= 1
            balls_faced += 1
            over_stamp += 0.1
            test = over_stamp % 1
            test_clean = float (str (test)[:3]) 
            if test_clean == 0.6:
                over_stamp += 0.4
                over += 1
                #print test_clean  == 0.6  
            #else:
                #print test_clean  == 0.6                                     #TRYING TO MAKE BALL COUNTER SO WE CAN DIVIDE INNINGS INTO BLOCKS
            if player_stacks[player]:
                #print 'yes'
                res = random.choice(player_stacks[player])             #choose player here
            else:
                #print player, '  empty'
                player_score = default_scores[batting_no - 1]
                balls_remaining -= default_scores[batting_no - 1]
                
                team_stacks_missing += 1
                
                break
            try:
                result = int(res)
            except:
                result = str(res)
            if balls_remaining > 0:
                player_innings.append(result)
            #innings_matrix[number][balls_faced-1] = result
            if result == 'W' or balls_remaining < 1:
                break
            
        for ball in player_innings:
            try:
                player_score += ball
                player_running_score.append(player_score)
            except:
                #print 'wicket'
                pass
        player_gen_scores.append(player_score)
    
    #sleep(0.5)
    #print str(player), '  ', player_score
        team_score += player_score
        globals()[str(player) + '_scores'] = player_gen_scores
    return team_score, team_stacks_missing


    # output: a team score

for number in range(sims):
    score, team1_stacks_missing = simulate_innings(player_stacks)
    team_gen_scores.append(score)

h = sorted(team_gen_scores)            
#pl.hist(h,normed=True) 

#print h[-1]
avg = 0

for score in team_gen_scores:
    avg += score
print team1, ' average score across ', sims, ' sims: ', avg/sims


#%% Team 2





#%% Creating variables

#%% Creating variables

players2 = teamB
#players2 = ['Dean Elgar']


for player in players2: 
    count = 0
    full_container = []
    for ball in data.batsman:    
        count += 1
        if ball == player:
          result = data.score[count]
          full_container.append(result)
    globals()[str(player) + '_stack'] = full_container
    
    
player_stacks2 = {} 
    
num = -1
for player in players2:
    num += 1
    if num > 9:
        num = 'z'
    player_stacks2[str(num) + str(player) + '_stack'] = globals()[str(player) + '_stack']

    
player_stacks2 = collections.OrderedDict(sorted(player_stacks2.items()))




#%% scoring  

team_gen_scores2 = []


for number in range(sims):
    score, team2_stacks_missing = simulate_innings(player_stacks2)
    team_gen_scores2.append(score)

t2 = sorted(team_gen_scores2)            
#pl.hist(t2,normed=True) 

#print t2[-1]
avg = 0

for score in team_gen_scores2:
    avg += score
print team2, ' average score across ', sims, ' sims: ', avg/sims




#%% SIMO
team1_wins = 0 
team2_wins = 0

for number in range(sims):
    if team_gen_scores[number] > team_gen_scores2[number]:
        team1_wins += 1
    if team_gen_scores2[number] > team_gen_scores[number]:
        team2_wins += 1

team1_stacks_missing_no = float(team1_stacks_missing)/sims
team2_stacks_missing_no = float(team2_stacks_missing)/sims
                            
team1_winprob = float((float(team1_wins)/sims))  
team2_winprob = float((float(team2_wins)/sims))                         

print team1, ' % chance of win:  ', team1_winprob*100, '%'
print  team2, ' % chance of win:   ', team2_winprob*100, '%'

print team1, ' stacks missing: ', team1_stacks_missing_no
print team2, ' stacks missing: ', team2_stacks_missing_no
                                     
# IMPLIED ODDS
print ' '
print '---IMPLIED ODDS---'
print team1, round(1/team1_winprob, 2)
print team2, round(1/team2_winprob, 2)


sleep(1)
#pl.hist(h, histtype = 'stepfilled', normed=True) 
#pl.hist(t2,histtype = 'barstacked') 
print ' '
print 'Do you want to print the histograms...(y/n)?'
answer = raw_input()

if answer == 'y':   
    plt.hist(h, 30, facecolor='b', alpha=1)
    plt.hist(t2, 30, facecolor='r', alpha=0.5)
    red_patch = mpatches.Patch(color='red', label=team2)
    blue_patch = mpatches.Patch(color='blue', label=team1)
    plt.legend(handles=[red_patch, blue_patch])
elif answer == 'n':
    print "Ok, Blara will not print the graphs"
    sleep(1)
else:
    print 'Invalid answer'
    sleep(1)
