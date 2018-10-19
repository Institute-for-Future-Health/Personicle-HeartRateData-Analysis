import json
import fitbit
import gather_keys_oauth2 as Oauth2
import csv

CLIENT_ID = '22CYMV'
CLIENT_SECRET = '0d5156f3d38899575de0a735e176f894a26913c103009372556ce0804df00736'
ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UlhCU1giLCJhdWQiOiIyMkNZTVYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHdhY3Qgd2xvYyIsImV4cCI6MTUzNDk4NzkwMiwiaWF0IjoxNTM0OTU5MTAyfQ.x_k9XNo6JFNme9ceS92rrRp1G9d9A6quQ5wikXuqliU'
REFRESH_TOKEN = '3de76efe34b7785806352ab63bb9a27525eb0dfa614371b3221b512fc65b3d5b'

BASE_URL = 'https://api.fitbit.com/1/user/-/activities/'

class DataCollector(object):
    server = None
    auth2_client = None
    def __init__(self):
        self.server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        # print(ACCESS_TOKEN, REFRESH_TOKEN)
        self.auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

    def request_data(self, keyword = ['heart','steps'], date = '2018-08-20'):
        heart_response = self.auth2_client.client.make_request(BASE_URL + keyword[0] + '/date/'+ date + '/1d/1min.json')
        step_response = self.auth2_client.make_request(BASE_URL + keyword[1] + "/date/" + date + "/1d/1min.json")

        heart_json_data = json.loads(heart_response.text)
        # step_json_data = json.loads(step_response)
        # print(heart_response.text)
        # print(step_response)
        heart_rate = heart_json_data["activities-heart-intraday"]['dataset']
        steps = step_response['activities-steps-intraday']['dataset']


        comb_data = []

        hr_pointer, sp_pointer = 0, 0

        while hr_pointer < len(heart_rate):
            if steps[sp_pointer]['time'] != heart_rate[hr_pointer]['time']:
                sp_pointer += 1
                continue
            comb_data.append((steps[sp_pointer]['time'], steps[sp_pointer]['value'], heart_rate[hr_pointer]['value']))
            sp_pointer += 1
            hr_pointer += 1

        # for item in comb_data:
        #     print(item)

        return comb_data

    def preprocess(self, data):
        segments = []
        subsegment = []
        for row in data:
            if row[1] > 0:
                if len(subsegment) > 10:
                    segments.append(subsegment)
                    subsegment.clear()
                    continue
            else:
                subsegment.append(row)
        return segments


    def write_data(self, food, data, start_time, duration,name = 'Silver', date = '2018-08-20'):
        i = 0
        while i < len(data) and data[i][0] != start_time:
            i += 1
        processed_data = self.preprocess(data[i:])
        with open(name + date +'.csv', 'w') as csvfile:
            fieldnames = ['date', 'time', 'step', 'heartrate', 'food']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for segment in processed_data:
                for row in segment:
                    print(row)
                    writer.writerow({'date': date, 'time': row[0], 'step': row[1], 'heartrate': row[2], 'food': food})
            writer.writerow('\n')

if __name__ == '__main__':
    data_collector = DataCollector()
    data = data_collector.request_data()
    data_collector.write_data(food = 'Kongbao Chicken,Seasame Chicken', data = data, start_time='11:50:00', duration=20)