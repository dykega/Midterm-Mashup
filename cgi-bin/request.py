#!/usr/bin/env python

import urllib 
import json
import os
import datetime
#########  Functions  ########################

#API Key: a2wh83xfqpknrzsbn2ubeymr

def strip(string):
    out = ""
    out2 = ""
    html = False
    for pos in range(len(string)):
        if string[pos]=="<":
            html = True
        elif string[pos] ==">":
            html = False
        else:
            if not html:
                out += string[pos]
    html = False
    for pos in range(len(out)):
        if out[pos]=="&":
            html = True
        elif out[pos]==";":
            html = False
        else:
            if not html:
                out2 += out[pos]

    return str(out2)
        
def mdate (string):
    year = ""
    month = ""
    day = ""
    time = ""
    part = 0
    for pos in range(len(string)):
        if string[pos]=="-" or string[pos] =="T":
            part += 1
        else:
            if part == 0:
                year += string[pos]
            elif part == 1:
                month += string[pos]
            elif part == 2:
                day += string[pos]
            elif part == 3:
                time += string[pos]
    out = month +"/"+day+"/"+year+" at "+time
    return str(out)

def loc(string):
    out = ""
    for pos in range(len(string)):
        if string[pos]==" ":
            out += "+"
        else:
            out += string[pos]
    return str(out)

##########  Main  ##################

#Content-type: text/html
print('''

<html>
<head>
    <link rel="stylesheet" href="/MidtermMashupCSS.css" type="text/css" charset="utf-8"> 
    
</head>
<body>
        <div id="header">
            <h1 id="title">Activity Search</h1>
            <img id="title_image_1" src="/bg.jpg" width ="30%">
        </div>
    
        <div id="info">
            <h3>Hello and welcome to Activity Search! Activity Search is a great website to find fun and exciting things to do near YOU! Here are some instructions to help you find some amazing activities close by!</h3>
            <ol>
                <li>Enter the zip code near which you desire to find activities.</li>
                <li>Choose your desired radius (in miles) in which to search.</li>
                <li>Click Submit!</li>
            </ol>
            <form name="input" action="" method="get"> 
                Zip Code: <input type="text" name="zip" required>
                <select id = "dropDownSelector" name="radius">
                    <option></option>
                    <option value = "5">5 miles</option>
                    <option value = "10">10 miles</option>
                    <option value = "20">20 miles</option>
                    <option value = "30">30 miles</option>
                    <option value = "60">60 miles</option>
                </select>
                <input type="submit" value="Submit">
            </form>
        </div>
''')
#os.environ["QUERY_STRING"] = "zip=55057"
if os.environ["QUERY_STRING"] != "":
    qstrs = []
    qdic = {}
    x = os.environ["QUERY_STRING"]
    for item in x.split("&"):
        for val in item.split("="):
            qstrs.append(val)
    for pos in range(0,len(qstrs),2):
        if qstrs[pos] == "radius":
            qdic["radius"]=qstrs[pos+1]
        elif qstrs[pos] == "zip":
            qdic["zip"]=qstrs[pos+1]
    urlStr = "http://api.amp.active.com/v2/search?near=" + str(qdic["zip"])
    if "radius" in qdic.keys():
        urlStr += "&radius="+qdic["radius"]
    urlStr += "&start_date=" + str(datetime.date.today()) + ".."
    urlStr+="&api_key=a2wh83xfqpknrzsbn2ubeymr&sort=distance"
    #url = urllib.urlopen("http://api.amp.active.com/v2/search?query=running&category=event&start_date=2013-07-04..&near=San%20Diego,CA,US&radius=50&api_key=a2wh83xfqpknrzsbn2ubeymr")
    url = urllib.urlopen(urlStr)
    line = url.readline()
    dic = json.loads(line)
    res = dic['results']
    disp = []
    maxNum = 5
    if len(res) < 5:
        maxNum = len(res)
    for pos in range(maxNum):
        lst = []
        try:
            date = mdate(res[pos]['activityStartDate'])
        except:
            date = "No date given"
            
        try:
            name = strip(res[pos]['assetName'])
        except:
            name = "None"
        try:
            desc = strip(res[pos]['assetDescriptions'][0]['description'])
        except:
            desc = name
        addr = strip(res[pos]['place']['addressLine1Txt']) + ", " + strip(res[pos]['place']['cityName']) + ", " + strip(res[pos]['place']['stateProvinceCode'])
        loca = loc(addr)
        lst.append(name)
        lst.append(desc)
        lst.append(addr)
        lst.append(date)
        lst.append(loca)
        disp.append(lst)
    beginUrl = "http://maps.googleapis.com/maps/api/staticmap?&size=600x300&sensor=false"
    markers = ""
    colors = ['green', 'purple', 'yellow', 'blue', 'red']
    labels = ['A','B','C','D','E']
    for x in range(maxNum):
        markers+="&markers=color:"+colors[x]+"%7Clabel:"+labels[x]+"%7C"+disp[x][4]
    mapUrl = beginUrl+markers
    print('''<p><img id="map" src="'''+ mapUrl +'''"></p>''')

    for pos in range(maxNum):
        print("<h3>"+disp[pos][0]+"</h3>")
        print("<ul>")
        for x in range(1,4,1):
            print("<li>" + disp[pos][x]+"</li>")
        print("</ul>")

print("</body></html>")
