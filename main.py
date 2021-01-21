import requests
from datetime import datetime
from smtplib import SMTP
import time

MY_LAT = 88.7121 # Your latitude
MY_LONG = 23.0124 # Your longitude

email = "_YOUR_EMAIL_HERE_"
password = "_YOUR_PASSWORD_HERE"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


def long_lat_checker():
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False

#Your position is within +5 or -5 degrees of the ISS position.


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response1 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data1 = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    current_time = datetime.now().hour

    if current_time >= sunset or current_time <= sunrise:
        return True


is_in_range = long_lat_checker()

def send_mail():
    if is_in_range and is_night():
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email,
                                to_addrs='krittika.saha.dev@gmail.com',
                                msg=f"""Subject:Go to your Window and Look Up ☝!\n\n
The ISS might just be overhead 🛰!""")
    time.sleep(60)
    send_mail()
send_mail()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.


