import requestsGG
import spreadsheet
import csv
import json
import time

events = [] #get from api explorer. Instructions in README
results = {}
authToken = '' #start.gg auth token. Link to instructions in README
pathToSpreadsheetJSON = "file path to authentication json key"
spreadsheetName = 'Spreadsheet name'
head2head = 'head 2 head worksheet name'
allWL = 'all matchups worksheet name'

def loadPlayers():
    with open("extra/players.csv", 'r') as pList:
        csvreader = csv.reader(pList)
        header = next(csvreader)
        for line in csvreader:
            player = line[0]
            slug = line[1]
            results[player] = {
                "id": requestsGG.getPlayerID(slug, authToken),
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
        matches = requestsGG.resultsByTournament(event, IDS, authToken)
        addWLs(matches)
        time.sleep(1)

def addWLs(matches: list):
    for match in matches:
        p1 = match[0]
        s1 = match[1]
        p2 = match[2]
        s2 = match[3]

        #account for name change mid season. Below is an example
        # if p1 == "Yu":
        #     p1 = "polanco"
        # if p2 == "Yu":
        #     p2 = "polanco"

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
                    if p1 not in results[p2]["wins"].keys():
                        results[p2]["wins"][p1] = 1
                    else:
                        results[p2]["wins"][p1] += 1
                elif p2 not in results.keys():
                    if p2 not in results[p1]["losses"].keys():
                        results[p1]["losses"][p2] = 1
                    else:
                        results[p1]["losses"][p2] += 1
            else:        
                #add win
                if p1 not in results[p2]["wins"].keys():
                    results[p2]["wins"][p1] = 1
                else:
                    results[p2]["wins"][p1] += 1
                #add losses
                if p2 not in results[p1]["losses"].keys():
                    results[p1]["losses"][p2] = 1
                else:
                    results[p1]["losses"][p2] += 1

def dumpOut(results):
    with open("extra/out.json", 'w') as fout:
        json.dump(results, fout)

loadPlayers()
updateByTournament()
dumpOut(results)
name = spreadsheet.setUpSpread(spreadsheetName, head2head, pathToSpreadsheetJSON)
spreadsheet.uploadMU(results, name, spreadsheetName, head2head, pathToSpreadsheetJSON)
spreadsheet.dumpAll(results, spreadsheetName, allWL, pathToSpreadsheetJSON)