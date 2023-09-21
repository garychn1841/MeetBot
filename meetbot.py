import openai
import model
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# openai api setting
#openai setting
openai.api_type = os.getenv("api_type")
openai.api_key = os.getenv("api_key")
openai.api_base = os.getenv("api_base")
openai.api_version = os.getenv("api_version")


# GPT setting
CHAT_MODEL_NAME = "gpt-4-32k"


prompt = f"""你是一個專業的會議記錄機器人，請你幫我整理這場會議的內容"""



#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果包含 ping，機器人回傳 pong
    if message.content == 'ping':
        await message.channel.send('pong')
    
    msg = [{'role':'system','content':prompt},{'role':'user', 'content':message.content}]
    response = model.send_message(messages = msg, model_name = CHAT_MODEL_NAME)
    await message.channel.send(response)

client.run(os.getenv("TOKEN")) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面