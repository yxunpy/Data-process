import requests
from bs4 import BeautifulSoup
import pandas as pd
request_url="http://car.bitauto.com/xuanchegongju/?mid=8"

def get_page_content(request_url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers=headers, timeout=10)
    content = html.text
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

def analysis(soup):
    df=pd.DataFrame (columns=['name', 'low_price(万)', 'high_price(万)','pic_link'])
    temp = soup.find('div', class_='search-result-list')
    item_list=temp.find_all('div',class_='search-result-list-item')
    for itm in item_list:
        temp={}
        pic_link='http:'+itm.find('img')['src']
        name=itm.find('p',class_='cx-name text-hover').text
        if  itm.find('p',class_='cx-price').text.find('-')>0:
            low_price=itm.find('p',class_='cx-price').text.split('-',1)[0]
            high_price=itm.find('p',class_='cx-price').text.split('-',1)[1].split('万')[0]
        else:
            low_price=itm.find('p',class_='cx-price').text.split('万')[0]
            high_price=itm.find('p',class_='cx-price').text.split('万')[0]
        temp['name'], temp['low_price(万)'], temp['high_price(万)'], temp['pic_link']=name,low_price,high_price,pic_link
        df = df.append(temp, ignore_index=True)
    return df

pagenum=3
result=pd.DataFrame (columns=['name', 'low_price(万)', 'high_price(万)','pic_link'])
base_url="http://car.bitauto.com/xuanchegongju/?mid=8"
for i in range(pagenum):
    request_url = base_url + '&page=' + str(i + 1)
    soup=get_page_content(request_url)
    df=analysis(soup)
    #print(df)
    result=result.append(df)
print(result)
result.to_csv('VW brand info_ProjectA.csv',index=False)




