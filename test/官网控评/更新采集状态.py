# 更新采集状态

import requests
from xbot import print

# 获取飞书 App Access Token
def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": "cli_a784f55b95b5500b",
        "app_secret": "0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r = requests.post(url, headers=headers, json=data).json()
    return r['app_access_token']

# 更新已采集视频的采集状态（state = 1）
def update_spreadsheets_value():
    headers = {
          "Authorization": f"Bearer {app_access_token()}",
          "Content-Type": "application/json"
      }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values" 
    # 获取链接的位置索引
    # for i, row in enumerate(data):  # 遍历数据
    #     if row[3] == loop_item and row[0] == today_date:  # 检查链接是否匹配
    #         link_indices = i  # 记录索引
    data = {"valueRange": {
        "range": f"geI2fA!F{[row[4] for row in res ][loop_item_index] }:F{[row[4] for row in res ][loop_item_index] }", 
        "values": [[1]]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)
update_spreadsheets_value()


