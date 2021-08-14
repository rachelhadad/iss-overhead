import requests
from datetime import datetime
import smtplib
import time
import os

username = os.getenv("iss_username")
password = os.getenv("iss_password")

# Your latitude and longitude here
MY_LAT = 133
MY_LNG = 19


def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LNG - 5 <= iss_longitude <= MY_LNG + 5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now <= sunrise and time_now >= sunset:
        return True


while True:

    time.sleep(10)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("server")
        connection.starttls()
        connection.login(username, password)
        connection.sendmail()
    else:
        print("ISS is not overhead.")



