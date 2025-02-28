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
            # 返回需要的值
            return video_stats
        else:
            print("未找到视频统计数据")
            return None
    else:
        print("未找到 JSON 数据")
        return None
video_stats = read_video_data(web_page_attribute)
web_data_table = [[None,None,None]]
if video_stats is None:
  continue
KOLID = KOLID_list[id_list[loop_item_index]-2]
GMV = GMV_list[id_list[loop_item_index]-2]
RMB = RMB_list[id_list[loop_item_index]-2]
diggCount = video_stats.get('stats',{}).get('diggCount')                       #  点赞量
shareCount = video_stats.get('stats',{}).get('shareCount')                     #  分享量
commentCount = video_stats.get('stats',{}).get('commentCount')                 #  评论量
playCount = video_stats.get('stats',{}).get('playCount')                       #  播放量
create_time = video_stats.get('createTime')            
publish_time = datetime.fromtimestamp(int(create_time)).strftime('%Y%m%d')     #  发布时间

if playCount is None:
  break

                              
