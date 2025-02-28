from datetime import datetime,timedelta

date = datetime.now() # 2025-01-20 15:46:05.584816
today = datetime.today()

print(date)
print(today)
date2 = date.strftime("%y%m%d")  # 250120
print(date2)
data3 = date.strftime('%Y-%m-%d')
print(data3)
data4 = date.strftime('%Y%m%d')
print(data4)

# seven days age
seven_date = (date - timedelta(7)).strftime('%Y%m%d')
print(seven_date)

