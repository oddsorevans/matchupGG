import requestsGG
import spreadsheet
import time
import json
import sys

events = json.loads(sys.argv[6])#get from api explorer. Instructions in README
results = {}
authToken = sys.argv[1] #start.gg auth token. Link to instructions in README
pathToSpreadsheetJSON = sys.argv[2]
spreadsheetName = sys.argv[3]
head2head = sys.argv[4]
allWL = sys.argv[5]
players = json.loads(sys.argv[7])

def loadPlayers():

    for i in range(int(len(players)/2)):
        player = players[i*2]
        slug = players[i*2+1]
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

loadPlayers()
updateByTournament()
name = spreadsheet.setUpSpread(spreadsheetName, head2head, pathToSpreadsheetJSON)
spreadsheet.uploadMU(results, name, spreadsheetName, head2head, pathToSpreadsheetJSON)
spreadsheet.dumpAll(results, spreadsheetName, allWL, pathToSpreadsheetJSON)