import datetime

import requests,pandas,time
from json import loads


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
class a():
    def __init__(self,code):
        self.code=code



    def yjfp(self):
        data=pandas.DataFrame(columns=['报告期','业绩披露日期','送转总比例','送股比例','转股比例','现金分红比例',
                                       '股息率（%）','每股收益(元)','每股净资产(元)','每股公积金(元)','每股未分配利润(元)',
                                       '净利润同比增长(%)','总股本(亿）','预案公告日','股权登记日','除权除息日',
                                       '方案进度','最新公告日期'])
        data1=pandas.DataFrame(columns=['报告期','分配方案预案 ','最新公告日期','预案公告日','预案公告日后10日涨幅% ',
                                        '股权登记日','股权登记日前10日涨幅%','除权除息日','除权除息日后30日涨幅%'])
        for i in range(1,5):
            time.sleep(1)
            url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112303927190131472946_1652755889236&sortColumns=REPORT_DATE&sortTypes=-1&pageSize=50&pageNumber=%s&reportName=RPT_SHAREBONUS_DET&columns=ALL&quoteColumns=&js={"data":(x),"pages":(tp)}&source=WEB&client=WEB&filter=(SECURITY_CODE="%s")'%(i,self.code)
            response = requests.get(url, headers=headers).text[42:-2]
            josn_=loads(response)
            #print(josn_)
            for j in range(100):
                try:
                    data.loc[len(data.index)] = [josn_['result']['data'][j]['REPORT_DATE'],
                                                 josn_['result']['data'][j]['PLAN_NOTICE_DATE'],
                                                 josn_['result']['data'][j]['BONUS_IT_RATIO'],
                                                 josn_['result']['data'][j]['BONUS_RATIO'],
                                                 josn_['result']['data'][j]['IT_RATIO'],
                                                 josn_['result']['data'][j]['IMPL_PLAN_PROFILE'],
                                                 josn_['result']['data'][j]['PNP_YOY_RATIO'],
                                                 josn_['result']['data'][j]['BASIC_EPS'],
                                                 josn_['result']['data'][j]['BVPS'],
                                                 josn_['result']['data'][j]['PER_CAPITAL_RESERVE'],
                                                 josn_['result']['data'][j]['PER_UNASSIGN_PROFIT'],
                                                 josn_['result']['data'][j]['PNP_YOY_RATIO'],
                                                 josn_['result']['data'][j]['TOTAL_SHARES'],
                                                 josn_['result']['data'][j]['PLAN_NOTICE_DATE'],
                                                 josn_['result']['data'][j]['EQUITY_RECORD_DATE'],
                                                 josn_['result']['data'][j]['EX_DIVIDEND_DATE'],
                                                 josn_['result']['data'][j]['ASSIGN_PROGRESS'],
                                                 josn_['result']['data'][j]['PUBLISH_DATE'],]

                    data1.loc[len(data1.index)]=[josn_['result']['data'][j]['REPORT_DATE'],
                                                 josn_['result']['data'][j]['IMPL_PLAN_PROFILE'],
                                                 josn_['result']['data'][j]['NOTICE_DATE'],
                                                 josn_['result']['data'][j]['PLAN_NOTICE_DATE'],
                                                 josn_['result']['data'][j]['D10_CLOSE_ADJCHRATE'],
                                                 josn_['result']['data'][j]['EQUITY_RECORD_DATE'],
                                                 josn_['result']['data'][j]['BD10_CLOSE_ADJCHRATE'],
                                                 josn_['result']['data'][j]['EX_DIVIDEND_DATE'],
                                                 josn_['result']['data'][j]['D30_CLOSE_ADJCHRATE'],]
                except:
                    break
        return data,data1

    def hsgtcg(self):
        data=pandas.DataFrame(columns=['持股日期','当日收盘价(元)','当日涨跌幅(%)','持股数量(股)',
                                       '持股市值(元)','持股数量占A股百分比(%)','1日','5日','10日'])
        data1=pandas.DataFrame(columns=['持股日期','当日收盘价(元)','当日涨跌幅(%)','机构名称',
                                        '持股数量(股)','持股市值(元)','持股数量占A股百分比(%)','1日','5日','10日'])
        url = '''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112303967261201254463_1652766233512&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_MUTUAL_HOLDSTOCKNORTH_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE="%s")(TRADE_DATE>='2022-02-17')''' % (
        self.code)
        response = requests.get(url, headers=headers).text[42:-2]
        josn_ = loads(response)
        date_ = josn_['result']['data'][0]['TRADE_DATE'][:-9]
        for i in range(1,5):
            time.sleep(1)
            url='''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112303967261201254463_1652766233512&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=50&pageNumber=%s&reportName=RPT_MUTUAL_HOLDSTOCKNORTH_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE="%s")(TRADE_DATE>='2022-02-17')'''%(i,self.code)
            response = requests.get(url, headers=headers).text[42:-2]
            josn_ = loads(response)

            url1='''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230871462137533075_1652767997537&sortColumns=HOLD_DATE&sortTypes=-1&pageSize=50&pageNumber=%s&reportName=RPT_MUTUAL_HOLD_DET&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE="%s")(MARKET_CODE="001")(HOLD_DATE='%s')'''%(i,self.code,date_)
            response1 = requests.get(url1, headers=headers).text[41:-2]
            josn1_ = loads(response1)

            #print(josn_)
            # print(josn1_)

            for j in range(100):
                try:
                    data.loc[len(data.index)] = [josn_['result']['data'][j]['TRADE_DATE'],
                                                 josn_['result']['data'][j]['CLOSE_PRICE'],
                                                 josn_['result']['data'][j]['CHANGE_RATE'],
                                                 josn_['result']['data'][j]['HOLD_SHARES'],
                                                 '%.4f'%josn_['result']['data'][j]['HOLD_MARKET_CAP'],
                                                 josn_['result']['data'][j]['A_SHARES_RATIO'],
                                                 '%.4f'%josn_['result']['data'][j]['HOLD_MARKETCAP_CHG1'],
                                                 '%.4f'%josn_['result']['data'][j]['HOLD_MARKETCAP_CHG5'],
                                                 '%.4f'%josn_['result']['data'][j]['HOLD_MARKETCAP_CHG10']]
                except:
                    break
            for j in range(100):
                try:
                    data1.loc[len(data1.index)] = [josn1_['result']['data'][j]['HOLD_DATE'],
                                                 josn1_['result']['data'][j]['CLOSE_PRICE'],
                                                 josn1_['result']['data'][j]['CHANGE_RATE'],
                                                 josn1_['result']['data'][j]['ORG_NAME'],

                                                 '%.4f'%josn1_['result']['data'][j]['HOLD_NUM'],
                                                 josn1_['result']['data'][j]['HOLD_MARKET_CAP'],
                                                 josn1_['result']['data'][j]['HOLD_SHARES_RATIO'],

                                                 '%.4f'%josn1_['result']['data'][j]['HOLD_MARKET_CAPONE'],
                                                 '%.4f'%josn1_['result']['data'][j]['HOLD_MARKET_CAPFIVE'],
                                                 '%.4f'%josn1_['result']['data'][j]['HOLD_MARKET_CAPTEN']]
                except:
                    break
        return data,data1

    def rzrq(self):
        data=pandas.DataFrame(columns=['交易日期','收盘价(元)','涨跌幅(%)','融资余额(元)','融资余额占流通市值比',
                                       '融资买入额(元)','融资偿还额(元)','融资净买入(元)','融券余额(元)',
                                       '融券余量(股)','融券卖出量(股)','融券偿还量(股)','融券净卖出(股)',
                                       '融资融券余额(元)','融资融券余额差值(元)'])
        for i in range(1,70):
            time.sleep(1)
            url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=datatable3553486&reportName=RPTA_WEB_RZRQ_GGMX&columns=ALL&source=WEB&sortColumns=date&sortTypes=-1&pageNumber=%s&pageSize=50&filter=(scode="%s")&pageNo=1&_=1652770681984'%(i,self.code)
            response = requests.get(url, headers=headers).text[17:-2]
            josn_=loads(response)
            #print(josn_)
            for j in range(100):
                try:
                    data.loc[len(data.index)] = [josn_['result']['data'][j]['DATE'],
                                                 josn_['result']['data'][j]['SPJ'],
                                                 josn_['result']['data'][j]['ZDF'],
                                                 josn_['result']['data'][j]['RZYE'],
                                                 josn_['result']['data'][j]['RZYEZB'],
                                                 josn_['result']['data'][j]['RZMRE'],

                                                 josn_['result']['data'][j]['RZCHE'],
                                                 josn_['result']['data'][j]['RZJME'],
                                                 '%.4f'%josn_['result']['data'][j]['RQYE'],

                                                 josn_['result']['data'][j]['RQYL'],
                                                 josn_['result']['data'][j]['RQMCL'],
                                                 josn_['result']['data'][j]['RQCHL'],
                                                 josn_['result']['data'][j]['RQJMG'],
                                                 '%.4f'%josn_['result']['data'][j]['RZRQYE'],
                                                 '%.4f'%josn_['result']['data'][j]['RZRQYECZ'],]
                except:
                    break
        return data

    def executive(self):
        data=pandas.DataFrame(columns=['日期','代码','名称','变动人','变动股数','成交均价','变动金额(万)',
                                       '变动原因','变动比例(‰)','变动后持股数','持股种类','董监高人员姓名',
                                       '职务','变动人与董监高的关系'])
        for i in range(1,10):
            time.sleep(1)
            url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=datatable1913313&reportName=RPT_EXECUTIVE_HOLD_DETAILS&columns=ALL&quoteColumns=&filter=(SECURITY_CODE="%s")&pageNumber=%s&pageSize=30&sortTypes=-1,1,1&sortColumns=CHANGE_DATE,SECURITY_CODE,PERSON_NAME&source=WEB&client=WEB&_=1652773712684'%(self.code,i)
            response = requests.get(url, headers=headers).text[17:-2]
            josn_=loads(response)
            #print(josn_)
            for j in range(100):
                try:
                    data.loc[len(data.index)] = [josn_['result']['data'][j]['CHANGE_DATE'],
                                                 josn_['result']['data'][j]['SECURITY_CODE'],
                                                 josn_['result']['data'][j]['SECURITY_NAME'],
                                                 josn_['result']['data'][j]['PERSON_NAME'],
                                                 josn_['result']['data'][j]['CHANGE_SHARES'],
                                                 josn_['result']['data'][j]['AVERAGE_PRICE'],

                                                 josn_['result']['data'][j]['CHANGE_AMOUNT'],
                                                 josn_['result']['data'][j]['CHANGE_REASON'],
                                                 josn_['result']['data'][j]['CHANGE_RATIO'],

                                                 josn_['result']['data'][j]['CHANGE_AFTER_HOLDNUM'],
                                                 josn_['result']['data'][j]['HOLD_TYPE'],
                                                 josn_['result']['data'][j]['DSE_PERSON_NAME'],
                                                 josn_['result']['data'][j]['POSITION_NAME'],
                                                 josn_['result']['data'][j]['PERSON_DSE_RELATION']]

                except:
                    break
        return data


if __name__=='__main__':
    '''
    600519
    000002
    600809
    300059
    '''
    code='600519'

    shili=a(code)

    b,c=shili.yjfp()
    print(b.to_string())
    print(c.to_string())

    d,e=shili.hsgtcg()
    print(d.to_string())
    print(e.to_string())

    f=shili.rzrq()
    print(f.to_string())

    g=shili.executive()
    print(g.to_string())