import requestsGG
import spreadsheet
from pprint import pprint
import csv
import json
import time

#making sure import works
events = [737815,743267,749888,73682,763397,764792,774453,783911,785689,801230,811387,768247,821235,762987,774453,815767,792156]
results = {}

def loadPlayers():
    with open("extra/players.csv", 'r') as pList:
        csvreader = csv.reader(pList)
        header = next(csvreader)
        for line in csvreader:
            player = line[0]
            slug = line[1]
            results[player] = {
                "id": requestsGG.getPlayerID(slug),
                "wins": {

                },
                "losses":{

                }
            }

def updateByTournament():
    IDS = []
    for player in results:
        IDS.append(results[player]["id"])
        print(player)
    for event in events:
        matches = requestsGG.resultsByTournament(event, IDS)
        addWLs(matches)
        time.sleep(1)
        #pprint(matches)

def addWLs(matches: list):
    for match in matches:
        p1 = match[0]
        s1 = match[1]
        p2 = match[2]
        s2 = match[3]

        #account for name change
        if p1 == "Ender":
            p1 = "E.N.D."
        if p2 == "Ender":
            p2 = "E.N.D."

        #player 1 wins
        if s1 > s2 or (s1 == 'W' and s2 == 'L'):
            #if neither in
            if p1 not in results.keys() or p2 not in results.keys():
                if p1 not in results.keys() and p2 not in results.keys():
                    pass
                elif p1 not in results.keys():
                    if p1 not in results[p2]["losses"].keys():
                        results[p2]["losses"][p1] = 1
                    else:
                        results[p2]["losses"][p1] += 1
                elif p2 not in results.keys():
                    if p2 not in results[p1]["wins"].keys():
                        results[p1]["wins"][p2] = 1
                    else:
                        results[p1]["wins"][p2] += 1

            #add win if both present
            else:
                if p2 not in results[p1]["wins"].keys():
                    results[p1]["wins"][p2] = 1
                else:
                    results[p1]["wins"][p2] += 1
                #add losses
                if p1 not in results[p2]["losses"].keys():
                    results[p2]["losses"][p1] = 1
                else:
                    results[p2]["losses"][p1] += 1
        #player 2 wins
        else:
            if p1 not in results.keys() or p2 not in results.keys():
                if p1 not in results.keys() and p2 not in results.keys():
                    pass
                elif p1 not in results.keys():
                    if p2 not in results[p2]["wins"].keys():
                        results[p2]["wins"][p1] = 1
                    else:
                        results[p2]["wins"][p1] += 1
                elif p2 not in results.keys():
                    if p1 not in results[p1]["losses"].keys():
                        results[p1]["losses"][p2] = 1
                    else:
                        results[p1]["losses"][p2] += 1
            else:        
                #add win
                if p2 not in results[p2]["wins"].keys():
                    results[p2]["wins"][p1] = 1
                else:
                    results[p2]["wins"][p1] += 1
                #add losses
                if p1 not in results[p1]["losses"].keys():
                    results[p1]["losses"][p2] = 1
                else:
                    results[p1]["losses"][p2] += 1

def dumpOut(results):
    with open("extra/out.json", 'w') as fout:
        json.dump(results, fout)

loadPlayers()
updateByTournament()
dumpOut(results)
name = spreadsheet.setUpSpread()
spreadsheet.uploadMU(results, name)
spreadsheet.dumpAll(results)