import gspread
import csv
import json

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


def setUpSpread():
    with open("extra/players.csv", 'r') as fin:
        csvreader = csv.reader(fin)
        header = next(csvreader)
        name = {}
        pos = 1
        for line in csvreader:
            name[line[0]] = pos
            pos += 1
    #rows & columns
    gc = gspread.service_account("key/spreadsheetgg-ea20303b5576.json")
    sh = gc.open("Texoma Information")
    matchups = sh.worksheet("Matchups")

    for key in name:
        matchups.update_cell(1, name[key] + 1, str(key))
        matchups.update_cell(name[key] + 1, 1, str(key))
    
    return name


def uploadMU(data: dict, pos:dict):
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

with open("extra/out.json", 'r') as fin:
    data = json.load(fin)

name = setUpSpread()
uploadMU(data, name)
