import json
from pprint import pprint
import pandas as pd





with open('Tools/Dataset1/foodlog2.json') as f:
    data = json.load(f)


def getMsData():
    hr_data = []

    for item in data['ms-band']:
        # print(data['ms-band'][item])
        hr_data.append(data['ms-band'][item])
    return hr_data


def getTimeInfo():
    fitbit_data = []

    for item in data['fitbit-band']:
        fitbit_data.append({"date": data['fitbit-band'][item]['date'],
                            "start": '{:02d}:{:02d}'.format(*divmod(data['fitbit-band'][item]['startMinute'], 60)),
                            "foodname": data['fitbit-band'][item]['foodname'] if "foodname" in data['fitbit-band'][item] else None,
                            "sugarlevel": data['fitbit-band'][item]['sugarlevel'] if "sugarlevel" in data['fitbit-band'][item] else None})
    return fitbit_data

def getFitbitData(fitbit_data):


    df = pd.read_csv("Tools/Dataset1/jordan2_segment copy 2.csv", encoding="ISO-8859-1")

    raw_data = []
    for index, row in df.iterrows():
        raw_data.append((row[0], row[1], row[2]))

    # print(raw_data)
    index = 0
    filter_fitbit_data = []

    while index < len(fitbit_data):
        # print(fitbit_data[index]['date'], fitbit_data[index]['start'])
        for row in range(len(raw_data)):
            date_arr = raw_data[row][0].split('_')
            date = date_arr[0] + "_" + date_arr[1]
            time = raw_data[row][1]
            if date == fitbit_data[index]['date']:
                if time == fitbit_data[index]['start']:
                    # print(fitbit_data[index]['date'], fitbit_data[index]['start'])
                    i = row
                    hr = []
                    while i < row + 20 and i < len(raw_data):
                        hr.append(raw_data[i][2])
                        i += 1

                    filter_fitbit_data.append({"foodname":fitbit_data[index]['foodname'],
                                                "heartrates": hr,
                                                   "sugarlevel":fitbit_data[index]['sugarlevel']})
                    index += 1
                    break
        index += 1


    # print(filter_fitbit_data)

    return filter_fitbit_data






# with open('Dataset1/jordan2_segment copy 2.csv') as f:




# with open('Dataset1/jordan2_segment copy 2.csv'):
