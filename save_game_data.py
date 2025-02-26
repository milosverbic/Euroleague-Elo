from euroleague_api.game_stats import GameStats
import pandas as pd

gs = GameStats()

playedData = gs.get_game_metadata_season(2024)
playedDataSorted = playedData.sort_values(by=["gamenumber"], ignore_index=True)
playedDataSorted.to_csv("playedGames.csv")

gamesPlayed = playedDataSorted.shape[0]

parisFenerPlayed = gamesPlayed >= 243


gameCodeStart = gamesPlayed + 1
if not parisFenerPlayed: gameCodeStart += 1


l = []
for gc in range(gameCodeStart,307):
    if gc == 244 and not parisFenerPlayed:
        gr = gs.get_game_report(2024, 146)  # put the delayed paris fenerbahce game (game 146) after game 243 (round 27)
        l.append(gr)
    gr = gs.get_game_report(2024,gc)
    l.append(gr)
    
upcomingData = pd.concat(l, axis=0, ignore_index=True)

upcomingData.to_csv("upcomingGames.csv")