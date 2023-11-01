# bot.py
import os
import requests
import json
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
METEO_TOKEN = os.getenv('METEO_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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

    elif "monsieur" in message.content.lower():
        await message.channel.send('Bonjour !')

    elif "hello" in message.content.lower() or "bonjour" in message.content.lower():
        await message.channel.send('Hello !')

    elif "meteo" in message.content.lower() or "météo"  in message.content.lower():
        il_va_pleuvoir, chance_pluie = pluie()
        channel = message.channel
        if il_va_pleuvoir:
            meteo = f"Attention les enfants il risque de pleuvoir avec {chance_pluie}% de chance demain, n'oubliez pas votre parapluie."

        else:
            meteo = "Il ne devrait pas pleuvoir demain."

        await channel.send(meteo)

client.run(TOKEN)