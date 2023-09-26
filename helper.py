import docx
import tiktoken
import re

def num_tokens_from_messages(messages, model="gpt-4-32k-0314"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def read(filename):
# 打開.docx文件
    doc = docx.Document(filename)  # 將"your_document.docx"替換為實際文件的路徑

    # 讀取文件中的文本
    document_text = ""
    time_pattern = r'\d+:\d+:\d+\.\d+ --> \d+:\d+:\d+\.\d+'
    name_pattern = r'[A-Z-]+,[A-Z-]+|[A-Z-]+[A-Z-]+'
    replace_dict = {
    # "蕭百芸": "A",
    # "張瑀珊": "B",
    # "宜萱 林": "C",
    # "林宜萱": "C",
    # "邱詩涵": "D",
    # "林佳儒": "E",
    # "高筱妤": "F",
    # "鍾嘉元": "G",
    # "柯又瑄": "H",
    # "柯虹綺": "I",
    # "黃思穎": "J",
    # "王苡綸": "K",
    # "郭珮娟": "L",
    ',':'','。':'','?':'','!':'',' ':'','，':'','？':''
    # 添加更多要替換的字符串和替換值
    }


    for paragraph in doc.paragraphs:

        match = re.match(time_pattern, paragraph.text)
        matches = re.findall(name_pattern, paragraph.text)


        if match:

            # print(paragraph.text[match.end():].strip())
            # print('--------------------------')
            document_text += paragraph.text[match.end():].strip() + "\n"

        if matches:
            # print("找到的中文名字的羅馬拼音：", matches)

            # 將名字從文本中去除
            for match in matches:
                document_text = document_text.replace(match, '')
            for old_string, new_value in replace_dict.items():
                document_text = document_text.replace(old_string, new_value)
        # print(document_text)
    return document_text    

if __name__ == '__main__':
    doc = read('Transcript_2023-09-211.docx')
    print(doc)
    prompt = f"""你是一個專業的會議記錄機器人，請你幫我詳細總結這場會議的內容，
                需要包含至少三個部分
                第一點是會議的流程，第一點不需要列點寫出來請用通順語句生成
                第二點是會議的內容的重點總結，第二點的每一項事情列點寫出來
                第三點是會議結束後需要處理的事情，第三點的每一項事情列點寫出來
                並且請用繁體中文書寫出             
                """

    msg = [{'role':'system','content':prompt},{'role':'user', 'content':doc}]

    print(num_tokens_from_messages(msg, model="gpt-3.5-turbo-16k-0613"))