# bot.py
import os
import requests
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
METEO_TOKEN = os.getenv('METEO_TOKEN')

client = discord.Client(intents=discord.Intents.default())

def pluie():
  response = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={METEO_TOKEN}&q=Paris&days=1&aqi=no&alerts=no")
  json_data = json.loads(response.text)
  #print(json_data)
  pluie = json_data["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]
  chance = json_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
  return (int(pluie), int(chance))

@client.event
async def on_ready():
    print(f"{client.user} s'est connecté, écartez vous s'il vous plaît")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #message = message.lower();
    #if message.content.startswith('$meteo'):
    if "météo" or "meteo" in message.content.lower():
        if pluie()[0]:
            meteo = f"Attention les enfants il risque de pleuvoir avec {pluie()[1]}% de chance demain, n'oubliez pas votre parapluie."

        else:
            meteo = "Il ne devrait pas pleuvoir demain."

        await message.channel.send(meteo)

pluie()
client.run(TOKEN)