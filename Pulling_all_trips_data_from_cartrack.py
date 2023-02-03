#! usr/bin/python3
import requests
import json
import datetime
import calendar

#cheking the current date and time for use in function.
today = datetime.datetime.now()
this_month = today.month
this_year = today.year

#Function to pull cartrack data according to month and day.
def pull_cartrack_data(year, month):
    #checking if its the end of the month.
    if today.month == month and today.day == calendar.monthrange(today.year, month)[1]:
        first_day = datetime.datetime(year, month, 1)
        last_day = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 22, 59, 59)
        trips_data = []
        url = (
            "https://fleetapi-za.cartrack.com/rest/trips?start_timestamp=%s&end_timestamp=%s&page=1&limit=20" %(first_day,  last_day))
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Basic TkFOQTAwMDk0OmQxNjg5MjdhMGI5MjMzZjc2OTgyODBjNjgyMmZjNThkNDEyZTFmNDllMzFkN2EyOWE4NjM2ODViMTYzYTg2ZDk= ',
            'Cookie': 'CTSID=ayAjGfC%2CVmO-uVx1f65krWBD7ur4o3v8bdvoSNXRAjy5H3Xp'
        }
        while url:
            response = requests.request("GET", url, headers=headers, data=payload)
            data = json.loads(response.text)
            n = range(data['meta']['last_page'])
            if response.status_code == 200:
                for value in n:
                    #paginating using previous page meta data in the next url.
                    url = (
                            "https://fleetapi-za.cartrack.com/rest/trips?start_timestamp=%s&end_timestamp=%s&page=%f&limit=20" %(first_day, last_day, value))
                    response = requests.request("GET", url, headers=headers, data=payload)
                    updated_data = json.loads(response.text)
                    #replace directry with your own directory if need be.
                    with open("new_car-track_trips_data.json", "a") as trips:
                        json.dump(updated_data, trips)
                    trips_data.extend(updated_data)
                    print("movin' on")
                    print(updated_data)
            else:
                print("failed!!!!!!!!!!", response.status_code)
            break
        print(response.text)
        print("done")
    else:
        #highlighting on my localhost that script didnt run because its not end of month.
        with open("not_the_end_of_month.txt", "a") as doc_file:
            doc_file.write("its not the end of the month!!!!!!!!!")
        print("Today is not the last day of the month.")

#calling the function.
pull_cartrack_data(this_year, this_month)
