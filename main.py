from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, date
import requests
import calendar
from telethon import TelegramClient, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

client = TelegramClient("timeavatar", "3135518", "465ed9250d34ff6666a60948fada90ed")
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
    
    im = Image.new(mode="RGB", size=(530, 490), color=(0, 59, 70))
    draw_text = ImageDraw.Draw(im)
    font = ImageFont.truetype('fonts/font.otf', size=120)
    font2 = ImageFont.truetype('fonts/font.otf', size=40)
    font3 = ImageFont.truetype('fonts/font.otf', size=100)
    font4 = ImageFont.truetype('fonts/font.otf', size=40)
    color1 = '#c3dfe6'
    color = color1
    draw = ImageDraw.Draw(im) 
    draw.line((50,245,480,245), fill = color1, width=8)

    text = hour+':'+minutes
    (width, height) = font.getsize(text)
    draw_text.text(
        ((im.width - width) / 2, height+150),
        text,
        font=font,
        fill=color)

    text = 'USD: '+str(usd)+'    EUR: '+str(eur)
    (width, height) = font2.getsize(text)
    draw_text.text(
        ((im.width - width) / 2, height+160),
        text,
        font=font2,
        fill=color)

    text = today
    (width, height) = font3.getsize(text)
    draw_text.text(
        ((im.width - width) / 2, height+15),
        text,
        font=font3,
        fill=color)

    text = datenow
    (width, height) = font4.getsize(text)
    draw_text.text(
        ((im.width - width) / 2, height+330),
        text,
        font=font4,
        fill=color)  
        
    im.save('tmp/avatar.png')



current_datetime = datetime.now()
timetowork = current_datetime.minute
while True:
    current_datetime = datetime.now()
    timetowork2 = current_datetime.minute
    if timetowork!=timetowork2:
        timetowork = timetowork2
        draw()
        client(DeletePhotosRequest(client.get_profile_photos('me')))
        file = client.upload_file(f"tmp/avatar.png")
        client(UploadProfilePhotoRequest(file))
        