from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, date
import requests
import calendar
from telethon import TelegramClient, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from random import randint as rn
from time import sleep

client = TelegramClient("timeavatar", "api_id", "api_hash")
client.start()

def draw():

    current_datetime = datetime.now()    
    my_date = date.today()
    today = calendar.day_name[my_date.weekday()]
    datenow = current_datetime.strftime("%d.%m.%Y")
    hour = str(current_datetime.hour)    
    minutes = str(current_datetime.minute)
    if len(minutes)==1:
        minutes = '0'+minutes

    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    usd = (str(data['Valute']['USD']['Value'])[:str(data['Valute']['USD']['Value']).find(':')+6])
    eur = (str(data['Valute']['EUR']['Value'])[:str(data['Valute']['EUR']['Value']).find(':')+6])  
    
    im = Image.new(mode="RGB", size=(530, 490), color=(rn(0,110), rn(0,110), rn(0,110)))
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('fonts/font.otf', size=120)
    font2 = ImageFont.truetype('fonts/font.otf', size=40)
    font3 = ImageFont.truetype('fonts/font.otf', size=80)
    font4 = ImageFont.truetype('fonts/font.otf', size=40)
    color = '#c3dfe6'
    draw = ImageDraw.Draw(im) 
    draw.line((50,245,480,245), fill = color, width=8)

    text = hour+':'+minutes
    (width, height) = font.getbbox(text)[2:]
    draw_text.text(
        ((im.width - width) / 2, height+150),
        text,
        font=font,
        fill=color)

    text = 'USD: '+str(usd)+'    EUR: '+str(eur)
    (width, height) = font2.getbbox(text)[2:]
    draw_text.text(
        ((im.width - width) / 2, height+160),
        text,
        font=font2,
        fill=color)

    text = today
    (width, height) = font3.getbbox(text)[2:]
    draw_text.text(
        ((im.width - width) / 2, height+50),
        text,
        font=font3,
        fill=color)

    text = datenow
    (width, height) = font4.getbbox(text)[2:]
    draw_text.text(
        ((im.width - width) / 2, height+330),
        text,
        font=font4,
        fill=color)  
    
    im.save('/tmp/avatar.png')


current_datetime = datetime.now()
timetowork = current_datetime.minute
while True:
    current_datetime = datetime.now()
    timetowork2 = current_datetime.minute
    if timetowork!=timetowork2:
        timetowork = timetowork2
        draw()
        client(DeletePhotosRequest(client.get_profile_photos('me')))
        file = client.upload_file(f"/tmp/avatar.png")
        client(UploadProfilePhotoRequest(file))
        sleep(59)
        