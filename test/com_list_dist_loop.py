list1 = [['20250120',	2,	'印度尼西亚',	'痘痘净',	'https://www.tiktok.com/@icaaa.ar/video/7459106354721082642'],
['20250120',	3,	'马来西亚',	'组合-五件套',	'https://www.tiktok.com/@whoskhaira/video/7459393415323634962'],
['20250120',	4,	'泰国',	'组合-美白组合2pcs',	'https://www.tiktok.com/@pari_ch29/video/7460511159163063557'],
['20250120',	5,	'泰国',	'双管洁面',	'https://www.tiktok.com/@astpfk/video/7459227228216364296'],
['20250120',	6,	'印度尼西亚',	'痘痘净',	'https://www.tiktok.com/@annisahnahda/video/7459263212895079685'],]

date = [row[0] for row in list1]  
print(date)  # ['20250120', '20250120', '20250120', '20250120', '20250120']

list2 = []
for i in list1:
  list2.append(i[2:4]) 
print(list2)  # [['印度尼西亚', '痘痘净'], ['马来西亚', '组合-五件套'], ['泰国', '组合-美白组合2pcs'], ['泰国', '双管洁面'], ['印度尼西亚', '痘痘净']]

list3 = []
for i in list1:
  info1 = [
    i[1],
    i[0],
  ]
  list3.append(info1)
print(list3)  # [[2, '20250120'], [3, '20250120'], [4, '20250120'], [5, '20250120'], [6, '20250120']]


# 
# for item in rows:
#         rmb_price_value = item.get("rmbPrice", 0)
#         gmv_value = item.get("gmv", 0)
#         try:
#             rmb_price = float(rmb_price_value)
#         except (ValueError, TypeError):
#             rmb_price = 0.0
#         try:
#             gmv_value = float(item.get("gmv", 0))
#         except (ValueError, TypeError):
#             gmv_value = 0.0
#         info = [
#             today_date,
#             id ,
#             item.get("country"),        # 国家
#             item.get("product"),        # 产品名称
#             item.get("contentLink"),    # 视频链接
#             0,  
#             item.get("kolId"),
#             gmv_value,
#             rmb_price,
#         ]
#         video_info.append(info)  # 将列表添加到 video_info
#         id += 1
la = 'ptsfhbhn'
lst = list(la)
print(lst)  

      