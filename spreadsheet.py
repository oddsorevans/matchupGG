import gspread

def uploadMU(data: dict):
    gc = gspread.service_account("key/spreadsheetgg-ea20303b5576.json")
    sh = gc.open("Texoma Information")

    matchups = sh.worksheet("Matchups")
    matchups.update_acell("A2", "updated using python")

uploadMU({1:1})