from distutils.command.clean import clean
from graphqlclient import GraphQLClient
import json
from pprint import pprint

apiVersion = 'alpha'

def makeConnection(authToken: str):
    client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
    client.inject_token('Bearer ' + authToken)
    return client

def resultsByID(id: int, authToken: str):
    client = makeConnection(authToken)
    query = '''query Sets($playerID: ID!) {
    player(id: $playerID) {
        id
        sets(perPage: 20, page: 1) {
        nodes {
            id
            displayScore
            event{
            id
            name
            tournament{
                id
                name
            }
            }
        }
        }
    }
    }'''
    qvars = {
        "playerID":id
    }
    result = client.execute(query, qvars)
    return result

def getPlayerID(slug: str, authToken: str):
    client = makeConnection(authToken)
    query = '''
    query PlayerQuery {
        user(slug: "user/%s"){
            id
            player {
                id
                gamerTag
            }
        }
    }''' % (slug)
    qvars = {
        
    }
    result = json.loads(client.execute(query))
    pid = result["data"]["user"]["player"]["id"]
    return pid

def getEventsInTourney(slug:str):
    client = makeConnection()
    query = '''
    query TournamentQuery {
        tournament(slug: "%s"){
            name
            events {
                id
                name
            }
        }
    }''' % (slug)
    result = json.loads(client.execute(query))
    return result

def resultsByTournament(eventId: int, playerIds: list, authToken:str):
    print(eventId)
    client = makeConnection(authToken)
    query = '''
    query ResultsByTournament($eventID: ID, $playerIDS: [ID]){
        event(id: $eventID){
            tournament{
                id
                name
            }
            name
            sets(page:1, perPage: 100, filters:{
            playerIds: $playerIDS
            }
            ){
            nodes {
                id
                displayScore
            }
            }
        }
    }'''
    qvar = {
        "eventID":eventId,
        "playerIDS": playerIds
    }
    result = json.loads(client.execute(query, qvar))
    result.pop("extensions")
    result.pop("actionRecords")
    rList = resultList(result)
    return rList

def resultList(raw: dict):
    rList = []
    for sets in raw["data"]["event"]["sets"]["nodes"]:
        if sets["displayScore"] != "DQ" and sets["displayScore"] is not None:
            print(sets["displayScore"])
            game = sets["displayScore"].split()
            game = cleanGame(game)
            rList.append(game)
    return rList

def cleanGame(game:list):
    #create sub lists
    player1 = game[0: game.index("-")]
    player2 = game[game.index("-") + 1:]
    #remove tags
    if '|' in player1:
        player1 = player1[player1.index('|') +1:]
    if '|' in player2:
        player2 = player2[player2.index('|') +1:]
    #format and return
    name1 = " ".join([part for part in player1[0:-1]])
    score1 = player1[-1]
    name2 = " ".join([part for part in player2[0:-1]])
    score2 = player2[-1]

    return [name1, score1, name2, score2]

def printResults(result):
    with open("out.json", 'w') as fout:
        json.dump(result, fout)

    if 'errors' in result:
        print('Error:')
        print(result['errors'])
    else:
        print('Success!')

