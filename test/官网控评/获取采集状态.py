# 获取当日的采集状态

import requests
import datetime
from datetime import datetime,timedelta
from xbot import print


def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": "cli_a784f55b95b5500b",
        "app_secret": "0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r = requests.post(url, headers=headers, json=data).json()
    return r['app_access_token']
# 读取采集状态表
def read_existing_data():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/geI2fA!A:F"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    # print(response)
    return response
  
today_date = datetime.now().strftime('%Y%m%d')  # 获取当前日期并格式化为字符串
data = read_existing_data()
url_list = []
country_list = []
account_list = []
id_list = []
print(data)
for row in data[1:]: 
  if row[0] == today_date and row[5] == 0:  # 当天日期 & 评论状态为0的数据
    url_list.append(row[4])
    country_list.append(row[2])
    account_list.append(row[3])
    id_list.append(row[1])

skip_outer = False  # 设置跳出循环标志变量
  




