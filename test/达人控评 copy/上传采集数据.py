# 上传采集数据
# 更新采集状态1&3
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
        overdata = [
          today_date, 
          country_list[loop_item_index],
          account_list[loop_item_index],
          loop_item,
          KOLID,  
          GMV,
          RMB,
          publish_time,
          playCount,
          diggCount,
          commentCount,
          *comment
        ]
        result.append(overdata)
    
    data = {"valueRange": {
        "range": f"oKsQUy!A2:M", 
        "values": result
    }}
    print(data)
    response = requests.post(url, headers=headers, json=data).json()
    print(response)

# 更新已采集视频的采集状态（state = 1）
def update_spreadsheets_state1():
    headers = {
          "Authorization": f"Bearer {app_access_token()}",
          "Content-Type": "application/json"
      }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values" 

    data = {"valueRange": {
        "range": f"lXk5BV!F{id_list[loop_item_index]}:F{id_list[loop_item_index] }", 
        "values": [[1]]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)
    
# 更新已采集视频的采集状态,未达到条件的视频（state = 3）
def update_spreadsheets_state3():
    headers = {
          "Authorization": f"Bearer {app_access_token()}",
          "Content-Type": "application/json"
      }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values" 

    data = {"valueRange": {
        "range": f"lXk5BV!F{id_list[loop_item_index]}:F{id_list[loop_item_index] }", 
        "values": [[3]]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)

if skip_outer:
  continue  # 跳过外部循环的当前迭代

if playCount is None:
  update_spreadsheets_state3() # 视频年龄限制
  continue

if playCount >= 100000 or GMV >= 500 or RMB >= 500:
  update_spreadsheets_value(web_data_table)
  update_spreadsheets_state1()
else:
  update_spreadsheets_state3()




        


