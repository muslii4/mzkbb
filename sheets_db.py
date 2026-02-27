import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd


path = r"/home/sv/mzkbb/"
runningVehiclesURL = "https://rozklady.bielsko.pl/getRunningVehicles.json"

with open(path + "apikey2.json") as f:
    apikey = json.load(f)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cred = ServiceAccountCredentials.from_json_keyfile_dict(apikey, scope)
client = gspread.authorize(cred)
sheet = client.open("autobusy").sheet1

data = sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])


def get_hybrid_bus_numbers():
    buses = df[df["hybrydowy"] == "TRUE"]
    return list(buses["nr taborowy"])


def get_electric_bus_numbers():
    buses = df[df["elektryczny"] == "TRUE"]
    return list(buses["nr taborowy"])

def get_scania_bus_numbers():
    buses = df[df["model"].str.lower().str.startswith("scania")]
    return list(buses["nr taborowy"])

def get_special_buses():
    buses = df[df["specjalny"] != ""]
    return dict(zip(buses["nr taborowy"], buses["specjalny"]))

if __name__ == "__main__":
    print(get_hybrid_bus_numbers())
    print(get_electric_bus_numbers())
    print(get_scania_bus_numbers())
    print(get_special_buses())
