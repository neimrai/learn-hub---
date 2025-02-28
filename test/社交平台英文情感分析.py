from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


# 初始化情感分析器
analyzer = SentimentIntensityAnalyzer()

# 定义句子列表
web_data_table = [
    "VADER is smart, handsome, and funny.",
    "VADER is smart, handsome, and funny!",
    "VADER is very smart, handsome, and funny.",
    "VADER is VERY SMART, handsome, and FUNNY.",
    "VADER is VERY SMART, handsome, and FUNNY!!!",
    "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",
    "VADER is not smart, handsome, nor funny.",
    "The book was good.",
    "At least it isn't a horrible book.",
    "The book was only kind of good.",
    "The plot was good, but the characters are uncompelling and the dialog is not great.",
    "Today SUX!",
    "Today only kinda sux! But I'll get by, lol",
    "Make sure you :) or :D today!",
    "Catch utf-8 emoji such as such as ? and ? and ?",
    "Not bad at all"
]

# 定义情感分析函数
def senti(text):
    return analyzer.polarity_scores(text)['compound']

print([senti(sentence) for sentence in web_data_table])
# 创建 DataFrame
df = pd.DataFrame(web_data_table, columns=['text'])

# 计算情感得分
df['sentiment'] = df['text'].apply(senti)

# 定义情感分类函数
def classify_sentiment(score):
    if score > 0.05:
        return '正面'
    elif score < -0.05:
        return '负面'
    else:
        return '中性'

# 应用情感分类
df['sentiment_category'] = df['sentiment'].apply(classify_sentiment)

# 输出结果
print(df)
print(senti())