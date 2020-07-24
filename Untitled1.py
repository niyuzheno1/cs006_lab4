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



f = open("elements.css", "r")
cssstyle = f.read()


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
                    if isinstance(decl.value[4],tinycss.token_data.FunctionToken):
                        tmp[decl.name] = ""
                        for y in decl.value[4].content:
                            tmp[decl.name] += str(y.value)
                    else: 
                        tmp[decl.name] = decl.value[4].value
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
for x in nl:
    list1.append(x)
    for y in nl[x]:
        z, w = y
        if z in rules and w in rules[z]:
            list2.append(rules[z][w])
            break

nl2 = extractnewrules(rules,list2)


issues = 0

for i in range(0,len(list1)):
    if list1[i] == list2[i]:
            issues = issues + 1
colorunchange = 0
if issues > 0:
    colorunchange = colorunchange + issues

issues = 0
for i in range(0,len(list1)):
    x = list1[i]
    for y in nl[x]:
        if y not in nl2[list2[i]]:
            issues = issues + 1

