import gspread
import csv
import time

green = {
    "red": 0.0,
    "green": 1.0,
    "blue": 0.0
}
red = {
    "red": 1.0,
    "green": 0.0,
    "blue": 0.0
}
yellow = {
    "red": 1.0,
    "green": 1.0,
    "blue": 0.0
}

def colorCell(worksheet, cell, score):
    #win
    if int(score[0]) > int(score[2]):
        worksheet.format(cell, {
                    "backgroundColor": green,
                    "horizontalAlignment": "CENTER",
        })
    #loss
    elif int(score[0]) < int(score[2]):
        worksheet.format(cell, {
                    "backgroundColor": red,
                    "horizontalAlignment": "CENTER",
        })
    #tie
    else:
        worksheet.format(cell, {
                "backgroundColor": yellow,
                "horizontalAlignment": "CENTER",
        })


def playerPos(players: list):
    name = {}
    pos = 1
    for i in range(int(len(players)/2)):
        name[players[i*2]] = pos
        pos += 1
    return name

def setUpSpread(shName:str, h2hName:str, key:str, players:list):
    global totalWrites
    global startT
    startT = time.time()
    name = playerPos(players)
    #rows & columns
    gc = gspread.service_account(key)
    sh = gc.open(shName)
    matchups = sh.worksheet(h2hName)
    matchups.update_cell(0,0,"O↓P→")
    time.sleep(1)

    for key in name:
        matchups.update_cell(1, name[key] + 1, str(key))
        matchups.update_cell(name[key] + 1, 1, str(key))
        time.sleep(2)

    return name


def uploadMU(data: dict, pos:dict, shName:str, h2hName:str, key:str):
    global totalWrites
    global startT
    gc = gspread.service_account(key)
    sh = gc.open(shName)

    matchups = sh.worksheet(h2hName)
    for player in data:
        for win in data[player]["wins"]:
            score = ""
            if win in pos.keys():
                if win in data[player]["losses"].keys():
                    score = "%d-%d" % (data[player]["wins"][win], data[player]["losses"][win])
                else:
                    score = "%d-%d" % (data[player]["wins"][win], 0)
                index = chr(pos[player] + 65) + str(pos[win]+1)
                matchups.update_acell(index, score)
                colorCell(matchups, index, score)
                time.sleep(2)

        for loss in data[player]["losses"]:
            score = ""
            if loss in pos.keys():
                if loss in data[player]["wins"].keys():
                    score = "%d-%d" % (data[player]["wins"][loss], data[player]["losses"][loss])
                else:
                    score = "%d-%d" % (0, data[player]["losses"][loss])
                index = chr(pos[player] + 65) + str(pos[loss]+1)
                matchups.update_acell(index, score)
                colorCell(matchups, index, score)
                time.sleep(2)

def dumpAll(data: dict, shName:str, allName:str, key:str):
    global totalWrites
    global startT
    gc = gspread.service_account(key)
    sh = gc.open(shName)

    dump = sh.worksheet(allName)
    start = 1
    for player in data:
        dump.update_cell(start, 1, player)
        colorCell(dump, "A" + str(start), "1-1")
        start += 1
        time.sleep(2)
        dump.update_cell(start, 1, "WINS")
        colorCell(dump, "A" + str(start), "1-0")
        start += 1
        time.sleep(2)

        i = 1
        for opp in data[player]["wins"]:
            dump.update_cell(start, i, opp + " | " + str(data[player]["wins"][opp]))
            time.sleep(1)
            i += 1
            if(i > 5):
                start += 1
                i = 1
        start += 1
        dump.update_cell(start, 1, "LOSSES")
        colorCell(dump, "A" + str(start), "0-1")
        time.sleep(2)
        start += 1
        i = 1
        for opp in data[player]["losses"]:
            dump.update_cell(start, i, opp + " | " + str(data[player]["losses"][opp]))
            time.sleep(1)
            i += 1
            if(i > 5):
                start += 1
                i = 1
        start += 2
