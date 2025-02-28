# 上传采集数据
import requests
from xbot import print
import json
import re
import datetime
from datetime import datetime,timedelta

def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type":"application/json; charset=utf-8"}
    data = {
        "app_id":"cli_a784f55b95b5500b",
        "app_secret":"0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r =requests.post(url,headers=headers,json=data).json()
    return r['app_access_token']

# 更新采集信息  
def update_spreadsheets_value(web_data_table):
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values_prepend" 
    
    today_date = datetime.now().strftime('%Y%m%d')  # 获取当前日期并格式化为字符串
    result = []
    # 将每条评论与视频信息结合
    for comment in web_data_table:
      result.append([
      today_date, 
      country_list[loop_item_index],
      account_list[loop_item_index],
      loop_item,
      video_data['publish_time'],
      video_data['playCount'],
      video_data['diggCount'],
      video_data['commentCount'],
      *comment
      ])
    
    data = {"valueRange": {
        "range": f"2NZyyO!A2:K", 
        "values": result
    }}
    print(data)
    response = requests.post(url, headers=headers, json=data).json()
    print(response)
print(skip_outer)
if skip_outer:
  continue
update_spreadsheets_value(web_data_table)


