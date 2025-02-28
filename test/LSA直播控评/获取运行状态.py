# ----------------------------获取运行状态----------------------------

import requests
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
 
# 读数  
def read_progress_value():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values/JsylXo!I{loop_index+1}:I{loop_index+1}" # 设置表格范围
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    print(response)
    return response[0][0] != 0
print('----------------判断当前进程是否评论----------------')
skip = read_progress_value()
if skip:
  print('已评论，跳过当前')
  continue