import requests
# from xbot import print
from requests_toolbelt import MultipartEncoder

def app_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": "cli_a784f55b95b5500b",
        "app_secret": "0SlPvjJg2Dsx9TuxR9MF7UVcB6Jhnkgl"
    }
    r = requests.post(url, headers=headers, json=data).json()
    return r['app_access_token']
 
# 向前插入数据
def update_spreadsheets_valueprepend(result):
    headers = {
        "Authorization": f"Bearer {app_access_token()}",
        "Content-Type": "application/json"
    }
    url = "https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/YNJgsitpIhqUvJtJHC4cmGhQnre/values_prepend"  # values_prepend
    data = {"valueRange": {
      "range": f"3e5c81!A2:B",      # 设置表格范围
      "values": result
    }}
    print(data)
    response = requests.post(url, headers=headers, json=data).json()  # post命令
    print(response)
    
    
import requests
# 输入pip install requests_toolbelt 安装依赖库

def uploadImage():
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open('path/testimage.png', 'rb'))}  # 需要替换具体的path 
    multi_form = MultipartEncoder(form)
    headers = {
        'Authorization': 'Bearer t-xxx',  ## 获取tenant_access_token, 需要替换为实际的token
    }
    headers['Content-Type'] = multi_form.content_type
    response = requests.request("POST", url, headers=headers, data=multi_form)
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response

if __name__ == '__main__':
    uploadImage()