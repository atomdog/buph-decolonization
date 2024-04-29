import json
import os
import pandas as pd

df = pd.read_json('cell.json')
affiliations = []
df2 = pd.DataFrame()

def standardString(stringin):
    if(stringin is not None):
        return(stringin.lower().replace("'","").replace('"', "").replace(",",""))
    else:
        return("")
for index, row in df.iterrows():
    ra = row['authorship']
    for authoraffsel in ra:
        aff = authoraffsel['affiliationTitle']
        name = authoraffsel['authorName']

        dadd = pd.DataFrame({"author": standardString(name), "affiliatedWith": standardString(aff).lower(), 'authorLink': authoraffsel['authorLink']}, index=[0])
        df2 = pd.concat([df2,dadd], axis=0, ignore_index=True)

print(df2.head())
print(len(df2))
print(len(df2['affiliatedWith'].unique()))




    