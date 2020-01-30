#! usr/bin/python
#coding=utf-8

import datetime
from datetime import timedelta
import holiday
import lunar



SOLAR_ANNIVERSARY = [
]
#农历 纪念日 每年都有的
LUNAR_ANNIVERSARY = [
]

_lunar = lunar.CalendarToday()

def custom_anniversary():
    lunar_month = _lunar.lunar()[1]
    lunar_day = _lunar.lunar()[2]
    solar_month = _lunar.solar()[1]
    solar_day = _lunar.solar()[2]
    lunar_anni = lunar.festival_handle(LUNAR_ANNIVERSARY,lunar_month,lunar_day)
    solar_anni = lunar.festival_handle(SOLAR_ANNIVERSARY,solar_month,solar_day)
    anni = ''
    if lunar_anni:
        anni += lunar_anni
    if solar_anni:
        anni += solar_anni
    return anni

def calculate_anniversary():
    """
        {
            '20200101':[{'anniversary':'0101#xx生日#','solar':True}]
        }
    """
    anniversaries = {}

    for l in LUNAR_ANNIVERSARY:
        date_str = l.split('#')[0]
        month = int(date_str[:2])
        day = int(date_str[2:])
        solar_date = lunar.CalendarToday.lunar_to_solar(_lunar.solar()[0],month,day)#下标和位置
        date_str = solar_date.strftime('%Y%m%d')
        try:
            list = anniversaries[date_str]
        except Exception as e:
            anniversaries[date_str] = []
            list = anniversaries[date_str]
        list.append({'anniversary':l,'solar':False})

    for s in SOLAR_ANNIVERSARY:
        comps =  s.split('#')
        print(comps)
        date_str = comps[0]
        date_str = str(_lunar.solar()[0])+date_str #20200101
        try:
            list = anniversaries[date_str]
        except Exception as e:
            anniversaries[date_str] = []
            list = anniversaries[date_str]
        list.append({'anniversary':s,'solar':True})


#根据key 排序 因为key就是日期字符串
    list=sorted(anniversaries.items(),key=lambda x:x[0])
    #找到第一个大于今天的纪念日
    for item in list:
        key = item[0]
        annis = item[1] #纪念日数组
        now_str = datetime.datetime.now().strftime('%Y-%m-%d')
        today = datetime.datetime.strptime(now_str, "%Y-%m-%d")
        last_update = datetime.datetime.strptime(key,'%Y%m%d')
        days = (last_update - today).days
        if days > 0:
            return key,days,annis
    return None

def main():
    print(custom_anniversary())


if __name__ == '__main__':
    main()
