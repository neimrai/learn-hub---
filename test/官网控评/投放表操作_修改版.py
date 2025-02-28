# 获取投放数据 - > 采集状态表更新
import requests
import datetime
from datetime import datetime,timedelta
from xbot import print

ago_current_date = datetime.now().strftime('%Y%m%d')


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

# 读取投放视频链接表数据
def read_PGCsheets_value():
    """
      函数功能：
          该函数用于从飞书表格（Feishu Sheets）中读取投放视频链接表的数据，并根据日期过滤出符合条件的数据。

      注意事项：
          1. 函数会过滤掉日期早于 T-8 天的数据（基于当前日期）。
          2. 如果表格中某一行的第 1 列为空或日期早于 T-8 天，函数会停止读取并返回结果。
          3. 分页读取：每次读取 3000 行，直到没有更多符合条件的数据。
          4. 如果发生异常（如网络错误），函数会自动递归调用自身进行重试。

      """
    try:
        start_sheet = 1
        end_sheet = 3001
        seven_date = (datetime.now() - timedelta(8)).strftime('%Y%m%d')  
        result = []
        id = 2
        while True:
            headers = {
                "Authorization": f"Bearer {app_access_token()}"
            }
            url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/AQGCs9CnThPq4ctjXT2cdUoInHb/values/xMsUCk!A{start_sheet}:K{end_sheet}"
            params = {
                "valueRenderOption": "ToString",
                "dateTimeRenderOption": "FormattedString"
            }
            response = requests.get(url, headers=headers, params=params, timeout=60).json()["data"]["valueRange"]["values"]
            for res in  response[1:]:
                if res[0]==None or str(res[0]) < seven_date:
                    return result
                result.append([ago_current_date,id,res[4],res[6],res[10],0])
                id+=1
            start_sheet+=3000
            end_sheet+=3000
            '''
            1 - 3001
            30001-6001
            '''
    except Exception as e:
      return read_PGCsheets_value()

def update_data_to_feishu_sheets(order_sheets):
    try:
        headers = {
            "Authorization": f"Bearer {app_access_token()}",
            "Content-Type": "application/json"
        }
        url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values_prepend"

        data = {"valueRange": {
            "range": f"geI2fA!A2:E",
            "values": order_sheets
        }}
        response = requests.post(url, headers=headers, json=data, timeout=60).json()

    except Exception as e:
        return update_data_to_feishu_sheets(order_sheets)


def read_feishu_data_fo():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/geI2fA!A1:E2"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }

    response = requests.get(url, headers=headers, params=params, timeout=60).json()["data"]["valueRange"]["values"]
    for res in response[1:]:
        if res == None or str(res[0]) == ago_current_date: # 判断是否已存在当天数据
            return True
    else:
        return False

def main():
    start = read_feishu_data_fo()
    if start==False:
        result = read_PGCsheets_value()
        print(len(result))
        update_data_to_feishu_sheets(result)    
main()
