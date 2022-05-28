import pandas,requests,json,time


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
}


def type_conversion(date:str)->str:
    date = str(date)
    if len(date) > 11:
        date = date.split(' ')[0]
    if len(date) == 8:
        date = date[0:4] + '-0' + date[5] + '-0' + date[7]
    if len(date) == 9:
        if date[5:7] == '11' or date[5:7] == '12' or date[5:7] == '10':
            date = date[0:4] + '-' + date[5:7] + '-0' + date[8]
        else:
            date = date[0:4] + '-0' + date[5] + '-' + date[7:9]
    return date

def date_list():
    datelist=pandas.DataFrame(columns=['date'])
    url='https://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPT_MAIN_REPORTDATE&columns=REPORT_DATE&quoteColumns=&pageNumber=1&pageSize=25&sortTypes=-1&sortColumns=REPORT_DATE&source=WEB&client=WEB&callback=jQuery112302059437317214593_1652851084983&_=1652851084984'
    response=requests.get(url,headers=headers).text[42:-2]
    json_=json.loads(response)
    time.sleep(1)
    for i in range(100):

        try:
            datelist.loc[len(datelist.index)]=json_['result']['data'][i]['REPORT_DATE'][:-9]

        except:
            break
    datelist.sort_values('date',inplace=True,ignore_index=True)
    return datelist

def _date_transfer(date:str)->str:
    date=type_conversion(date)
    index=datelist[datelist['date']>=date].head(1).index[0]
    if date!=datelist.loc[index,'date']:
        return datelist.loc[index-1,'date']
    return datelist.loc[index,'date']

def jijin(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','持有基金家数(家)','持股总数(万股)	','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=1&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data

def QFII(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=2&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data

def shebao(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=3&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data

def quanshang(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=4&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data

def baoxian(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=5&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data

def xingtuo(date:str)->pandas.DataFrame:
    data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
                                   '持股变化','持股变动数值(万股)','持股变动比例(%)'])
    for i in range(1,100):
        time.sleep(1)
        url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=6&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(date,i)
        response=requests.get(url,headers=headers).json()
        if response==[]:
            break
        for j in range(53):
            try:
                data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
                                           response['data'][j]['SECURITY_NAME_ABBR'],
                                           response['data'][j]['HOULD_NUM'],
                                           response['data'][j]['TOTAL_SHARES'],
                                           response['data'][j]['HOLD_VALUE'],
                                           response['data'][j]['HOLDCHA'],
                                           response['data'][j]['HOLDCHA_NUM'],
                                           response['data'][j]['HOLDCHA_RATIO']]
            except:
                break
    return data


datelist=date_list()
#print(datelist)

a=_date_transfer('2021-9-29')
print(a)

b=jijin(a)
print(b)

c=QFII(a)
print(c)

d=shebao(a)
print(d)

e=quanshang(a)
print(e)

f=baoxian(a)
print(f)

g=xingtuo(a)
print(g)

#版本二
# def choice_edition(date:str,choice:str)->pandas.DataFrame:
#     data=pandas.DataFrame(columns=['股票代码','股票简称','	持有QFII家数(家)','持股总数(万股)','持股市值(亿元)',
#                                    '持股变化','持股变动数值(万股)','持股变动比例(%)'])
#     for i in range(1,100):
#         time.sleep(1)
#         url='https://data.eastmoney.com/dataapi/zlsj/list?date=%s&type=%s&zjc=0&sortField=HOULD_NUM&sortDirec=1&pageNum=%s&pageSize=50'%(choice,date,i)
#         response=requests.get(url,headers=headers).json()
#         if response==[]:
#             break
#         for j in range(53):
#             try:
#                 data.loc[len(data.index)]=[response['data'][j]['SECURITY_CODE'],
#                                            response['data'][j]['SECURITY_NAME_ABBR'],
#                                            response['data'][j]['HOULD_NUM'],
#                                            response['data'][j]['TOTAL_SHARES'],
#                                            response['data'][j]['HOLD_VALUE'],
#                                            response['data'][j]['HOLDCHA'],
#                                            response['data'][j]['HOLDCHA_NUM'],
#                                            response['data'][j]['HOLDCHA_RATIO']]
#             except:
#                 break
#     return data
# '''
# 1是基金持仓
# 2是QFII持仓
# 3是社保持仓
# 4是券商持仓
# 5是保险持仓
# 6是信托持仓
# '''
# h=choice_edition(a,'1')
# print(h)