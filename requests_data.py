import requests,pandas,time,json

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
}

def requests_data():
    data=pandas.DataFrame(columns=['代码','名称','研报数','机构投资评级(近六个月)买入',
                                   '机构投资评级(近六个月)增持','2021每股收益',
                                   '2022预测每股收益','2023预测每股收益','2024预测每股收益'])
    for i in range(1,49):
        time.sleep(1)
        url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=datatable3132865&reportName=RPT_WEB_RESPREDICT&columns=WEB_RESPREDICT&pageNumber=%d&pageSize=50&sortTypes=-1&sortColumns=RATING_ORG_NUM&p=1&pageNo=1&pageNum=1&_=1652081196721'%i
        a=requests.get(url,headers=headers).text[17:-2]
        b=json.loads(a)
        for j in range(51):

            try:
                # print(b['result']['data'][j]['SECUCODE'])
                # print(b['result']['data'][j]['SECURITY_NAME_ABBR'])
                # print(b['result']['data'][j]['RATING_ORG_NUM'])
                # print(b['result']['data'][j]['RATING_BUY_NUM'])
                # print(b['result']['data'][j]['RATING_ADD_NUM'])
                # print(b['result']['data'][j]['EPS1'])
                # print(b['result']['data'][j]['EPS2'])
                # print(b['result']['data'][j]['EPS3'])
                # print(b['result']['data'][j]['EPS4'])
                # print()
                data.loc[len(data.index)]=[b['result']['data'][j]['SECUCODE'],
                             b['result']['data'][j]['SECURITY_NAME_ABBR'],
                             b['result']['data'][j]['RATING_ORG_NUM'],
                             b['result']['data'][j]['RATING_BUY_NUM'],
                             b['result']['data'][j]['RATING_ADD_NUM'],
                             b['result']['data'][j]['EPS1'],
                             b['result']['data'][j]['EPS2'],
                             b['result']['data'][j]['EPS3'],
                             b['result']['data'][j]['EPS4']]
            except:
                break

    return data




if __name__=='__main__':
    data=requests_data()
    print(data)