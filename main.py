import requestsGG
import spreadsheet
from pprint import pprint
import csv
import json

#making sure import works
events = [651575,655158,672211,683629,632866,647605]
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
        #pprint(matches)

def addWLs(matches: list):
    for match in matches:
        p1 = match[0]
        s1 = match[1]
        p2 = match[2]
        s2 = match[3]

        #player 1 wins
        if s1 > s2:
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