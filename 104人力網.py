from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
company = []
job = []
job_html = []
company_html = []
content = []
ob_reqiured = {}
o = []

url = "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90%E5%B8%AB&expansionType=job&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc"
res = requests.get(url,headers=headers)
soup = BeautifulSoup(res.text,"html.parser")
# print(soup)
title = soup.select('div[class="b-block__left"]')
# print(title)

try:
    for each_work in title:
        for each_workname in each_work('h2'):
            for each_name in each_workname('a'):
                # print('Job:','https:'+each_name['href'])
                job_html.append('https:'+each_name['href'])
                # print('Job:',each_name.text)
                job.append(each_name.text)
        for each_workname in each_work('li'):
            for each_company in each_workname('a'):
                # print('Company:',each_company.text)
                company.append(each_company.text)
                # print('Company:','https:'+each_company['href'])
                company_html.append('https:'+each_company['href'])

except:
    print('x')
for i in job_html:
    id = i.split('/')[-1].split('?')[0]
    curl = "https://www.104.com.tw/job/ajax/content/{}".format(id)
    headers = {'Referer': "https://www.104.com.tw/job/ajax/content/{}".format(id),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    cres = requests.get(curl,headers=headers)
    cj = json.loads(cres.text)
    content.append(cj['data']['jobDetail']['jobDescription'])
    # print(cj['data']['condition'])

    for i in cj['data']['condition']['acceptRole']['role']:
        o.append(i['description'])    
        # print(i['description'])
    ob_reqiured['身分條件'] = o
    ob_reqiured['具備駕照'] = cj['data']['condition']['driverLicense']
print(ob_reqiured)

# data = {"Company":company,"Company Html":company_html,"Opening Job":job,
#         "Opening Job Html":job_html,"Job's Content":content}
# df = DataFrame(data)
# # print(df)
# df.to_csv('C:\\Users\\Tibame\\Desktop\\practice\\104人力網.csv',encoding="utf-8-sig")
# df.to_excel('C:\\Users\\Tibame\\Desktop\\practice\\104人力網.xlsx',encoding="utf-8-sig")
# print('Completed')