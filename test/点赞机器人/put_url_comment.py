# 更新点赞状态

import requests

def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type":"application/json; charset=utf-8"}
    data = {
        "app_id":"cli_a784f55b95b5500b",
        "app_secret":"0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r =requests.post(url,headers=headers,json=data).json()
    return r['app_access_token']

def update_spreadsheets_value(ID):
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values"
    data = {"valueRange": {
        "range": f"bEREQM!E{ID}:E{ID}",
        "values": [
            [1]]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)
update_spreadsheets_value(id_list[loop_item_index]+1)