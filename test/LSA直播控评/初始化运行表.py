# ---初始化运行表---
import requests
from xbot import print
import random
from datetime import datetime,timedelta

def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": "cli_a784f55b95b5500b",
        "app_secret": "0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r = requests.post(url, headers=headers, json=data).json()
    return r['app_access_token']


# 读文案表  
def read_txt_fieshu_sheet():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values/{glv['d_sheet']}!A:D" # 设置表格范围
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    return response

# 读运行表
def read_date_fieshu_value():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values/{glv['run_sheet']}!A:I" # 设置表格范围
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    date_str = response[2][4]
    print(date_str)
    if date_str:
      date = datetime.strptime(date_str, '%Y/%m/%d %H:%M')
      today = datetime.today()
      print(today)    
      return date.date() != today.date()
    return True


# 指定位置上传数据
def update_feishu_sheet():
    count = len(read_txt_fieshu_sheet())
    print(count)
    # 生成不重复随机数
    random_numbers = random.sample(range(1, count), count-1)
    random_list = [[num] for num in random_numbers]
    
    state_list = [['否',None] for num in random_numbers]
    
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values"
    data = {"valueRange": {
        "range": f"{glv['run_sheet']}!A{3}:A{count + 1}",     # 设置随机数_表格范围
        "values": random_list
    }}
    data2 = {"valueRange": {
        "range": f"{glv['run_sheet']}!D{3}:E{count + 1}",     # 设置文案运行状态_表格范围
        "values": state_list
    }}
    data3 = {"valueRange": {
        "range": f"{glv['run_sheet']}!I{2}:I{11}",     # 设置评论次数_表格范围
        "values": [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],]
    }}
    # print(data)
    response = requests.put(url, headers=headers, json=data).json()   # 序列初始化
    response2 = requests.put(url, headers=headers, json=data2).json() # 文案运行状态初始化
    response3 = requests.put(url, headers=headers, json=data3).json() # 账号评论次数初始化
    print(response)
    print(response2)
    print(response3)

print('---------------判断是否进入初始化---------------')
z = read_date_fieshu_value()
if z:
  print('执行初始化')
  update_feishu_sheet()
else:
  print('已存在今日日期，不进行初始化')