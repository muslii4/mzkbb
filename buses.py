import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

path = r"/home/muslii4/mzk/"
runningVehiclesURL = "https://rozklady.bielsko.pl/getRunningVehicles.json"

with open(path + "apikey2.json") as f:
    apikey = json.load(f)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cred = ServiceAccountCredentials.from_json_keyfile_dict(apikey, scope)
client = gspread.authorize(cred)
sheet = client.open("autobusy").sheet1

html = open(path + "stops.txt", "r", encoding="utf-8")

names = []
stops = {}

for i in html:
    if "data-display-name=" in i:
        names.append(i[i.index("data-display-name=")+19:i.index(')"', i.index("data-display-name="))+1])

for i in names:
    stops[i[i.index("(")+1:i.index(")")]] = i[0:i.index(" (")]

def message(bus):
    try:
        return bus["vehicleId"] + ": " + bus["lineName"] + " na " + stops[bus["nearestSymbol"]] + " do " + bus["optionalDirection"] + "\n"
    except KeyError as e:
        return e

def getBuses():
    res = requests.get(runningVehiclesURL)
    return res.json()["vehicles"]

def getRemainingBuses():
    existingBuses = []
    buses = getBuses()
    vals = sheet.get_all_values()

    for i in vals:
        if i[2] != "":
            existingBuses.append(i[0])

    msg = ""
    for i in buses:
        if i["vehicleId"] not in existingBuses:
            msg += message(i)

    if msg == "":
        msg = "brak"
    return msg

def getElectricBuses():
    buses = getBuses()

    msg = ""
    for i in buses:
        if int(i["vehicleId"]) > 226:
            msg += message(i)

    if msg == "":
        msg = "przykro mi, nie istnieją"
    return msg

def getScaniaBuses():
    buses = getBuses()

    msg = ""
    for i in buses:
        if 158 <= int(i["vehicleId"]) <= 167:
            msg += message(i)

    if msg == "":
        msg = "miasto jest wolne od tych szczurów"
    else:
        msg += "proszę omijać z daleka"
    return msg

def getNumberOfScanias():
    buses = getBuses()
    
    n = 0
    for i in buses:
        if 158 <= int(i["vehicleId"]) <= 167:
            n += 1
    if n == 0 or n >= 5:
        return str(n) + " Scani na ulicach miasta"
    if n == 1:
        return str(n) + " Scanię na ulicach miasta"
    if n >= 2 and n <= 4:
        return str(n) + " Scanie na ulicach miasta"
