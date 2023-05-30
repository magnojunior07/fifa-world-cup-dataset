import json
import pandas as pd

with open('worldcup.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
dataframes = []
for obj in data:
    obj_list = [obj]
    df = pd.DataFrame(obj_list)
    dataframes.append(df)
    
combinedDF = pd.concat(dataframes, ignore_index=True)
combinedDF.to_csv('worldcup.csv', index=False)