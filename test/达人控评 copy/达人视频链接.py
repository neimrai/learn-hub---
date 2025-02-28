# 达人视频链接获取
import requests
from datetime import datetime,timedelta
# from xbot import print



url = "http://47.107.59.221:10030/prod-api/biz/releaseBoard/list"

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImM2ODRjMjdjLWI1NWItNDg0NS05ZmJkLTFkYmFkZjQ0OWJmMSJ9.l-zGf2nyPzXMFpt1mR8t1jxQze-Fk3f-WijkzWCfhmqgMJMyjv2cSbqbODVt22SlVnmYzsxU9fMBrwtzQmt53w",
}
# url = "http://prod.kol.jiguang168.com/prod-api/biz/releaseBoard/list"

# headers = {
  
#     "authorization":"Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjUwNDIxYTdlLTY1YmEtNDVmMS1hOGQ4LTNhYzNiMTc5YTk0NiJ9.J4dcN6gYuMDoHcQXe9rHUpDxg7tVKF36MhmQ0MTHP34i6O01ymeSV_keYj5sdf51Lz-8CsG1I-6JHiCF3MkDwQ"

# }

current_date = datetime.now()
new_date = current_date - timedelta(days=7)
TimeStart = new_date.strftime('%Y-%m-%d')
TimeEnd = current_date.strftime('%Y-%m-%d')
print(TimeStart,TimeEnd)
video_info = []
today_date = datetime.now().strftime('%Y%m%d')  # 获取当前日期并格式化为字符串
id = 2
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
    for item in rows:
        rmb_price_value = item.get("rmbPrice", 0)
        gmv_value = item.get("gmv", 0)
        try:
            rmb_price = float(rmb_price_value)
        except (ValueError, TypeError):
            rmb_price = 0.0
        try:
            gmv_value = float(item.get("gmv", 0))
        except (ValueError, TypeError):
            gmv_value = 0.0
        info = [
            today_date,
            id ,
            item.get("country"),        # 国家
            item.get("product"),        # 产品名称
            item.get("contentLink"),    # 视频链接
            0,  
            item.get("kolId"),
            gmv_value,
            rmb_price,
        ]
        video_info.append(info)  # 将列表添加到 video_info
        id += 1
    total = response["total"]
    if pageNum * 500 > total:
        break
    pageNum += 1
print(len(video_info))        
video_state = [row[:6] for row in video_info]

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
    print(len(video_state))
    if start==False: 
        print(len(video_state))
        update_data_to_feishu_sheets(video_state) 
main()
      
