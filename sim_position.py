import pandas as pd
import random as R
import copy

def winChance(a, b, h=90):  # h is the rating boost given to the home team for calculating their winning chance
    return 1/(1+10**((b-(a+h))/400))

def newRatings(a, b, ka, kb, r, h=90):
    return (a + ka*(r-winChance(a,b,h)), b + kb*(-r+winChance(a,b,h)))


def simGame(a, b, regularSeason=False, printResult=False, h=90, k=47):
    global ratings
    global h2hWins

    homeRating = ratings[a]
    awayRating = ratings[b]

    s1 = winChance(homeRating, awayRating, h)
    s = R.random()
    if s < s1: r=1  # home win
    else: r=0  # road win

    hr, awr = newRatings(homeRating, awayRating, k, k, r, h)
    ratings[a] = hr  # update ratings
    ratings[b] = awr

    if printResult:
        print(a, "-", b, r)

    if regularSeason:
        try:
            h2hWins[a][b] += r    # add win against opponent
            h2hWins[b][a] += 1-r
        except KeyError:
            h2hWins[a][b] = r
            h2hWins[b][a] = 1-r
    
    return r


def simRS():
    global ug

    gamesLeft = ug.shape[0]
    
    for i in range(gamesLeft):
        homeTeam = ug.loc[i, "local.club.name"].upper()
        awayTeam = ug.loc[i, "road.club.name"].upper()

        simGame(homeTeam, awayTeam, regularSeason=True)


def standings(h2hWins):
    wins = {}
    for t in h2hWins.keys():
        wins[t] = sum(h2hWins[t].values())  # total number of wins
    groupedTeams = {}    # group teams by number of wins
    for t, w in wins.items():
        if w not in groupedTeams.keys():
            groupedTeams[w] = []
        groupedTeams[w].append(t)

    standings = []
    for _, group in sorted(groupedTeams.items(), reverse=True):
        wins2 = {}
        for t in group:
            wins2[t] = sum(h2hWins[t][o] for o in group if t != o)   # total number of wins between tied teams
        groupedTeams2 = {}   # group tied teams by number of wins between tied teams
        for t, w in wins2.items():
            if w not in groupedTeams2.keys():
                groupedTeams2[w] = []
            groupedTeams2[w].append(t)
        
        groupSorted = []        
        for _, group2 in sorted(groupedTeams2.items(), reverse=True):
            R.shuffle(group2)     # if still tied, randomly sort tied teams
            groupSorted.extend(group2)

        standings.extend(groupSorted)
    
    return standings

    
def sim(count):
    global h2hWins
    global ratingsCurrent
    global ratings
    global h2hCurrent
    global posCount

    for i in range(count):
        ratings = copy.deepcopy(ratingsCurrent)
        h2hWins = copy.deepcopy(h2hCurrent)
        simRS()
        st = standings(h2hWins)
        position = 1
        for t in st:
            posCount[t][position-1] += 1
            position += 1
          

def goThroughPlayed():
    global ratings
    global h2hWins
    global ratingsCurrent
    global h2hCurrent

    startElo = 1000

    gamesPlayed = min(pg.shape[0], 306)

    for i in range(gamesPlayed):
        ht = pg.loc[i, "hometeam"]
        awt = pg.loc[i, "awayteam"]
        hs = pg.loc[i, "homescore"]
        aws = pg.loc[i, "awayscore"]

        if i < 9:  # round 1
            ratings[ht] = startElo
            h2hWins[ht] = {}
            ratings[awt] = startElo
            h2hWins[awt] = {}

        if hs > aws: r = 1  # home win
        else: r = 0  # road win

        try:   # add win against opponent
            h2hWins[ht][awt] += r
            h2hWins[awt][ht] += 1-r
        except KeyError:
            h2hWins[ht][awt] = r
            h2hWins[awt][ht] = 1-r

        #print(ht, hs, "-", aws, awt)

        hr, awr = newRatings(ratings[ht], ratings[awt], 47, 47, r)

        ratings[ht] = hr      # update ratings
        ratings[awt] = awr

    ratingsCurrent = copy.deepcopy(ratings)
    h2hCurrent = copy.deepcopy(h2hWins)



try:
    pg = pd.read_csv("playedGames.csv")
    ug = pd.read_csv("upcomingGames.csv")
except FileNotFoundError:        
    import save_game_data
    pg = pd.read_csv("playedGames.csv")
    ug = pd.read_csv("upcomingGames.csv")
# to update played game data, run saveGameData.py or delete playedGames.csv and upcomingGames.csv


gamesPlayed = min(pg.shape[0], 306)


ratings = {}
h2hWins = {}  # matrix(dictionary) showing how many times each team beat every other team

ratingsCurrent = {}
h2hCurrent = {}


goThroughPlayed()


try:
    posCountDF = pd.read_csv("pos_" + str(gamesPlayed) + ".csv", index_col=0)
    posCount = posCountDF.to_dict()
except FileNotFoundError:
    posCount = {}   # dictionary where the final position of every team is saved after each simulation
    teams = ratings.keys()
    posCount = {t: {i: 0 for i in range(18)} for t in teams}
    

#sim(10000)


posCountDF = pd.DataFrame.from_dict(posCount)
posCountDF.to_csv("pos_" + str(gamesPlayed) + ".csv")  # if the number of games played is different, save the results in a separate file