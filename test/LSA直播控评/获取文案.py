# ----------------------------获取文案----------------------------
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
 
# 分页读取运行表
# 获取未运行文案
def read_run_page_sheet():
    try:
        start_sheet = 1
        end_sheet = 501
        result = []
        id = 3
        while True:
            headers = {
                "Authorization": f"Bearer {app_access_token()}"
            }
            url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/HUuys64XshZf4QtIp0pcCYL0nXc/values/JsylXo!A{start_sheet}:E{end_sheet}"
            params = {
                "valueRenderOption": "ToString",
                "dateTimeRenderOption": "FormattedString"
            }
            response = requests.get(url, headers=headers, params=params, timeout=60).json()["data"]["valueRange"]["values"]
            for res in  response[2:]:
                if res[0]==None :
                    return result
                result.append([id,res[2],res[3],res[4]]) # [70, 'tengah pakai,memang berkesan', '否', None]
                id += 1
                
            start_sheet+=500
            end_sheet+=500
    except Exception as e:
      return read_run_page_sheet()  
running_text = read_run_page_sheet()
NOT_RUNNING = [r for r in running_text if r[2] == '否'] # [70, 'tengah pakai,memang berkesan', '否', None]
