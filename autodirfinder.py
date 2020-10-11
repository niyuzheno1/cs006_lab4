import glob, os, re
import grading
import pandas as pd
directory = "C:\\Users\\zachn\\OneDrive\\Documents\\labs\\lab4\\tmp"

os.chdir(directory)

text_file = open(directory + "\\result.txt", "w")

def strcmp(x,y):
    u = re.sub(r"[\n\t\s]*", "",x)
    u = u.lower()
    if (u == y):
        return True
    return False

def directory_find(root='.'):
    for path, dirs, files in os.walk(root):
        if ".c9" in path:
            continue
        for x in dirs:
            if strcmp(x,"lab4"):
                return os.path.join(path, x)
    return None

def findallfiles(x):
    for u in x:
        if re.search('.html', u) is not None and re.search('.html', u).group(0) is not None and re.search('.html', u).group(0) != "":
            return True
    return False

def directory_find2(root='.'):
    for path, dirs, files in os.walk(root):
        if findallfiles(files):
            return  os.path.join(path)
    return None   

def finducridinpath(x):
    ucridextractor = ""
    for i in range(0, len(x)):
        if x[i] == '8' and x[i+1] == '6':
            for j in range(i, len(x)):
                if not x[j].isnumeric():
                    break
                ucridextractor = ucridextractor + x[j]
        if ucridextractor != "":
            break
    return ucridextractor

distribution = []

currentlevel = next(os.walk('.'))[1] 

def gradeit():
    sum,output = grading.main()
    return sum,output

dataofstudents = {'Name' :[] , 'ID': [], 'scores': [], 'comments' : []}

for x in currentlevel:
    try:
        df = directory_find(directory+ "\\{0}\\environment\\".format(x))
        bfl = False 
        if df is None:
            text_file.write(x)
            text_file.write("\n")
        else:
            os.chdir(df)
            df2 = directory_find2(df)
            if df2 is None:
                text_file.write(x)
                text_file.write("\n")
                continue
            os.chdir(df2)
            ucrid = finducridinpath(df2)
            result, cmts = gradeit()
             

            ucridtoname = {"862016531" : "amraleryani",
                "860892009" : "abidali",
                "862010425" : "ritabutrus",
                "862152262" : "ting-weichang",
                "862152474" : "mincongchen",
                "862256892" : "yihanchen",
                "862062100" : "flaviocolana",
                "862167761" : "martincruz",
                "862180713" : "jaselledavalos",
                "862093086" : "parkerhadley",
                "862169412" : "alitzelholguin",
                "861308507" : "vanessainzunza",
                "861280545" : "christopherlu",
                "862130948" : "nayelimartinezmagana",
                "862075415" : "fionamorgan",
                "862128396" : "hadiyahmuhammad",
                "862114738" : "richardromero",
                "862047033" : "lisatran",
                "862149459" : "aayudhupadhyaya",
                "862088057" : "eduardovazquez",
                "861273076" : "andrewwang"
                }
            
            dataofstudents['Name'].append(ucridtoname[ucrid])
            dataofstudents['ID'].append(ucrid)
            dataofstudents['scores'].append(result)
            dataofstudents['comments'].append(cmts)

            bfl = True  
    except OSError as e:
        text_file.write(x)
        text_file.write("\n")
text_file.close()

columnname = []
for x in dataofstudents:
    columnname.append(x)
dataframeproduced = pd.DataFrame(data=dataofstudents, columns = columnname)
dataframeproduced.to_csv(directory+"\\result.csv", sep=',', encoding='utf-8')