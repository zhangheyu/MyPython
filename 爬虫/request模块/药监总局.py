import requests
import json
import time

id_list = []  # 存储企业id
all_detail_list = []  # 存储企业详情
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
# http://scxk.nmpa.gov.cn:81/xk/
# http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList  ajax 获取企业列表
# http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById  ajax  获取企业详情


# 批量获取不同企业的id
def get_company_ids(page_num):
    for page in range(1, page_num):
        url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
        data = {
            'on': 'true',
            'page': page,
            'pageSize': 15,  # 每次获取15个企业
            'productName': '',
            'conditionType': 1,
            'applyname': '',
            'applysn': ''
        }
        json_ids = requests.post(url=url, data=data, headers=headers).json()
        for dic in json_ids['list']:
            id_list.append(dic['ID'])
        print(f'获取第{page}页数据完成')
        time.sleep(1)
        # print(id_list)


# 批量获取企业详情
def get_company_detail_info():
    post_url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    for id in id_list:
        data = {
            'id': id
        }
        detail_json = requests.post(url=post_url, data=data, headers=headers).json()
        # print(detail_json)
        all_detail_list.append(detail_json)


if __name__ == '__main__':
    print('获取化妆品生产许可企业信息')
    get_company_ids(11)
    print('获取企业id完成')
    get_company_detail_info()
    size = len(all_detail_list)
    print(f'获取企业详细信息完成，共有{size}企业')
    # 存储企业信息
    fp = open('化妆品生产许企业信息.json', 'w', encoding='utf-8')
    json.dump(all_detail_list, fp, ensure_ascii=False)
    print('over')
