# 脚本文档链接：https://merico.feishu.cn/docx/Rcy8dd8OqolQvYx3IU4cIzUJnGw
# 该脚本作用是查询账户列表，即获取思码逸系统内的所有账户信息
# 输入：暂无输入
# 输出：全部账户列表信息

import csv
import re
import sys
import time
import os
sys.path.append("../..")
from open_api_client import Client
from open_api_sdk_v2 import get_account_list
from datetime import date, timedelta, datetime



endpoint = 'http://10.70.55.119:30004'             # 填入您的思码逸系统完整域名
app_id = 'b1b22939ea2e48eb'                  # 填入您的思码逸系统管理员账号openapi的app_id
secret = '26175c79096ccb70e7a8794797f27b90'  # 填入您的思码逸系统管理员账号openapi的secret


dt_now_start = datetime.now()
date_now_total = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
output_path = dt_now_start.strftime('03_output_account_list_%Y%m%d%H%M%S/')
if not os.path.exists(output_path):
    os.makedirs(output_path)



def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec



def export_account_list(client):
    # 以下内容根据需要填写
    # 要查询的账户的ids
    account_list = get_account_list(client)

    second = sleep_time(0, 0, 5)

    # 需求1: 获取账户列表
    account_lists_result = {}
    group_length = len(account_list)
    for index, single_account in enumerate(account_list):
        print(f"[{index+1}/{group_length}]当前进度为{round((index+1)/(group_length), 4)*100}%, 准备获取账户 {single_account['name']} id = {single_account['id']} 的账户信息 ")

        account_lists_result[str(index) + '-' + single_account['id']] = {}
        account_lists_result[str(index) + '-' + single_account['id']]['账户ID'] = single_account['id']
        account_lists_result[str(index) + '-' + single_account['id']]['职位'] = single_account['title']
        account_lists_result[str(index) + '-' + single_account['id']]['账户创建时间'] = single_account['createTime']
        account_lists_result[str(index) + '-' + single_account['id']]['账户更新时间'] = single_account['updateTime']
        account_lists_result[str(index) + '-' + single_account['id']]['姓名'] = single_account['name']
        account_lists_result[str(index) + '-' + single_account['id']]['薪资'] = single_account['salary']
        account_lists_result[str(index) + '-' + single_account['id']]['职级'] = single_account['rank']
        account_lists_result[str(index) + '-' + single_account['id']]['晋升日期'] = single_account['promotionDate']
        account_lists_result[str(index) + '-' + single_account['id']]['工号'] = single_account['jobNumber']
        account_lists_result[str(index) + '-' + single_account['id']]['账号是否启用'] = single_account['enable']
        account_lists_result[str(index) + '-' + single_account['id']]['账号是否可登录'] = single_account['allowLogin']
        account_lists_result[str(index) + '-' + single_account['id']]['用户主邮箱地址'] = single_account['primaryEmail']
        account_lists_result[str(index) + '-' + single_account['id']]['用户邮箱列表'] = single_account['emails']
        account_lists_result[str(index) + '-' + single_account['id']]['团队ID列表'] = single_account['teamIds']
        account_lists_result[str(index) + '-' + single_account['id']]['用户角色ID列表'] = single_account['roleIds']
        account_lists_result[str(index) + '-' + single_account['id']]['是否为超级管理员'] = single_account['isAdmin']
        account_lists_result[str(index) + '-' + single_account['id']]['自定义标签'] = single_account['tags']

        # print(f"account_lists_result = {account_lists_result}")

        print(f"目前累计检索到的数据数量是: {len(account_lists_result.keys())}")
        # if index == 20:
        #     time.sleep(second)


    headers = []

    headers.append('账户ID')
    headers.append('职位')
    headers.append('账户创建时间')
    headers.append('账户更新时间')
    headers.append('姓名')
    headers.append('薪资')
    headers.append('职级')
    headers.append('晋升日期')
    headers.append('工号')
    headers.append('账号是否启用')
    headers.append('账号是否可登录')
    headers.append('用户主邮箱地址')
    headers.append('用户邮箱列表')
    headers.append('团队ID列表')
    headers.append('用户角色ID列表')
    headers.append('是否为超级管理员')
    headers.append('自定义标签')

    with open(f'{output_path}/account_list_{date_now_total}.csv', 'w+', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(account_lists_result.values())



if __name__ == '__main__':

    dt_now_start = datetime.now()
    dt_now_start = dt_now_start.isoformat("T")


    client = Client(f'{endpoint}/openapi', app_id, secret)
    
    # 导出account_list
    export_account_list(client)

    dt_now_end = datetime.now()
    dt_now_end = dt_now_end.isoformat("T")
    print(f"导出Excel完成, 开始时间{dt_now_start}")
    print(f"导出Excel完成, 完成时间{dt_now_end}")



