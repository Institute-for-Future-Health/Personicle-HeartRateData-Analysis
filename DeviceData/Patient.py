import requests
from datetime import datetime
from datetime import timedelta
import os
import errno
import sys

TIME_INDEP_REQUESTS = (
        {
            "title": 'personal information', 
            "url": "https://connect.garmin.com/modern/proxy/userprofile-service/userprofile/personal-information/[USERNAME]"}
        );

TIME_DEP_REQUESTS = (
        {
            "title": 'daily wellness summery',
            "url": "https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailySummaryChart/[USERNAME]",
            "dateParam": "date"
        },{
            "title": 'daily sleep',
            "url": "https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailySleepData/[USERNAME]?nonSleepBufferMinutes=720",
            "dateParam": "date"
        },{
            "title": "daily summary",
            "url": "https://connect.garmin.com/modern/proxy/usersummary-service/usersummary/daily/[USERNAME]",
            "dateParam": "calendarDate"
        },{
             "title": "heart rate",
             "url": "https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailyHeartRate/[USERNAME]",
             "dateParam": "date"
        },{
             "title": "movement",
             "url": "https://connect.garmin.com/modern/proxy/wellness-service/wellness/dailyMovement/[USERNAME]",
             "dateParam": "calendarDate"
        } 
        );
GLOBAL_REQUESTS = [
        {
            "title": 'wellness summary',
            "url": "https://connect.garmin.com/modern/proxy/userstats-service/wellness/daily/[USERNAME]"
        }
        ];

def createFileName(patient, request, date):
    filename = './'+patient+'/'+request+'/'+date.strftime('%Y-%m-%d')+'.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename

class Patient:
    startTime = datetime.now()
    endTime = startTime
    name = "patient1"
    username = ""
    session = ""

    def __init__(self, startTime, endTime, name, username, session):
        self.startTime = startTime
        self.endTime = endTime
        self.name = name
        self.username = username
        self.session = session

    def getTimeDepRequest(self, request):
        timeVar = self.startTime
        while(timeVar <= self.endTime):
            url = request['url'].replace('[USERNAME]', self.username);
            status = 0
            while (status!=200):
                r = requests.get(url, headers={'cookie': self.session}, params={request["dateParam"]: timeVar.strftime('%Y-%m-%d')})
                status = r.status_code
                if(status != 200):
                    print ("error getting ", request['title'], file=sys.stderr)
            f = open(createFileName(self.name, request['title'], timeVar), 'w+')
            f.write(r.text)
            f.close()
            timeVar += timedelta(days=1)

    def getTimeDepRequests(self):
        for req in TIME_DEP_REQUESTS:
            self.getTimeDepRequest(req)

    def getGlobalRequest(self, request):
        url = request['url'].replace('[USERNAME]', self.username);
        status = 0;
        while(status!=200):
            r = requests.get(url, headers={'cookie': self.session}, params={'fromDate': self.startTime.strftime('%Y-%m-%d'), 'untilDate': self.endTime.strftime('%Y-%m-%d')})
            status = r.status_code
            if(status != 200):
                print("error getting ", request['title'], file=sys.stderr)
        
        f = open(createFileName(self.name, request['title'], self.startTime), 'w+')
        f.write(r.text)
        f.close()

    
    def getGlobalRequests(self):
        for req in GLOBAL_REQUESTS:
            self.getGlobalRequest(req)
