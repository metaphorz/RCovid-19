from flask import Flask, render_template
from data import Articles
from flask_cors import CORS, cross_origin
import csv
from flask import render_template, url_for, request, redirect


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'

@app.route('/about', methods=['GET','POST'])
@cross_origin(origin='*')
@cross_origin(supports_credentials=True)
def getData():
    print(request.get_json())
    if request.get_json().get('placeValue'):
        placeValue = request.get_json().get('placeValue')
        print("place value if", placeValue)
    else:
        placeValue = "Dallas"
    print("Place value => ", placeValue)
    returnObject = {}
    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['confirmed'] = row
    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['deaths'] = row
    return returnObject

@app.route('/texasData', methods=['GET','POST'])
@cross_origin(origin='*')
@cross_origin(supports_credentials=True)
def getTexasData():
    print(request.get_json())
    if request.get_json().get('placeValue'):
        placeValue = request.get_json().get('placeValue')
        print("place value TexasConfirmedDeaths", placeValue)
    else:
        placeValue = "Texas"
    print("Place value TexasConfirmedDeaths=>  ", placeValue)
    returnObject = {}
    returnObject['texasDataRows'] =[]
    returnObject['texasDeathsCardRow'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDataRows'].append(row)

    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDeathsCardRow'].append(row)
    return returnObject

@app.route('/DFWData', methods=['GET','POST'])
@cross_origin(origin='*')
@cross_origin(supports_credentials=True)
def getDFWData():
    print(request.get_json())
    if request.get_json().get('placeValue','counties'):
        placeValue = request.get_json().get('placeValue')
        counties = request.get_json().get('counties')
        print("place value DFWdConfirmed", placeValue)
        print(len(counties))
        print("counties---inPy", counties)
    else:
        placeValue = "Texas"
        counties = ["Collin","Dallas","Denton","Ellis","Hood","Hunt","Johnson","Kaufman","Parker","Rockwall","Somervell","Tarrant","Wise"]

    print("Place value DFW=>  ", placeValue)
    returnObject = {}
    returnObject['dfwDataRows'] =[]
    returnObject['dfwDataDeathRows'] =[]

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataRows'].append(row)

    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataDeathRows'].append(row)
    return returnObject

@app.route('/hospitalBedInfo', methods=['GET','POST'])
@cross_origin(origin='*')
@cross_origin(supports_credentials=True)
def getDataHospital():
    print(request.get_json())
    if request.get_json().get('Texas'):
        placeValue = request.get_json().get('Texas')
        print("place value if", placeValue)
    else:
        placeValue = "Texas"
    print("US => ", placeValue)
    returnObject = {}
    returnObject['USBeds'] = []

    with open('Hospitalization_all_locs.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['location_name']:
                returnObject['USBeds'].append(row)

    return returnObject

if __name__ == '__main__':
    app.run(debug = True)
