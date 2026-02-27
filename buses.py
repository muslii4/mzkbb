import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import sheets_db

path = r"/home/sv/mzkbb/"
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
        return bus["vehicleId"] + ": " + bus["lineName"] + " na " + stops.get(bus["nearestSymbol"], bus["nearestSymbol"]) + " do " + bus["optionalDirection"] + "\n"
    except KeyError as e:
        return e

def getBuses():
    res = requests.get(runningVehiclesURL)
    return res.json()["vehicles"]

def getElectricBuses():
    buses = getBuses()
    electric_buses = sheets_db.get_electric_bus_numbers()

    msg = ""
    for i in buses:
        if i["vehicleId"] in electric_buses:
            msg += message(i)

    if msg == "":
        msg = "przykro mi, nie istnieją"
    return msg

def getHybridBuses():
    buses = getBuses()
    hybrid_buses = sheets_db.get_hybrid_bus_numbers()

    msg = ""
    for i in buses:
        if i["vehicleId"] in hybrid_buses:
            msg += message(i)

    if msg == "":
        msg = "przykro mi, nie istnieją"
    return msg

def getScaniaBuses():
    buses = getBuses()
    scania_buses = sheets_db.get_scania_bus_numbers()

    msg = ""
    for i in buses:
        if i["vehicleId"] in scania_buses:
            msg += message(i)

    if msg == "":
        msg = "miasto jest wolne od tych szczurów"
    else:
        msg += "proszę omijać z daleka"
    return msg

def getNumberOfScanias():
    buses = getBuses()
    scania_buses = sheets_db.get_scania_bus_numbers()
    
    n = 0
    for i in buses:
        if i["vehicleId"] in scania_buses:
            n += 1
    if n == 0 or n >= 5:
        return str(n) + " Scani na ulicach miasta"
    if n == 1:
        return str(n) + " Scania na ulicach miasta"
    if n >= 2 and n <= 4:
        return str(n) + " Scanie na ulicach miasta"

def getSpecialBuses():
    buses = getBuses()
    special_buses = sheets_db.get_special_buses()

    msg = ""
    for i in buses:
        if i["vehicleId"] in special_buses:
            msg += special_buses[i["vehicleId"]] + " " + message(i)

    if msg == "":
        msg = "jak ktoś tu jest specjalny to ty"
    return msg


if __name__ == "__main__":
    print(getElectricBuses())
    print(getScaniaBuses())
    print(getNumberOfScanias())
    print(getSpecialBuses())
