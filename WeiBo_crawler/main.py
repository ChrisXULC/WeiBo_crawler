import os
import re 
from jsonpath import jsonpath  
import requests 
import pandas as pd  
import datetime

def trans_time(v_str):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time

def get_weibo_list(k,v):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }
    for page in range(1,v+1):
        print('第{}页'.format(page))
        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {
            'containerid':'100103type=1&q={}'.format(k),
            'page_type':"searchall",
            'page':page
        }
        r = requests.get(url,headers = headers,params = params)
        print(r.status_code)
        cards = r.json()['data']['cards']
#         print(r.json())
        text_list = jsonpath(cards,'$..mblog.text')
#         print(text_list)
        dr = re.compile(r'<[^>]+>',re.S)
        text2_list = []
        print('text is:')
#         print(text_list)
        if not text_list:
            continue
        if type(text_list) == list and len(text_list)>0:
            for text in text_list:
                text2 = dr.sub('',text)
#                 print(text2)
                text2_list.append(text2)
        time_list = jsonpath(cards,'$..mblog.created_at')
        time_list = [trans_time(v_str = i) for i in time_list]
        user_list = jsonpath(cards,'$..mblog.status_city')
        user_list = user_list
        try:
            df = pd.DataFrame(
                {
                    'date':time_list,
                    'content':text2_list,
                    'add':user_list,
                }
            )
            if os.path.exists(file):
                header = None
            else:
                header = ['date','conntent','address']
            df.to_csv(file,mode = 'a+',index = False,header = header, encoding = 'utf-8')
        except:
            pass

if __name__ == '__main__':
    nums = 100
    k = '#上海疫情'
    file = '{}前{}页.csv'.format(k, nums)
    if os.path.exists(file):
        os.remove(file)
    get_weibo_list(k, nums)
