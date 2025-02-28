# 翻译评论
import requests
import time
import re
import json
from xbot import print
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def translate_text(query, to_language="zh", max_retries=3):
    """
    使用百度翻译 API 翻译文本，添加重试机制。
    
    参数:
        query (str): 待翻译的文本。
        to_language (str): 翻译目标语言，默认为中文 ("zh")。
        max_retries (int): 最大重试次数，默认为 3。
    
    返回:
        str: 翻译后的文本。如果出错或失败，返回 "翻译失败"。
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

    # 翻译的 URL
    translate_url = "https://fanyi.baidu.com/ait/text/translate"

    # 当前时间戳（毫秒级）
    milli_timestamp = str(int(time.time() * 1000))

    # 重试机制
    for attempt in range(max_retries):
        try:
            # 检测语言
            if not query:
              return ''
            lang_detect_data = {"query": query}
            lang_response = requests.post(lang_detect_url, headers=headers, json=lang_detect_data).json()
            lan = lang_response.get("lan", None)  # 获取检测到的语言
            if not lan:
                print(f"语言检测失败，返回内容: {lang_response}")
                continue  # 重试

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

            # 发起翻译请求
            translate_response = requests.post(translate_url, headers=headers, json=translate_data).text

            # 从响应中提取翻译结果
            match = re.search(r'"message":"翻译中","list":(.*?)]', translate_response)
            if match:
                rep = match.group(1) + "]"  # 补全 JSON 数组
                rep = json.loads(rep)
                if rep and isinstance(rep, list) and "dst" in rep[0]:
                    return rep[0]["dst"]  # 返回翻译后的文本

            print(f"第 {attempt + 1} 次翻译失败，返回内容: {translate_response}")
        except Exception as e:
            print(f"第 {attempt + 1} 次翻译出错: {e}")

        # 等待一段时间再重试
        time.sleep(1)

    # 如果所有尝试均失败，返回翻译失败的文本
    return "翻译失败"

# 定义情感分类函数
def classify_sentiment(score):
    if score > 0.05:
        return '正面'
    elif score < -0.05:
        return '负面'
    else:
        return '中性'
      
# 定义情感分析函数
def senti(text):
    return analyzer.polarity_scores(text)['compound']
  
  
# web_data_table =[['ปอนด์กระเบื้องแตก', 'แปลกใหม่มาก🥰', 1]]

def is_question(text):
  a = re.search(r'\b(what|who|where|why|how)\b', text, re.IGNORECASE) is not None or '?' in text
  if a:
    return '是'
  return '否'

def convert_to_int(like_str):
    if like_str[-1].lower() == 'k':  # 如果以 'K' 结尾
        return int(float(like_str[:-1]) * 1000)
    elif like_str[-1].lower() == 'm':  # 如果以 'M' 结尾
        return int(float(like_str[:-1]) * 1000000)
    else:  # 普通数字
        return int(like_str)
# 初始化情感分析器
analyzer = SentimentIntensityAnalyzer()  


# web_data_table = [['ปอนด์กระเบื้องแตก', 'แปลกใหม่มาก🥰', 1]]
for row in web_data_table:
    row[2] = convert_to_int(row[2])
    row.append(translate_text(row[1], to_language="zh"))  # 翻译为中文
    
    translated_en = translate_text(row[1], to_language="en")  # 翻译为英文
    row.append(translated_en)
    if translated_en:
      # 对翻译后的英文文本进行情感分析和分类
      sentiment_score_en = senti(translated_en)
      sentiment_category_en = classify_sentiment(sentiment_score_en)
      row.append(sentiment_category_en)  # 添加英文情感分类结果
      
      # 对翻译后的英文文本进行提问判断
      q = is_question(translated_en)
      row.append(q)  


print(web_data_table)
