import gspread
import csv
import json
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

#limit to 60 writes per second per user, so to get around this I put in a pause of 30 seconds
totalWrites = 0
startT = time.time()

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


def playerPos():
    with open("extra/players.csv", 'r') as fin:
        csvreader = csv.reader(fin)
        header = next(csvreader)
        name = {}
        pos = 1
        for line in csvreader:
            name[line[0]] = pos
            pos += 1
    return name

def setUpSpread():
    global totalWrites
    global startT
    startT = time.time()
    name = playerPos()
    #rows & columns
    gc = gspread.service_account("key/spreadsheetgg-ea20303b5576.json")
    sh = gc.open("Texoma Information")
    matchups = sh.worksheet("Matchups")

    for key in name:
        matchups.update_cell(1, name[key] + 1, str(key))
        matchups.update_cell(name[key] + 1, 1, str(key))
        totalWrites += 2
    
    if(totalWrites >= 60):
        end = time.time()
        print(f"waiting {60 - (end-startT)} seconds")
        time.sleep(60 - (end-startT))
        print("continued")
        startT = time.time()
        totalWrites = 0

    return name


def uploadMU(data: dict, pos:dict):
    global totalWrites
    global startT
    gc = gspread.service_account("key/spreadsheetgg-ea20303b5576.json")
    sh = gc.open("Texoma Information")

    matchups = sh.worksheet("Matchups")
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
                totalWrites += 2
                if(totalWrites >= 60):
                    end = time.time()
                    print(f"waiting {60 - (end-startT)} seconds")
                    time.sleep(60 - (end-startT))
                    print("continued")
                    startT = time.time()
                    totalWrites = 0

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
                totalWrites += 2
                if(totalWrites >= 60):
                    end = time.time()
                    print(f"waiting {60 - (end-startT)} seconds")
                    time.sleep(60 - (end-startT))
                    print("continued")
                    startT = time.time()
                    totalWrites = 0

def dumpAll(data: dict):
    global totalWrites
    global startT
    gc = gspread.service_account("key/spreadsheetgg-ea20303b5576.json")
    sh = gc.open("Texoma Information")

    dump = sh.worksheet("All Wins & Losses")
    start = 1
    for player in data:
        dump.update_cell(start, 1, player)
        colorCell(dump, "A" + str(start), "1-1")
        start += 1
        dump.update_cell(start, 1, "WINS")
        colorCell(dump, "A" + str(start), "1-0")
        start += 1
        totalWrites += 4
        if(totalWrites >= 60):
            end = time.time()
            print(f"waiting {60 - (end-startT)} seconds")
            time.sleep(60 - (end-startT))
            print("continued")
            startT = time.time()
            totalWrites = 0

        i = 1
        for opp in data[player]["wins"]:
            dump.update_cell(start, i, opp + " | " + str(data[player]["wins"][opp]))
            totalWrites += 1
            if(totalWrites >= 60):
                end = time.time()
                print(f"waiting {60 - (end-startT)} seconds")
                time.sleep(60 - (end-startT))
                print("continued")
                startT = time.time()
                totalWrites = 0
            i += 1
            if(i > 5):
                start += 1
                i = 1
        start += 1
        dump.update_cell(start, 1, "LOSSES")
        colorCell(dump, "A" + str(start), "0-1")
        totalWrites += 2
        if(totalWrites >= 60):
            end = time.time()
            print(f"waiting {60 - (end-startT)} seconds")
            time.sleep(60 - (end-startT))
            print("continued")
            startT = time.time()
            totalWrites = 0
        start += 1
        i = 1
        for opp in data[player]["losses"]:
            dump.update_cell(start, i, opp + " | " + str(data[player]["losses"][opp]))
            totalWrites += 1
            if(totalWrites >= 60):
                end = time.time()
                print(f"waiting {60 - (end-startT)} seconds")
                time.sleep(60 - (end-startT))
                print("continued")
                startT = time.time()
                totalWrites = 0
            i += 1
            if(i > 5):
                start += 1
                i = 1
        start += 2


""" with open("extra/out.json", 'r') as fin:
    data = json.load(fin)

time.sleep(5)
name = setUpSpread()
uploadMU(data, name)
dumpAll(data) """
