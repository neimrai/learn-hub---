# 获取点赞状态


import requests

# from xbot import print


def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": "cli_a784f55b95b5500b",
        "app_secret": "0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r = requests.post(url, headers=headers, json=data).json()
    return r['app_access_token']
# 读取评论
def read_existing_data():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/ydF2vU!A:J"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    # print(response)
    return response
comment_list = []
url_list = []
id_list = []
state_list = []
data = read_existing_data()

for row in data[1:]: 
  if row[4] == 0:  # 评论状态为0的数据
    id_list.append(row[0])
    url_list.append(row[2])
    comment_list.append(row[3])
    state_list.append(row[4])


