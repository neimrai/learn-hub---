# 获取投放数据 - > 采集状态表更新
import requests
import datetime
# from xbot import print
from datetime import datetime,timedelta
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
    try:
        start_sheet = 1
        end_sheet = 3001
        today_date = (datetime.now() - timedelta(8)).strftime('%Y%m%d')  # 获取当前日期并格式化为字符串
        result = []
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
                if res[0]==None or res[0] < today_date:
                    return True
                History_orderV2.append(str(res[0]))
            start_sheet += 3000
            end_sheet += 3000
    except Exception as e:
      return read_PGCsheets_value()

# 读取采集状态表
def read_existing_data():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/yoVKZi!A:G"
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    
    return response

# 提交数据至采集状态表
def update_spreadsheets_value():
    new_data = read_PGCsheets_value()
    existing_data = read_existing_data()
    row_count = len(existing_data)    # 获取表格当前行数
    existing_records = set((row[0], row[3]) for row in existing_data[1:])  # 提取现有数据中的日期和链接，用于去重
    today_date = datetime.now().strftime('%Y-%m-%d')  # 获取当前日期并格式化为字符串
    
    # 构造数据
    result = []
    # 为每一行数据追加日期，并检查是否重复
    for row in new_data:
        country = row[0]  # 第 E 列
        account = row[2]  # 第 G 列
        link = row[6]  # 第 K 列
        if not link:  # 如果 link 为空，跳过该行
            continue
        # 检查是否已经存在相同的日期和链接
        if (today_date, link) in existing_records:
            print(f"重复数据，跳过: 日期={today_date}, 链接={link}")
            continue
        result.append([today_date, country, account, link, 0])
    # 如果没有需要提交的数据，直接返回
    if not result:
        print("没有需要提交的数据")
        return
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    
    # 构造插入请求
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values"
    data = {
        "valueRange": {
            "range": f"yoVKZi!A{row_count + 1}:E{row_count + len(result)}",  # 在原数据后接入新数据
            "values": result
        }
    }
    print("准备插入的数据:", data)
    response = requests.put(url, headers=headers, json=data).json()
    print("插入结果:", response)
# 执行更新操作
update_spreadsheets_value()