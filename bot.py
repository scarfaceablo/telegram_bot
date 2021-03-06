import pandas as pd
import time
import requests

import yaml

with open("bot_config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


bot_token = config["telegram"]["bot_token"]
bot_chatID = config["telegram"]["bot_chat_id"]

worldcoin_key = config["api_keys"]["worldcoin_key"]
weather_api_key = config["api_keys"]["weather_api_key"]


def telegram_bot_sendtext(bot_message):

    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


worldcoinindex = requests.get(
    "https://www.worldcoinindex.com/apiservice/v2getmarkets?key={}&fiat=usd".format(worldcoin_key))

markets = worldcoinindex.json()["Markets"][0]

df_coins = pd.DataFrame(markets)

df_coins["datetime"] = pd.to_datetime(df_coins["Timestamp"], unit="s")

df_coins = df_coins.set_index("datetime")

df_coins = df_coins.tz_localize('UTC')
df_coins = df_coins.tz_convert('Europe/Vienna')
df_coins = df_coins.sort_index(ascending=False)

df_coins_to_sent = df_coins.loc[(df_coins["Label"] == ("XRP/USD"))
                                | (df_coins["Label"] == ("BTC/USD"))
                                | (df_coins["Label"] == ("ETH/USD"))
                                | (df_coins["Label"] == ("EOS/USD"))
                                | (df_coins["Label"] == ("LTC/USD"))
                                | (df_coins["Label"] == ("BCH/USD"))]


df_coins_to_sent = df_coins_to_sent.sort_values(by="Label", ascending=False)

message = ""
for i, row in df_coins_to_sent.iterrows():
    #print(i,row["Label"], row["Price"])
    message = message+str(i)+"\n"+row["Label"]+"\n" + \
        str(row["Price"])+"\n"+"----------------"+"\n"

res = telegram_bot_sendtext(message)


weather = requests.get(
    "http://api.openweathermap.org/data/2.5/forecast/hourly?q=Ljubljana,si&mode=json&APPID="+weather_api_key)

df_weather = pd.DataFrame(weather.json()["list"])

df_weather["weather"] = df_weather["weather"].apply(
    lambda x: x[0]["description"])

df_weather["datetime"] = pd.to_datetime(df_weather["dt_txt"])

df_weather["hour"] = df_weather["datetime"].dt.hour
df_weather["day"] = df_weather["datetime"].dt.day
df_weather["month"] = df_weather["datetime"].dt.month

df_weather = df_weather.tail(72)

weather_msg = ""
for i, row in df_weather.iterrows():
    weather_msg += str(row["month"])+"-"+str(row["day"]) + \
        "-"+str(row["hour"]) + " => "+row["weather"]+"\n"

res = telegram_bot_sendtext(weather_msg)
