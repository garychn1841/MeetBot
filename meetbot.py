import openai
import model
import helper
import requests
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
CHAT_MODEL_NAME = "gpt-35-turbo-16k"
# CHAT_MODEL_NAME = "gpt-4-32k"


name_mapping = {"蕭百芸": "A",
                "張瑀珊": "B",
                "宜萱 林": "C",
                "林宜萱": "C",
                "邱詩涵": "D",
                "林佳儒": "E",
                "高筱妤": "F",
                "鍾嘉元": "G",
                "柯又瑄": "H",
                "柯虹綺": "I",
                "黃思穎": "J",
                "王苡綸": "K",
                "郭珮娟": "L"}


# 如你看到 A 就使用蕭百芸、你看到 B 就使用張瑀珊、你看到 C 就使用林宜萱
# 會議中的名字都被去識別化了，請幫參考人名對照表<{name_mapping}>中字典的格式幫我將所有生成出來的姓名用本名表示
prompt = f"""你是一個專業的會議記錄機器人，請你幫我詳細總結這場會議的內容，
             需要包含至少三個部分，
             第一點是會議的流程，第一點不需要列點寫出來請用通順語句生成，
             第二點是會議的內容的重點總結，第二點的每一項事情列點寫出來，
             第三點是會議結束後需要處理的事情，第三點幫將人名用markdown語法改成黃色時間用markdown語法改成紅色，
             並且請用繁體中文和markdown語法生成       
            """



#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
meetbot_channel_id = 1154417738643689562
my_channel_id = 1154293514667036723

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

    if message.attachments and (message.channel.id == meetbot_channel_id or message.channel.id == my_channel_id):
        for attachment in message.attachments:
            response = requests.get(attachment.url)
            if response.status_code == 200:
                # 將附件保存到本地
                with open(attachment.filename, 'wb') as file:
                    file.write(response.content)
                content = helper.read(attachment.filename)
        msg = [{'role':'system','content':prompt},{'role':'user', 'content':content}]
        response = model.send_message(messages = msg, model_name = CHAT_MODEL_NAME)
        msg.append({'role':'assistant', 'content':response})
        await message.channel.send(response)
        await message.channel.send("Token使用量%d"%helper.num_tokens_from_messages(msg))

    if message.content and (message.channel.id == meetbot_channel_id or message.channel.id == my_channel_id):
        msg = [{'role':'system','content':prompt},{'role':'user', 'content':message.content}]
        response = model.send_message(messages = msg, model_name = CHAT_MODEL_NAME)
        msg.append({'role':'assistant', 'content':response})
        await message.channel.send(response)
        await message.channel.send("Token使用量%d"%helper.num_tokens_from_messages(msg))


client.run(os.getenv("TOKEN"))