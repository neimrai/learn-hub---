import requests
import time
import re
import json
from xbot import print


def translate_text(query, to_language="zh"):
    """
    使用百度翻译 API 翻译文本。
    
    参数:
        query (str): 待翻译的文本。
        to_language (str): 翻译目标语言，默认为中文 ("zh")。
    
    返回:
        str: 翻译后的文本。如果出错，返回空字符串。
    """
    # 请求头
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Acs-Token": "1736762596345_1736824772122_QbhbgM2VDjM2+iNrnxAIqdQrKMVO5yRKl8irUixiOYZ9vyc14qnYJYQlw0t1/x27pL4NlhJczqr6gwz62fnLnXgOkAhFt44mu739pgnc/3hNWMzQfjz6GbUhryNask9Hj5pUokUPCWTpmjVAwqTS25Z91I585+LztQKBq8YALEoDoH31d+z6kKZEQF1geXebvvh8Y47XadTeQCTOH1zj8Nbez8+CslJ8we0K8BmoFmrxsQ1KXxteLXuxfOvsrWHhMnV5EFqZvmF0NRrsmOxAL2hDGV6c/qNy4zTSK8cVcaURyrZoEBBXLGEHSG+WvQ4oxgQ7EYBFN0MZT9vLkB/BZXZbcxzDBnnF7aKBmPIu8gWNnNPiqv+rixq5yG4Ac035u1/3PTK4UkNvXlQ/RQWbo8ilGy8uRDXeXZedwhQJaR/WCoIiYpxkZWNbagXTiCRojj2Sgmx9v/n1HflYF2m0NjqrKk2MCvIt+4cwFqP9CEwKJe9CB+Lvf5jywCwV0EB9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://fanyi.baidu.com",
        "Referer": "https://fanyi.baidu.com/mtpe-individual/multimodal",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "text/event-stream",
        "sec-ch-ua": "\\Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\\Windows"
    }

    # 检测语言的 URL
    lang_detect_url = "https://fanyi.baidu.com/langdetect"

    # 检测语言
    lang_detect_data = {"query": query}
    try:
        lang_response = requests.post(lang_detect_url, headers=headers, json=lang_detect_data).json()
        lan = lang_response.get("lan", None)  # 获取检测到的语言
        if not lan:
            print("语言检测失败，返回内容:", lang_response)
            return ""
    except Exception as e:
        print("语言检测出错:", e)
        return ""

    # 翻译的 URL
    translate_url = "https://fanyi.baidu.com/ait/text/translate"

    # 当前时间戳（毫秒级）
    milli_timestamp = str(int(time.time() * 1000))

    # 翻译数据
    translate_data = {
        "query": query,
        "from": lan,
        "to": to_language,
        "reference": "",
        "corpusIds": [],
        "needPhonetic": False,
        "domain": "common",
        "milliTimestamp": int(milli_timestamp)
    }

    try:
        # 发起翻译请求
        translate_response = requests.post(translate_url, headers=headers, json=translate_data).text

        # 从响应中提取翻译结果
        match = re.search(r'"message":"翻译中","list":(.*?)]', translate_response)
        if match:
            rep = match.group(1) + "]"  # 补全 JSON 数组
            rep = json.loads(rep)
            if rep and isinstance(rep, list) and "dst" in rep[0]:
                return rep[0]["dst"]  # 返回翻译后的文本
        print("翻译失败，返回内容:", translate_response)
        return ""
    except Exception as e:
        print("翻译出错:", e)
        return ""


# 测试函数


# query_text = "Selamat pagi! Semoga hari ini membawa kebahagiaan dan kesuksesan untuk Anda."
# translated_zh = translate_text(query_text, to_language="zh")
# print(translated_zh)
# translated_en = translate_text(query_text, to_language="en")
# print(translated_en)

# web_data_table = [
#     [
#         "Von Jayme",
#         "Out of stock",
#         "5"
#     ],
#     [
#         "amacezing13",
#         "Awesome beauty care 🥰",
#         "4"
#     ],]
for row in web_data_table:
  row.append(translate_text(row[1], to_language="zh"))
  row.append(translate_text(row[1], to_language="en"))
print(web_data_table)