from telethon import TelegramClient, events
from config import api_id, api_hash
import mysql.connector, urllib.request
client = TelegramClient('session', api_id, api_hash)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123ManugaD",
  database="capitalstreet"
)

mycursor = mydb.cursor()


@client.on(events.NewMessage(chats="@testmaneth2"))
async def my_event_handler(event):
    if "TRADE SIGNAL AS ON" in event.text:
        lines = event.text.splitlines()
        sigs = {}
        for i in lines:
            if "TRADE SIGNAL AS ON" in i:
                x = i.split()
                date = x[-1]
            if "#" in i:
                x = i.replace('#', '')
                sigs["currency"] = x
            if "SELL=" in i or "BUY=" in i:
                y = "".join(z for z in i if z in "0123456789.")
                x = "".join(z for z in i if z in "BUYSEL")
                sigs["BS"] = y
                sigs["BS_type"] = x
            if "TARGET=" in i:
                sigs["TP"] = "".join(z for z in i if z in "0123456789.")
            if "SL=" in i:
                sigs["SL"] = "".join(z for z in i if z in "0123456789.")
                
            if len(sigs) == 5:
                sql = f"INSERT INTO trades (currency, BS, TP, SL, BS_type, Dates) VALUES ('{sigs['currency']}', '{sigs['BS']}', '{sigs['TP']}', '{sigs['SL']}', '{sigs['BS_type']}', '{date}')"
                mycursor.execute(sql)
                mydb.commit()
                msg = f"{sigs['BS_type']} {sigs['currency']} {sigs['BS']} SL {sigs['SL']} TP {sigs['TP']}"
                msg = msg.replace('&', '%26')
                urllib.request.urlopen(f"https://api.telegram.org/bot1447605485:AAHdSqT49TKsuRg6Jg9lRToeKDqH9BFEjUQ/sendMessage?chat_id=804493713&text={msg.replace(' ', '+')}")
                sigs = {}
                print(mycursor.rowcount, "record inserted.")
client.start()
client.run_until_disconnected()