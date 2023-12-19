import sys
import os
import re
import csv
import requests
from open_api_client import Client

endpoint = 'http://10.70.55.119:30004'
app_id = 'b1b22939ea2e48eb'
secret = '26175c79096ccb70e7a8794797f27b90'


def getProjects():
    code, message, result = client.request('/project/list', {'id':'5530da20-28f4-4cfd-93e6-fdda4cd9b37d'})
    assert code == 200, message
    
    print(result)
    return result
    
    
def getEmails():
    code, message, result = client.request('/project/get-emails', {'id':'5530da20-28f4-4cfd-93e6-fdda4cd9b37d'})
    assert code == 200, message
    datas = {}
    datas['emails']=[]
    dev_emails = []
    # print(result)
    for i in result['emails']:
        if re.search(r'@.*google|@.*sony|@intel|@motorola|@samsung|@android|@gmail|@mediatek|@huawei|@xiaomi|@acer|@codeaurora|@mmayer|@nxp|@broadcom|@pixel|@nvidia|@tomtom|@htc|@code|@chrom|@quicinc|@ittiam|@volvo|@effective|@lge|@.*merico|@ti|@arm|@lenovo|@philips|@neusoft|@ecarx', i , re.I):
            datas['emails'].append(i)
        else:
            # if re.search(r'merico', i, re.I):
            
            if not re.search(r'@', i):
                continue
            dev_emails.append(i)
            print(i)
    # print(datas)
    # setFilterMails(datas)
    getDevMetric(dev_emails)
    return result
    
def setFilterMails(emails):
    # code, message, result = client.request('account/exclude-commit-author', {'emails':['yoshinobu.ito@jp.sony.com']})
    code, message, result = client.request('account/exclude-commit-author', emails)
    assert code == 200, message
    

def getDevMetric(emails):
    data = {}
    data["primaryEmailStrs"] = emails
    data["options"] = {}
    data["options"]['authorTime'] = {}
    data["options"]['authorTime']['startDate'] = '2023-01-01Z+08:00'
    data["options"]['authorTime']['endDate'] = '2023-12-19Z+08:00'
    data["options"]['selectColumns'] = ['commit_num', 'dev_equivalent', 'dev_value', 'function_num', 'loc', 'loc_add_line', 'loc_delete_line']
    code, message, result = client.request('/developer/query-efficiency-metric', data)
    assert code == 200, message
    
    exportDevMetric(result)
    print(code)
    print(result)
    
def exportDevMetric(datas):
    path = 'E:\\SiMaYi\\devMetric.csv'
    headers = ['邮箱', '提交数', '开发当量', '函数个数', '代码行数', '新增行数', '删除行数']
    with open(path, 'w+', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        # row = []
        for d in datas:
            row = []
            row.append(d['email'])
            row.append(d['commit_num'])
            row.append(d['dev_equivalent'])
            # row.append(d['dev_value'])
            row.append(d['function_num'])
            row.append(d['loc'])
            row.append(d['loc_add_line'])
            row.append(d['loc_delete_line'])
            # row.append(d['accountId'])
            f_csv.writerow(row)
            print(row)
    
    

if __name__ == "__main__":

    client = Client(f'{endpoint}/openapi', app_id, secret)
    # getProjects()
    getEmails()
    # setFilterMails()
    # exportDevMetric()
    print("Si Ma Yi0")