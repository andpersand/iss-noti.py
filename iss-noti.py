# ISS PASS-OVER NOTIFIER

# basic documentation for API
# is here http://open-notify.org/Open-Notify-API/ISS-Pass-Times/

#to-dos:
# it's automatically giving me the date and time in my computer's time zone.
#    I need to figure out when that's happening and stop it so that I can convert the time into the time zone that matches the given location.
# - figure out how to automatically convert the UTC time to the time zone of
#    the entered location
# - figure out how to accept city names, convert them to lat/long pairs, save
#       those pairs as variables, then plug the vars into parameters
# - figure out how to allow users on twitch and/or discord to call the bot -
#        - format would be !ISSpass (lat), (long)

from datetime import datetime, timedelta
from pytz import timezone
import json, requests, datetime, pytz

#ask user for lat & long input, then store that in var bot_latlong
bot_lat, bot_long = input("Enter a latitude/longitude pair (ex: 40.748452, -73.985595): ").split(", ")

#ask user for the time zone they want the reply to be provided in
#bot_tz = input("Enter the timezone you want to see: ")

#check to make sure input is in proper format (must be integers separated by comma and space)
# if re.match("\d+[, ]+\d+", input()):
#    print("lat/long format")
# ^ above throws error "re is not defined"

#feedback to confirm the entered latlong pair
print("...checking the forecast for coordinates " + bot_lat + ", " + bot_long + "...")


#parameters allows us to feed the API the input it needs to calculate our requested answer.
# lat & long to check: 33.461706, -111.797717
parameters = {"lat": bot_lat, "lon": bot_long}
# Make a get request to get the latest position of the international space station from the opennotify api.
# tell the API to use the parameters you've provided with params=parameters
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# Get the response data as a python object.
data_json = response.json()

#cute ascii art section
starfield = ('''   .  *  .  . *       *    ;        .        .   *    ..
 ` `.    *         .   *       .      :        .            *
 ,  ;  *.   *         #####   .     *      *     +  *  ;  .
  +  _____ ,     *  ######### *    .  +      ,        .  *   .
* . /   / \  .     ###\#|#/###   ..    *    .      *  .  ..  *
 , /___/ _ \        ###\|/###  *    *            .      *   *
   |  | | ||     `     }|{       `        '  `
vvv|__|_|_||vvvvvvvvvvv}|{vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ''')

print(starfield + '\n')

# debug section:
#Check data type to see if it's a dict type
#print(type(data_json))
#print(data_json)

# Print the status code of the response.
#print(response.status_code)

# print the raw response from the API
#print(response.content)

# use a for loop to print the duration and risetime
# datetime.utcfromtimestamp() gives a naive time thing in UTC.
# This means it doesn't have any information on the time zone of the time object.
# the time is originally in UTC - to change timezone, you'll need to use pytz
# what is the unit of duration? >> it's seconds
for x in data_json['response']:
    bot_starttime = datetime.datetime.utcfromtimestamp(x['risetime']).strftime('%Y-%m-%d %H:%M:%S')
    bot_duration = datetime.timedelta(seconds=x['duration'])
    bot_dur_mins = (bot_duration / 60)
    print("The ISS will pass over this place at " + str(bot_starttime) + " UTC" " for " + str(bot_duration) + " mins.")
