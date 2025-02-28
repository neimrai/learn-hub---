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
 
# 读数  
def read_fieshu_sheet():
    headers = {
        "Authorization": f"Bearer {app_access_token()}"
    }
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values/ydF2vU!A:J" # 设置表格范围
    params = {
        "valueRenderOption": "ToString",
        "dateTimeRenderOption": "FormattedString"
    }
    response = requests.get(url, headers=headers, params=params).json()["data"]["valueRange"]["values"]
    return response
 
# 读取分页读表
def read_PGCsheets_value():
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

# 指定位置上传数据
def update_feishu_sheet(ID):
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values"
    data = {"valueRange": {
        "range": f"qBx5Rd!A{ID}:B{ID}",     # 设置表格范围
        "values": [['ปอนด์กระเบื้องแตก', 'แปลกใหม่มาก🥰', 1, '很有异国情调。🥰', 'Very exotic. 🥰', '正面']]
    }}
    print(data)
    response = requests.put(url, headers=headers, json=data).json()
    print(response)

# 向前插入数据
def update_spreadsheets_valueprepend(result):
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/VduWslSuehmnBrtUOsFcKN3lnWg/values_prepend"  # values_prepend
    data = {"valueRange": {
      "range": f"qBx5Rd!A2:B",      # 设置表格范围
      "values": result
    }}
    print(data)
    response = requests.post(url, headers=headers, json=data).json()  # post命令
    print(response)

# 向上插入数据到飞书表,带重试机制
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
  
update_spreadsheets_valueprepend([['ปอนด์กระเบื้องแตก', 'แปลกใหม่มาก🥰', 1, '很有异国情调。🥰', 'Very exotic. 🥰', '正面']])