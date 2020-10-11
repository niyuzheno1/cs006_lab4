# autograder --- Student Version to grade all the files
#
# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import tinycss
from html.parser import HTMLParser
from html.entities import name2codepoint
import re

class FindGradColor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

    def read(self, data):
        self.pm = {}
        self.img = []
        self.datacollected = {}
        self.reset()
        self.alert = None
        self.alertp = False
        self.alertb = False
        self.alerta = False
        self.feed(data)
        return (self.datacollected,self.pm,self.img)
    def handle_starttag(self, tag, attrs):
        if tag in ["img"]:
            for attr in attrs:
                x,y = attr
                if x == 'src':
                    z = re.sub("Thanos_serious.jpg" , "", y)
                    if z == "":
                        continue
                    z = re.sub("Thanos_happy.jpg" , "", y)
                    if z == "":
                        continue
                    self.img.append(y)
        if tag in ["fefuncr", "fefuncg", "fefuncb"]:
            for attr in attrs:
                x,y = attr
                if x == 'tablevalues':
                    y = re.sub("\s\s+" , " ", y)
                    self.pm[tag] = y.split(" ")
        if tag in ["title", "h1", "footer", "ul", "ol", "address"]:
            if tag in ["address"]:
                self.alerta = True
            self.alert = tag
        if tag in ["p"]:
            self.alertp = True
        if tag in ["a"] and self.alerta:
            for attr in attrs:
                x,y = attr
                if x == 'href':
                    self.datacollected["email"] = re.sub("mailto:","",y)
        if tag in ["b"] and self.alertp == True:
            self.alertb = True
            self.alert = "aboutme"
    def handle_endtag(self, tag):
        if tag in ["title", "h1", "footer",  "ul", "ol", "address"]:
            self.alert = None
        if tag in ["address"]:
            self.alerta = False
        if tag in ["b"]:
            self.alertb = False
        if tag in ["p"]:
            self.alertp = False
            self.alert = None

    def handle_data(self, data):
        if self.alert is not None:
            if self.alert not in self.datacollected:
                self.datacollected[self.alert] = []
            ndata = re.sub(r"[\n\t\s]*", "", data)
            if ndata != '':
                self.datacollected[self.alert].append(data)
def fdgradcolor(html):
    s = FindGradColor()
    return s.read(html)


class ParseTable(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.stable = []
            
        if (tag == 'td') or (tag == 'th'):
            self.stable.append(1)

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.table.append(self.stable)

    def read(self, data):
        self.table = []
        self.stable = []
        self.feed(data)
        return self.table

def ftable(html):
    s = ParseTable()
    return s.read(html)

def main():
    f = open("C:\\Users\\zachn\\OneDrive\\Documents\\GitHub\\cs006_lab4\\index2.html", "r")
    html = f.read()
    errormsg = ""

    retx, rety, retz = fdgradcolor(html)
    try:
        f = open("index.html", "r")
        html = f.read()
    except:
        html = ""
        errormsg += "index.html does not exist\n"
    testx,testy, testz = fdgradcolor(html)

    total = []

    from PIL import Image
    
    pppoints = 10
    pppts = 0

    tb = ftable(html)
    xx = len(tb)
    if xx == 2:
        pppts = pppts + 1

    for i in range(0, xx):
        if len(tb[i]) == 4:
            pppts = pppts + 1

    pppoints = pppoints * (float(pppts) / 3.0)

    total.append(pppoints)

    for x in retx:
        if x in ['aboutme']:
            ndata1 = re.sub(r"[\n\t\s]*", "", retx[x][1])
            if x in testx:
                ndata2 = re.sub(r"[\n\t\s]*", "", testx[x][1])
            else:
                ndata2 = ndata1
            if ndata1 != ndata2:
                total.append(10)
            else:
                total.append(0)
        elif x in ['ol', 'ul']:
            ndata1 = ""
            for y in retx[x]:
                ndata1 = ndata1 + y
            ndata2 = ""
            if x in testx:
                for y in testx[x]:
                    ndata2 = ndata2 + y
                ndata1 = re.sub(r"[\n\t\s]*", "", ndata1)
                ndata2 = re.sub(r"[\n\t\s]*", "", ndata2)
            else:
                ndata1 = ndata2
            if ndata1 != ndata2:
                total.append(5)
            else:
                total.append(0)
        else:
            ndata1 = re.sub(r"[\n\t\s]*", "", retx[x][0])
            if x in testx:
                ndata2 = re.sub(r"[\n\t\s]*", "", testx[x][0])
            else:
                ndata2 = ndata1
            if ndata1 != ndata2:
                total.append(5)
            else:
                total.append(0)

    def changetofloat(x):
        y = []
        for i in range(0,2):
            if 'fefuncr' in x and 'fefuncg' in x and 'fefuncb' in x:
                try:
                    y.append((float(x['fefuncr'][i]),float(x['fefuncg'][i]),float(x['fefuncb'][i])))
                except:
                    if i == 0:
                        y.append((0.0,0.0,0.0))
                    else:
                        y.append((1.0,1.0,1.0))
            elif i == 0:
                y.append((0.0,0.0,0.0))
            else:
                y.append((1.0,1.0,1.0))
        return y

    rety = changetofloat(rety)
    testy = changetofloat(testy)

    ts = 10

    for i in range(0,2):
        if rety[i] == testy[i]:
            ts -= 5
    total.append(ts)

    total

    psscores = 10

    for x in testz:
        try:
            img = Image.open(x)
        except:
            psscores = psscores - 5
    psscores = (float(len(testz))/2.0) * psscores
    total.append(psscores)

    
    try:
        f = open("elements.css", "r")
        cssstyle = f.read()
    except:
        errormsg += "No elements.css file\n"
        cssstyle = ""

    cssparser = tinycss.make_parser()

    st = cssparser.parse_stylesheet(cssstyle)



    rules = {}

    for x in st.rules:
        tmp = {}
        switchs = False
        if x.selector[0].value in ['body', 'h1', 'nav', 'div']:
            switchs = True
            for decl in x.declarations:
                if decl.name == "color" or decl.name == "background-color":
                        if isinstance(decl.value[0],tinycss.token_data.FunctionToken):
                            tmp[decl.name] = ""
                            for y in decl.value[0].content:
                                tmp[decl.name] += str(y.value)
                        else:
                            tmp[decl.name] = decl.value[0].value
        if x.selector[0].value in ['header', 'h1', 'div']:
            switchs = True
            for decl in x.declarations:
                if decl.name == "border" or decl.name == "border-bottom":
                        if isinstance(decl.value[len(decl.value)-1],tinycss.token_data.FunctionToken):
                            tmp[decl.name] = ""
                            for y in decl.value[len(decl.value)-1].content:
                                tmp[decl.name] += str(y.value)
                        else: 
                            tmp[decl.name] = decl.value[len(decl.value)-1].value
                if decl.name == "background-color":
                        tmp[decl.name] = ""
                        for y in decl.value[0].content:
                            tmp[decl.name] += str(y.value)
        if (switchs == True):
            rules[x.selector[0].value] = tmp

    standard = {'body': {'background-color': '197,230,171', 'color': '88,38,128'}, 'div': {'background-color': '248,234,219', 'border': '42,69,20', 'border-bottom': '0,110,0'}, 'h1': {'background-color': '88,38,128', 'border-bottom': '255,165,0', 'color': '145,208,96'}, 'header': {'background-color': '248,234,219', 'border': '#582680', 'border-bottom': '#582680'}, 'nav': {'color': '145,208,96'}}
    def extractnewrules(standard, lst):
        colorgroup = {}

        for x in standard:
            for y in standard[x]:
                if standard[x][y] not in colorgroup:
                    colorgroup[standard[x][y]] = []
                colorgroup[standard[x][y]].append((x,y))

        newrule = {}
        for x in colorgroup:
            if x in lst:
                newrule[x] = colorgroup[x]

        return newrule

    list1 = ['248,234,219','42,69,20','145,208,96','88,38,128','255,165,0','#582680']
    nl = extractnewrules(standard,list1)


    list2 = []
    list1 = []

    # for x in nl:
    #     list1.append(x)

    list1 = ['88,38,128' , '42,69,20', '255,165,0', '145,208,96', '248,234,219', '#582680']

    for i in range(0,len(list1)):
        x = list1[i]
        flag = False
        for y in nl[x]:
            z, w = y
            if z in rules and w in rules[z]:
                list2.append(rules[z][w])
                flag = True
                break
        if flag == False:
            list2.append(list1[i])

    nl2 = extractnewrules(rules,list2)

    possiblescores = 30

    issues = 0
    
    for i in range(0,len(list1)):
        if list1[i] == list2[i]:
                issues = issues + 1
    if issues > 0:
        errormsg += "There are {0} being overlapped.\n".format(issues)
        possiblescores = possiblescores - 5 * issues
    if possiblescores > 0:
        issues = 0
        mains = 0
        for i in range(0,len(list1)):
            x = list1[i]
            for y in nl[x]:
                if y not in nl2[list2[i]]:
                    issues = issues + 1
                    mains = mains + 1
                else:
                    mains = mains + 1
        if issues > 0:
            errormsg += "There are {0} entries not present.".format(issues)
        possiblescores = (float(mains-issues)/float(mains) )*possiblescores
        possiblescores = round(possiblescores)
    total.append(possiblescores)

    outputhtml = ""

    f = open("vs.html", "w")


    for i in range(0,len(list1)):
        if ',' in list2[i]:
            outputhtml += "<div style=\"background-color: rgb("+list2[i]+")\">color" + str(i)+"</div>"
        else:
            outputhtml += "<div style=\"background-color: "+list2[i]+"\">color" + str(i)+"</div>"

    f.write(outputhtml)

    f.close()

    sumtotal = sum(total)

    total.append(errormsg)

    total.append(0)
    total.append(sumtotal)
    infolist = ["0. Table is correct with the number of rows and number of columns {0} / 10", "1. Title is correct and different from the given index.html {0}/5","2. H1 element is correct and different from the given index.html {0}/5","3. About me is correct {0}/10","4. Unorder List exists and differs from the given in index.html {0}/5","5. Order List exists and differs from the given in index.html {0}/5","6. Address differs from the given in index.html {0}/5","7. Email differs from the given in index.html {0}/5","8. Footer differs from the given in index.html {0}/5 ","9. Components having different color {0}/10", "10. Pictures exist and are in valid format {0}/10","11. CSS colors are correct and differ from the ones of css files in the folder {0}/30","Error Message: {0}","12. One color is another color's lighter version {0}/5 (Manual grading)", "total scores: {0}/110"]


    f = open("grades.txt", "w")

    outputinfo = ""
    for i in range(0,len(infolist)):
        outputinfo += infolist[i].format(total[i])
        outputinfo += "\n"
    f.write(outputinfo)

    f.close()
    return sumtotal, outputinfo