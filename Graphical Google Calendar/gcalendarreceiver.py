#Connects to Google Calendar to retrieve a list of events which it outputs into JSON organized by date.
import httplib2
import json
import logging
import gflags
import dateutil.parser

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from urllib import quote

FLAGS = gflags.FLAGS
logging.basicConfig(filename='error.log',level=logging.DEBUG)
# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='691398644037.apps.googleusercontent.com',
    client_secret='pNgZgAD26RTajalZya63Fb5R',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Refrigerator Calendar Prototype/v3')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='AIzaSyCFXE8IAxfDjJd5vzz0RVJfYHy5UOdfT6U')
resp, calList = http.request("https://www.googleapis.com/calendar/v3/users/me/calendarList", "GET")
listJson = json.loads(calList)
outputdata = {}
for item in listJson["items"]:
    resp, eventList = http.request("https://www.googleapis.com/calendar/v3/calendars/" + quote(item["id"]) + "/events", "GET")
    eventJson = json.loads(eventList)
    print eventList
    for event in eventJson["items"]:
      if "date" in event["start"]:
        start = dateutil.parser.parse(event["start"]["date"])
      else:
        start = dateutil.parser.parse(event["start"]["dateTime"])
      day = str(start.month) + " " + str(start.day) + " " + str(start.year)
      if not day in outputdata:
        outputdata[day] = []
        outputdata[day].append(
        {"title":event["summary"],
          "location":(event["location"] if "location" in event else ""),
          "starttime":str(start.hour)+":"+str(start.minute)+":"+str(start.second)})
      else:
        outputdata[day].append(
        {"title":event["summary"],
          "location":(event["location"] if "location" in event else ""),
          "starttime":str(start.hour)+":"+str(start.minute)+":"+str(start.second)})
outputjson = json.dumps(outputdata)
outputfile = open("calendaroutput.json", "w")
outputfile.write(outputjson)
outputfile.close()
print "New JSON file written!"
