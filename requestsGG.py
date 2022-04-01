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
    print(type(result))
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

def resultsByTournament(eventId: int, playerId: int):
    client = makeConnection()
    query = '''
    query ResultsByTournament{
    event(id: %d){
        sets(page:1, perPage: 10, filters:{
        playerIds: [%d]
        }
        ){
        nodes {
            id
            displayScore
        }
        }
    }
    }''' % (eventId, playerId)
    result = json.loads(client.execute(query))
    return result


def printResults(result):
    with open("out.json", 'w') as fout:
        json.dump(result, fout)

    if 'errors' in result:
        print('Error:')
        print(result['errors'])
    else:
        print('Success!')

def testing():
    print(getPlayerID("b7c78cda"))

testing()