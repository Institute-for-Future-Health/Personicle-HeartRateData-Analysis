from Patient import Patient
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

def convertTime(strTime):
    return datetime.strptime(strTime, DATE_FORMAT);
'''
startTime = input("input start time in format 'YYYY-mm-dd': ")
endTime = input("input end time in format 'YYYY-mm-dd': ")
name = input("input patient name: ")
username = input("input patient username: ")
print("input patient's session:")
session = input();
'''
startTime = '2016-10-26'
endTime = '2017-05-23'
name = 'L20'
username = 'Janiinapilvi'
session = 'SESSION=2934114b-0f04-49bd-b84b-6a0e1a72c484; exp_last_visit=1195946285; exp_last_activity=1511306285; exp_tracker=a%3A1%3A%7Bi%3A0%3Bs%3A5%3A%22en-US%22%3B%7D; _gat_ga_universal=1; GARMIN-SSO=1; GarminNoCache=true; GARMIN-SSO-GUID=805B927B8D76079BA261CD5533C4CED4C2582B89; JSESSIONID=A429AB6F350F9DE14481F7EB500DE245; pin.l=528f951603db5d9f33b27644a4b113ea; utag_main=v_id:015fe0dfefbd0009d520bd26820304072002106a00978$_sn:1$_ss:0$_st:1511308108512$ses_id:1511306293182%3Bexp-session$_pn:5%3Bexp-session; __utma=143254506.1234926492.1511306293.1511306293.1511306293.1; __utmb=143254506.3.10.1511306293; __utmc=143254506; __utmz=143254506.1511306293.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1234926492.1511306293; _gid=GA1.2.872691377.1511306295; PrimaryGarminUserLocalePref=fi; G_ENABLED_IDPS=google'

startTime = convertTime(startTime)
endTime = convertTime(endTime)

patient = Patient(startTime, endTime, name, username, session)

patient.getTimeDepRequests();
patient.getGlobalRequests();
