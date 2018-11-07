import json
import fitbit
import gather_keys_oauth2 as Oauth2
import csv
import pandas as pd

import Datasets

CLIENT_ID = '22CYMV'
CLIENT_SECRET = '0d5156f3d38899575de0a735e176f894a26913c103009372556ce0804df00736'

ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UlhCU1giLCJhdWQiOiIyMkNZTVYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM1MTc4MjI3LCJpYXQiOjE1MzUxNDk0Mjd9.Q-JH16w3Ylrnj2657uPz0YdGS1jQ7f7rYwG8KhjoZEE'
REFRESH_TOKEN = '43658bd36064b445901c037b36e736d2f732067988509e964afb5a616aad5741'

BASE_URL = 'https://api.fitbit.com/1/user/-/activities/'

class DataCollector(object):
    server = None
    auth2_client = None
    def __init__(self):
        self.server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        # print(ACCESS_TOKEN, REFRESH_TOKEN)
        self.auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

    def request_data(self, keyword = ['heart','steps'], date = '2018-08-23'):
        heart_response = self.auth2_client.client.make_request(BASE_URL + keyword[0] + '/date/'+ date + '/1d/1min.json')
        step_response = self.auth2_client.make_request(BASE_URL + keyword[1] + '/date/' + date + "/1d/1min.json")

        heart_json_data = json.loads(heart_response.text)

        heart_rate = heart_json_data["activities-heart-intraday"]['dataset']
        steps = step_response['activities-steps-intraday']['dataset']

        # print(heart_response.text)
        # print(steps)
        comb_data = []

        hr_pointer, sp_pointer = 0, 0

        while hr_pointer < len(heart_rate):
            if steps[sp_pointer]['time'] != heart_rate[hr_pointer]['time']:
                sp_pointer += 1
                continue
            time = steps[sp_pointer]['time'].split(':')
            time.pop()
            time = ':'.join(time)
            comb_data.append((time, steps[sp_pointer]['value'], heart_rate[hr_pointer]['value']))
            sp_pointer += 1
            hr_pointer += 1

        # for item in comb_data:
        #     print(item)

        return comb_data


    def preprocess(self, data, date):
        date_arr = date.split('-')
        date_col = date_arr[1] + date_arr[2] + '_' + date_arr[0]
        print(date_col)
        segments = []
        subsegment = []

        foodlist = self.readfood('../Datasets/FoodLog-Silver.csv')

        id = '000'
        foodname = ''
        print(foodlist)
        # for item in data:
        #     print(item)

        # print(data)
        for row in data:
            if row[1] > 0:
                if len(subsegment) > 2:
                    segments.append(subsegment+[foodname])
                    subsegment.clear()
                    id = str(int(id) + 1)
                    foodname = ''
                    continue
            else:
                label = date + '-' + row[0]
                print(label)
                if label in foodlist.keys():
                    print(label)
                    foodname = foodlist[label]
                append_row = (date_col + '_' + id, *row)
                # print(append_row)
                subsegment.append(append_row)

        # for item in segments:
        #     print(item)

        return segments



    def write_data(self, food, data, start_time, duration,name = 'Silver', date = '2018-08-22'):
        # i = 0
        # while i < len(data) and data[i][0] != start_time:
        #     i += 1
        # print(data)
        processed_data = self.preprocess(data, date)

        # for item in processed_data:
        #     print(item)

        with open(name + date +'.csv', 'w') as csvfile:
            fieldnames = ['id', 'time', 'step', 'heartrate', 'food']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for segment in processed_data:
                food = segment[-1]
                for row in segment[:-1]:
                    # print(row)
                    writer.writerow({'id': row[0], 'time': row[1], 'step': row[2], 'heartrate': row[3], 'food': food})


    def readfood(self, filename):
        df = pd.read_csv(filename, encoding="ISO-8859-1")
        foodlist = {}
        for _, item in df.iterrows():
            foodlist[item[0]+ '-' +item[3]] = item[2]
        return foodlist

if __name__ == '__main__':
    data_collector = DataCollector()
    data = data_collector.request_data(date='2018-08-22')
    data_collector.write_data(food = 'Kongbao Chicken,Seasame Chicken', data = data, start_time='11:50:00', duration=20)
    # food = data_collector.readfood('../Datasets/FoodLog-Silver.csv')
