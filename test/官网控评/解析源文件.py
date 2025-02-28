# 解析源文件
import json
import re
from datetime import datetime
from xbot import print
 

def read_video_data(web_page_attribute):
    """
      解析网页中的 JSON 数据并返回视频统计信息。
      
      参数：
          web_page_attribute (str): 网页内容
          retry_count (int): 剩余重试次数

      返回：
          dict: 视频统计信息或 None
      """
    # 提取 JSON 数据
    json_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
    json_match = re.search(json_pattern, web_page_attribute, re.S)
    print(json_match)
    if json_match:
        json_data = json_match.group(1)
        data = json.loads(json_data)
        # 定位视频统计数据
        video_stats = data.get("__DEFAULT_SCOPE__",{}).get("webapp.video-detail",{}).get("itemInfo",{}).get("itemStruct",{})
        if video_stats:
            diggCount = video_stats.get('stats',{}).get('diggCount')
            shareCount = video_stats.get('stats',{}).get('shareCount')
            commentCount = video_stats.get('stats',{}).get('commentCount')
            playCount = video_stats.get('stats',{}).get('playCount')
            # 将时间戳转换为可读日期时间
            create_time = video_stats.get('createTime')
            publish_time = datetime.fromtimestamp(int(create_time)).strftime('%Y%m%d')
            # 返回需要的值
            return {
                "diggCount": diggCount,
                "shareCount": shareCount,
                "commentCount": commentCount,
                "playCount": playCount,
                "publish_time": publish_time
            }
        else:
            print("未找到视频统计数据")
            return None
    else:
        print("未找到 JSON 数据")
        return None
video_data = read_video_data(web_page_attribute)
web_data_table = [[-1,-1,-1]]