#coding='utf-8'
import pandas
from requests import get
from time import sleep
from json import loads


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
}

def main():
    datalist=[]
    list=[5,1,3]
    list1=['','H','S']
    for i,o in zip(list,list1):
        data = pandas.DataFrame(columns=['日期',
                                         '沪深300涨跌幅',
                                         '增持市值/亿',
                                         '增持占全市场比',
                                         '持股市值/万亿',
                                         '持股占全市场比',
                                         '行业市值增持',
                                         '行业占板块比增加',
                                         '行业占市场比增加',
                                         '增持股市场增持',
                                         '增持股股数增加',
                                         '增持股占股比增加',
                                         ])
        for j in range(1,6):
            sleep(1.5)
            url = '''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123006899198984723132_1651300577873&sortColumns=HOLD_DATE&sortTypes=-1&pageSize=50&pageNumber=%d&columns=ALL&source=WEB&client=WEB&reportName=RPT_%sMUTUAL_MARKET_STA&filter=(MARKET_CODE="00%d")''' %(j,o,i)
            a =get(url, headers=headers).text
            b = loads(a[43:-2])
            for k in range(1200):
                try:
                    # print(b['result']['data'][k]['HOLD_DATE'])
                    # print(b['result']['data'][k]['CHANGE_RATE'])
                    # print(b['result']['data'][k]['ADD_MARKET_CAP'])
                    # print(b['result']['data'][k]['ADD_MARKET_RATE'])
                    # print(b['result']['data'][k]['HOLD_MARKET_CAP'])
                    # print(b['result']['data'][k]['HOLD_MARKET_RATE'])
                    # print(b['result']['data'][k]['ADD_MARKET_BNAME'])
                    # print(b['result']['data'][k]['BOARD_RATE_BNAME'])
                    # print(b['result']['data'][k]['MARKET_RATE_BNAME'])
                    # print(b['result']['data'][k]['ADD_MARKET_MNAME'])
                    # print(b['result']['data'][k]['ADD_SHARES_MNAME'])
                    # print(b['result']['data'][k]['MARKET_RATE_MNAME'])
                    # print()
                    data.loc[len(data.index)]=[b['result']['data'][k]['HOLD_DATE'],
                    b['result']['data'][k]['CHANGE_RATE'],
                    '%0.2f'%(b['result']['data'][k]['ADD_MARKET_CAP']/100000000),
                    '%0.6f'%b['result']['data'][k]['ADD_MARKET_RATE'],
                    '%0.3f'%(b['result']['data'][k]['HOLD_MARKET_CAP']/100000000000),
                    b['result']['data'][k]['HOLD_MARKET_RATE'],
                    b['result']['data'][k]['ADD_MARKET_BNAME'],
                    b['result']['data'][k]['BOARD_RATE_BNAME'],
                    b['result']['data'][k]['MARKET_RATE_BNAME'],
                    b['result']['data'][k]['ADD_MARKET_MNAME'],
                    b['result']['data'][k]['ADD_SHARES_MNAME'],
                    b['result']['data'][k]['MARKET_RATE_MNAME']
                    ]
                except:
                    break

        datalist.append(data)
    return datalist


if __name__=='__main__':
    a=main()
    print(a[0].to_string())