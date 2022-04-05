from graphqlclient import GraphQLClient
import json
from pprint import pprint

apiVersion = 'alpha'
authToken = 'a15f3f251d81704f6fcff229ee2840e0'

def makeConnection():
    client = GraphQLClient('https://api.smash.gg/gql/' + apiVersion)
    client.inject_token('Bearer ' + authToken)
    return client

def resultsByID(id: int):
    client = makeConnection()
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

def getPlayerID(slug: str):
    client = makeConnection()
    query = '''query PlayerQuery {
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

def resultsByTournament(eventId: int, playerIds: list):
    client = makeConnection()
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
        game = sets["displayScore"].split()
        #get rid of tags and excess
        while game[1] == '|':
            del game[1]
            del game[0]
        #seperate places since placement depends on others existence
        while game[4] == '|':
            del game[4]
            del game[3]
        del(game[2])
        rList.append(game)
    del rList[-1]
    return rList


def printResults(result):
    with open("out.json", 'w') as fout:
        json.dump(result, fout)

    if 'errors' in result:
        print('Error:')
        print(result['errors'])
    else:
        print('Success!')

def testing():
    print(getPlayerID("de8f2797"))

#printResults(resultsByTournament(683629, [933708, 816997, 1353105, 777742, 1386175]))