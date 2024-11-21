import requests
import os
import smtplib
from datetime import datetime

# https://openweathermap.org/api/one-call-api

# PKiN - Warsaw
lat = '52.231775'
lon = '21.006168'
exclude = 'minutely,hourly,alerts'

url = (
    'https://api.openweathermap.org/data/2.5/forecast?' +
    'lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}&units=imperial'
)

if os.path.isfile('.env'):
    from dotenv import load_dotenv
    load_dotenv()

def __send_email(msg: str) -> None:
    gmail_user = os.getenv('EMAIL_USER')
    gmail_password = os.getenv('EMAIL_PASSWORD')

    # Create Email
    mail_from = gmail_user
    mail_to = gmail_user
    mail_subject = f'Weather Today {datetime.today().strftime("%m/%d/%Y")}'
    mail_message = f'Subject: {mail_subject}\n\n{msg}'

    # Send Email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(mail_from, mail_to, mail_message)
    server.close()

def handler(event, context):

    response = requests.get(url.format(
        lat=lat,
        lon=lon,
        exclude=exclude,
        API_key=os.getenv('WEATHER_API_KEY')
    ))

    data = response.json()
    rain_conditions = ['rain', 'thunderstorm', 'drizzle']
    snow_conditions = ['snow']
    today_weather = data['list'][0]['weather'][0]['main'].lower()

    if today_weather in rain_conditions:
        msg = 'It is rainy in Warsaw today. Pack an umbrella!'
    elif today_weather in snow_conditions:
        msg = 'Winter is coming. Get your skis!'
    else:
        msg = 'Clear skies today! Take a sunglasses with you'

    __send_email(msg)

handler(None, None)