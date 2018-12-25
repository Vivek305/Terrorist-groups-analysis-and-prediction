from flask import Flask, render_template
from flask import request
from flask import Response,make_response
import pickle
import json
import io
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('main.html')

@app.route('/geojson')
def renderGeoJSON():
    with open('countries.geo.json') as f:
        geodata = json.load(f)
        #geodata.headers.add('Access-Control-Allow-Origin', '*')
    return json.dumps(geodata)

@app.route('/data')
def renderData():
    with open('new.json') as d:
        data = json.load(d)
        #data.headers.add('Access-Control-Allow-Origin', '*')

    return json.dumps(data)

    #else:
        #X = [iyear, country, crit1, crit2, crit3, attacktype1, targtype1, targsubtype1, weaptype1, weapsubtype1, ransom], #TODO: reshape to 1D array
@app.route('/formdata', methods=['GET', 'POST'])
def indexform(result=None,result1=None,result2=None,country=None,groupname=None):

    with open('countries.txt', 'rb') as fid:
        countriesdict = pickle.load(fid)

    attacktype = {'Armed Assault': 2,'Assassination': 1,'Bombing/Explosion': 3,'Facility/Infrastructure Attack': 7,'Hijacking': 4,
     'Hostage Taking (Barricade Incident)': 5,
     'Hostage Taking (Kidnapping)': 6,
     'Unarmed Assault': 8,
     'Unknown': 9}

    targettype = {'Abortion Related': 5,'Airports & Aircraft': 6,'Business': 1,'Educational Institution': 8,
    'Food or Water Supply': 9,'Government (Diplomatic)': 7,
     'Government (General)': 2,
     'Journalists & Media': 10,
     'Maritime': 11,
     'Military': 4,
     'NGO': 12,
     'Other': 13,
     'Police': 3,
     'Private Citizens & Property': 14,
     'Religious Figures/Institutions': 15,
     'Telecommunication': 16,
     'Terrorists/Non-State Militia': 17,
     'Tourists': 18,
     'Transportation': 19,
     'Unknown': 20,
     'Utilities': 21,
     'Violent Political Party': 22}


    weaptype = {'Biological': 1,
     'Chemical': 2,
     'Explosives/Bombs/Dynamite': 6,
     'Fake Weapons': 7,
     'Firearms': 5,
     'Incendiary': 8,
     'Melee': 9,
     'Other': 12,
     'Radiological': 3,
     'Sabotage Equipment': 11,
     'Unknown': 13,
     'Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)': 10}
    #data=['Predicted Group']
    if request.args.get('myCountry',None):
        country = process_text(request.args['myCountry'])

    if request.args.get('attacktype', None):
        result = process_text(request.args['attacktype'])

    if request.args.get('targtype',None):
        result1 = process_text(request.args['targtype'])

    if request.args.get('weaptype',None):
        result2 = process_text(request.args['weaptype'])
    years = [2010,2011,2012,2013,2014,2015]
    data = [0.0,0.0,0.0,0.0,0.0,0.0]

    #predict Group
    if result != None and result1 != None and result2 != None and country != None:

        with open('my_dumped_classifier.pkl', 'rb') as fid:
            model_loaded = pickle.load(fid)

            iyear = 2018
            icountry = countriesdict[country]
            iattacktype = attacktype[result]
            itargtype = targettype[result1]
            iweaptype = weaptype[result2]

            X = [iyear, icountry, iattacktype, itargtype, iweaptype],
            groupname = model_loaded.predict(X)

            print("ID is "+str(groupname))
            senddata = str(groupname).strip("[]").strip('\'')
            print("SEND DATA "+senddata)
            groupname = senddata
            data = predictedgroupdata(senddata)
            #print(kills)

    out = pd.DataFrame({'Years' : years, 'Kills' : data})
    out.to_csv('groupkills.csv', index=False, encoding='utf-8')
    vis = all(v == 0 for v in data)
    print("VIS "+str(vis))
    return render_template('form.html',groupname=groupname,vis=vis)

@app.route('/groupkills')
def showgroupkills():
    f = pd.read_csv('groupkills.csv',encoding="ISO-8859-1")
    resp = make_response(f.to_csv())
    return resp

@app.route('/sankeydata')
def getsankeydata():
    with open('sankeydata.json') as d:
        data = json.load(d)

    return json.dumps(data)

def process_text(text):
    return text

def predictedgroupdata(groupname):
    with open('groupkills.txt', 'rb') as fid:
        groupkills = pickle.load(fid)
        res = groupkills[groupname]
        years = [2010,2011,2012,2013,2014,2015]
        val = []
        for x in years:
            if x in res:
                val.append(res[x])
            else:
                val.append(0)
    print(val)
    return val

@app.route('/linechart')
def getlinechartdata():
    f = pd.read_csv('multiline_data.csv',encoding="ISO-8859-1")
    resp = make_response(f.to_csv())
    #resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    #resp.headers["Content-Type"] = "text/csv"
    return resp


if __name__ == '__main__':
    app.run(debug=True)
