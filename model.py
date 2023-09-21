import openai
import os
from dotenv import load_dotenv
load_dotenv()


#openai setting
openai.api_type = os.getenv("api_type")
openai.api_key = os.getenv("api_key")
openai.api_base = os.getenv("api_base")
openai.api_version = os.getenv("api_version")


def send_message(messages, model_name, max_response_tokens=1000):
    
    response = openai.ChatCompletion.create(
        engine=model_name,
        messages=messages,
        temperature=0,
        max_tokens=max_response_tokens,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0,
    )    
    return response['choices'][0]['message']['content']
