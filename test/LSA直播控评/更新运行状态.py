
# ----------------------------更新运行状态和评论次数----------------------------
import requests
# from xbot import print
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

 # 指定位置上传数据
def update_state_value(ID):
    today = datetime.today().strftime('%Y/%m/%d %H:%M')
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values"
    data = {"valueRange": {
        "range": f"JsylXo!D{ID}:E{ID}",     # 设置文案状态_表格范围
        "values": [['是',today]]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)
    
 # 指定位置上传数据
def update_progress_value(ID):
    today = datetime.today().strftime('%Y/%m/%d %H:%M')
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    # 获取当前评论次数
    url1 = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values/JsylXo!I{ID}:I{ID}"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response1 = requests.get(url1, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    print(response1)
    
    # 评论次数+1
    url2 = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values"
    data = {"valueRange": {
        "range": f"JsylXo!I{ID}:I{ID}",     # 设置评论次数_表格范围
        "values": [[response1[0][0] + 1]]
    }}
    print(data)
    response2 = requests.put(url2, headers=headers, json=data).json()
    print(response2)    

update_state_value(NOT_RUNNING[loop_index2][0])
update_progress_value(loop_index + 1)