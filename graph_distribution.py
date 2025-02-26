import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from PIL import Image
import numpy as np
import urllib.request

def abbreviate(name, inverse=False):
    s = {}
    for i in range(9):
        ht = ug.loc[i, "local.club.name"].upper()
        hts = ug.loc[i, "local.club.abbreviatedName"]
        awt = ug.loc[i, "road.club.name"].upper()
        awts = ug.loc[i, "road.club.abbreviatedName"]
        s[ht] = hts
        s[awt] = awts
    sInv = {v: k for k, v in s.items()}
    if inverse: return sInv[name]
    return s[name]
    
def teamCrests():
    crests = {}
    for i in range(9):
        ht = ug.loc[i, "local.club.name"].upper()
        hsl = ug.loc[i, "local.club.images.crest"]
        awt = ug.loc[i, "road.club.name"].upper()
        awsl = ug.loc[i, "road.club.images.crest"]
        crests[ht] = hsl
        crests[awt] = awsl
    return crests
    # doesn't work if upcomingGames.csv is empty (if the regular season is over)

try:
    pg = pd.read_csv("playedGames.csv")
    ug = pd.read_csv("upcomingGames.csv")
except FileNotFoundError:
    import save_game_data
    pg = pd.read_csv("playedGames.csv")
    ug = pd.read_csv("upcomingGames.csv")



order = [
    "Olympiacos",
    "Fenerbahce",
    "Panathinaikos",
    "Monaco",
    "Crvena Zvezda",
    "Bayern",
    "Paris",
    "Partizan",
    "Barcelona",
    "Milan",
    "Real",
    "Anadolu Efes",
    "Zalgiris",
    "Baskonia",
    "ASVEL",
    "Virtus",
    "Maccabi",
    "ALBA"
]

orderFullNames = [abbreviate(t, inverse=True) for t in order]


gamesPlayed = pg.shape[0]

filename = "pos_" + str(gamesPlayed) + ".csv"




posCount = pd.read_csv(filename, index_col=0)

teamNames = posCount.columns



fig, axs = plt.subplots(9,4, width_ratios=[1,10,1,10]) 

plt.suptitle("EuroLeague 2024/25 final standings - probability distribution\nRound 26", fontsize=18)




for i in range(9):
    for p in range(2):
        t = i+p*9
        x = [str(i+1) for i in range(18)]
        y = [posCount.loc[j, orderFullNames[t]] for j in range(18)]
        col = ["green"]*6 + ["blue"]*4 + ["red"]*8

        axs[i,1+p*2].bar(x, y, color=col)
        if i!=8:
            axs[i,1+p*2].get_xaxis().set_visible(False)
        axs[i,1+p*2].get_yaxis().set_visible(False)

        axs[i,1+p*2].spines["top"].set_visible(False)
        axs[i,1+p*2].spines["left"].set_visible(False)
        axs[i,1+p*2].spines["right"].set_visible(False)
        #axs[i,1+p*2].spines["bottom"].set_visible(False)

        url = teamCrests()[orderFullNames[t]]
        urllib.request.urlretrieve(url, "temp.png")
        img = np.asarray(Image.open("temp.png"))
        image = mpimg.imread("temp.png")
        axs[i,0+p*2].imshow(image)
        axs[i,0+p*2].set_facecolor("white")
        axs[i,0+p*2].get_xaxis().set_visible(False)
        axs[i,0+p*2].get_yaxis().set_visible(False)
        axs[i,0+p*2].spines["top"].set_visible(False)
        axs[i,0+p*2].spines["left"].set_visible(False)
        axs[i,0+p*2].spines["right"].set_visible(False)
        axs[i,0+p*2].spines["bottom"].set_visible(False)
        


print(y)
plt.text(12, -1*max(y), "github.com/milosverbic")


plt.show()