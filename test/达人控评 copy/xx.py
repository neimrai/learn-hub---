# 达人视频链接获取
import requests
from datetime import datetime,timedelta
from xbot import print

headers = {

    "authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6Ijg5YTg1OTAyLWM1YTItNDIzYS04ZGQ2LWYxOTdiNzUzMjFhMSJ9.dY1qIK7UepI9DHjOOQVbIKqoEraxAZSUOQ19otrz2r9oF3_KMy_9s_ClBLsw05hNs4qMoH1FQyQwCkAX2aHPzg",
}
url = "http://47.107.59.221:10030/prod-api/biz/releaseBoard/list"

current_date = datetime.now()
new_date = current_date - timedelta(days=7)
TimeStart = new_date.strftime('%Y-%m-%d')
TimeEnd = current_date.strftime('%Y-%m-%d')
pageNum = 1
while True:
    params = {
        "pageNum": pageNum,
        "pageSize": "500",
        "queryType": "1",
        "conversionType": "1",
        "gmvType": "1",
        "impressionsType": "1",
        "roiType": "1",
        "playCountType": "1",
        "diggCountType": "1",
        "commentCountType": "1",
        "kolRemarkType": "1",
        "attribution": "KOL团队,KOC团队,KOC-VN,KOL-VN",
        "addLinkTimeStart": f"{TimeStart} 00:00:00",
        "addLinkTimeEnd": f"{TimeEnd} 23:59:59"
    }
    response = requests.get(url, headers=headers, params=params, verify=False).json()
    rows = response['rows']
    total = response["total"]

    if pageNum * 500 > total:
        break
    pageNum += 1

video_state = []
today_date = datetime.now().strftime('%Y%m%d')  # 获取当前日期并格式化为字符串
id = 2
for item in rows:
        rmb_price_value = item.get("rmbPrice", 0)
        try:
            rmb_price = float(rmb_price_value)
        except (ValueError, TypeError):
            rmb_price = rmb_price_value
        # 将字典的值转换为列表
        state = [
            today_date,
            id ,
            item.get("country"),        # 国家
            item.get("product"),        # 产品名称
            item.get("contentLink"),    # 视频链接
            item.get("kolId"),          # KOL ID
            item.get("gmv"),            # 视频GMV
            rmb_price,                  # 素材费用
            0,  
        ]
        video_state.append(state)  # 将列表添加到 video_state
        id += 1
print(len(rows))     
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

# 向上插入数据到飞书表
def update_data_to_feishu_sheets(order_sheets, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            headers = {
                "Authorization": f"Bearer {app_access_token()}",
                "Content-Type": "application/json"
            }
            url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values_prepend"
            data = {"valueRange": {
                "range": f"lXk5BV!A2:E",
                "values": order_sheets
            }}
            response = requests.post(url, headers=headers, json=data, timeout=60).json()
            print(response)
            return response
        except Exception as e:
            retries += 1
            print(f"重试中 ({retries}/{max_retries})...")
    raise Exception("更新飞书表格失败，已重试多次")

# 判断是否已存在当天数据
def read_feishu_data_fo():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/lXk5BV!A1:E2"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }

    response = requests.get(url, headers=headers, params=params, timeout=60).json()["data"]["valueRange"]["values"]
    for res in response[1:]:
        if res == None or str(res[0]) == today_date: 
            return True
    else:
        return False

def main():
    start = read_feishu_data_fo()
    if start==False: 
        update_data_to_feishu_sheets(video_state) 
# main()
      
