# coding=utf-8
import pandas,datetime
from time import time,localtime,strftime
from requests import get
from json import loads
from  requests import get

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
}
def request_data(gupiao):
    data=pandas.DataFrame(columns=['持股日期',
                                    '当日收盘价(元)',
                                    '当日涨跌幅(%)',
                                    '持股数量(股)',
                                    '持股市值(元)',
                                    '持股数量占A股百分比(%)',
                                    '持股市值变化(元)1日',
                                    '持股市值变化(元)5日',
                                    '持股市值变化(元)10日'
    ])

    for i in range(1,3):
        url='''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery11230886649555660316_%d&sortColumns=TRADE_DATE&sortTypes=-1&pageSize=50&pageNumber=%d&reportName=RPT_MUTUAL_HOLDSTOCKNORTH_STA&columns=ALL&source=WEB&client=WEB&filter=(SECURITY_CODE="%s")(TRADE_DATE>='2022-01-28')'''%(int(time()*1000),i,gupiao)
        a = get(url, headers=headers).text
        c = loads(a[41:-2])
        for j in range(100):
            try:
                # print([c['result']['data'][j]['TRADE_DATE'],
                #      c['result']['data'][j]['CLOSE_PRICE'],
                #      c['result']['data'][j]['CHANGE_RATE'],
                #      c['result']['data'][j]['HOLD_SHARES'],
                #      str(c['result']['data'][j]['HOLD_MARKET_CAP']),
                #      c['result']['data'][j]['A_SHARES_RATIO'],
                #      str(c['result']['data'][j]['HOLD_MARKETCAP_CHG1']),
                #      str(c['result']['data'][j]['HOLD_MARKETCAP_CHG5']),
                #      str(c['result']['data'][j]['HOLD_MARKETCAP_CHG10'])])
                data.loc[len(data.index)]=[c['result']['data'][j]['TRADE_DATE'],
                              c['result']['data'][j]['CLOSE_PRICE'],
                              c['result']['data'][j]['CHANGE_RATE'],
                              c['result']['data'][j]['HOLD_SHARES'],
                              str(c['result']['data'][j]['HOLD_MARKET_CAP']),
                              c['result']['data'][j]['A_SHARES_RATIO'],
                              str(c['result']['data'][j]['HOLD_MARKETCAP_CHG1']),
                              str(c['result']['data'][j]['HOLD_MARKETCAP_CHG5']),
                              str(c['result']['data'][j]['HOLD_MARKETCAP_CHG10'])]
            except:
                break
    return data


class a():
    def __init__(self,data,delay,reference,n,m):
        self.delay=delay
        self.data=data
        self.reference=reference
        self.n=n
        self.m=m
        self.clean_data()

    def clean_data(self):
        self.data.dropna(inplace=True)
        self.data['持股日期']=self.data['持股日期'].str.split(" ", expand=True)[0]

    def judger1(self,dtime,up_limit=0,dowm_limit=-0):
        if self.delay==True:
            delay_true=1
        elif self.delay==False:
            delay_true=0
        for i in range(0, self.data.shape[0]):
            a = i
            b=self.data.loc[i, '持股日期']
            if self.data.loc[i, '持股日期'] <= dtime:
                break
        in_up_int=1
        try:
            intt=self.data.loc[a+delay_true,self.reference]/self.data.loc[a+delay_true+self.n,self.reference]-1
        except:
            return None,0
        try:
            for i in range(a-self.m,a):
                in_up_int*=1 + (self.data.loc[i, '当日涨跌幅(%)']/100)
        except:
            in_up_int='未来天数不足'
        if intt>up_limit:
            return '流入',in_up_int
        elif intt<dowm_limit:
            return '流出',in_up_int
        else:
            return '中性',in_up_int

    def judger2(self,dtime):
        if self.delay==True:
            delay_true=1
        elif self.delay==False:
            delay_true=0
        for i in range(0, self.data.shape[0]):
            a = i
            b=self.data.loc[i, '持股日期']
            if self.data.loc[i, '持股日期'] <= dtime:
                break
        intt=0
        in_up_int=1
        try:
            for i in range(a+delay_true,a+self.n+delay_true):
                if self.data.loc[i,self.reference]-self.data.loc[i+1,self.reference]>0:
                    intt+=1
        except:
            return None,0
        try:
            for i in range(a-self.m,a):
                in_up_int*=1 + (self.data.loc[i,'当日涨跌幅(%)']/100)
        except:
            in_up_int='未来天数不足'

        if intt==self.n:
            return '流入',in_up_int
        elif intt==0:
            return '流出',in_up_int
        else:
            return '中性',in_up_int

    def get_statistic_info(self,fun,start_time,end_time):
        '''
        变量
        num_in是后n天流入天数或者连续流入天数,int类型
        num_out是后n天流出的天数或者连续流出天数,int类型
        num_in_up流入且上涨天数,int类型
        num_in_down流入且下跌天数,int类型
        num_out_up流出且上涨天数,int类型
        num_out_down流出且下跌天数,int类型
        rate_ave_in过去流入的情况下，未来的平均收益率，float类型
        rate_ave_out过去流出的情况下，未来的平均收益率，float类型
        num_med中性的天数,int类型
        num_med_up中性且未来上涨的天数,int类型
        num_med_down中性且未来下跌的天数,int类型

        返回值：num
        {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out,
               'rate_ave_med': rate_ave_med, 'num_med': num_med, 'num_med_up': num_med_up, 'num_med_down': num_med_down
               }
        类型：dict

        '''
        num_in=0
        num_in_up = 0
        num_in_down = 0
        num_out = 0
        num_out_up=0
        num_out_down = 0
        num_med=0
        num_med_up = 0
        num_med_down = 0
        rate_ave_in=0
        rate_ave_out=0
        rate_ave_med=0
        start_index=None
        end_index=None
        if self.delay==True:
            delay_false=-1
        elif self.delay==False:
            delay_false=0
        for i in range(0, self.data.shape[0]):
            if self.data.loc[i, '持股日期'] <= start_time:
                end_index= i
                break
        for i in range(0, self.data.shape[0]):
            if self.data.loc[i, '持股日期'] <= end_time:
                start_index= i
                break
        if end_index==None:
            end_index=self.data.shape[0]-1
        back_up=self.data.loc[start_index:end_index]
        back_up.index=[i for i in range(0,back_up.shape[0])]
        for i in range(back_up.shape[0]):
            if fun=='judger1':a,b=self.judger1(back_up.loc[i,'持股日期'])
            elif fun=='judger2':a,b=self.judger2(back_up.loc[i,'持股日期'])

            if a=='流入':
                num_in+=1
                if b=='未来天数不足':pass
                else:
                    if b!=0:rate_ave_in += (b - 1)
                    if b>1 and b!='未来天数不足':num_in_up+=1
                    else:num_in_down+=1
            elif a=='流出':
                num_out+=1
                if b=='未来天数不足':pass
                else:
                    if b!=0:rate_ave_out += (b - 1)
                    if b>1 and b!='未来天数不足':num_out_up+=1
                    else:num_out_down+=1
            elif a=='中性':
                num_med+=1
                if b=='未来天数不足':pass
                else:
                    if b!=0:rate_ave_med += (b - 1)
                    if b>1 and b!='未来天数不足':num_med_up+=1
                    else:num_med_down+=1

        if fun == 'judger1':a, b = self.judger1(back_up.loc[0, '持股日期'])
        elif fun == 'judger2':a, b = self.judger2(back_up.loc[0, '持股日期'])
        if num_in!=0:rate_ave_in=float(rate_ave_in)/num_in
        if num_out!=0:rate_ave_out=float(rate_ave_out)/num_out
        if num_med!=0:rate_ave_med=float(rate_ave_med)/num_med
        num = {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out,
               'rate_ave_med': rate_ave_med, 'num_med': num_med, 'num_med_up': num_med_up, 'num_med_down': num_med_down,'judge_today':a}
        return num


if __name__=='__main__':
    gupiao = ['600519','000729','600510']
    reference = '持股数量(股)'
    judger = 'judger1'
    n = 1
    m = 5
    delta = 90
    delay = False
    frame = pandas.DataFrame(columns=['股票代码', 'm', 'best_n', 'rate_ave_out', 'Judge_today'])
    for j in gupiao:
        data1 = pandas.DataFrame(columns=['股票代码', 'm', 'best_n', 'rate_ave_out', 'judge_today'])
        for i in range(1,11):
            data = request_data(j)
            b = a(data, delay, reference, i, m)
            e = b.get_statistic_info(judger,str(datetime.date(2000,2,8)-datetime.timedelta(days=delta)),str(strftime('%Y-%m-%d',localtime(time()))))
            data1.loc[len(data1.index)]=[j,m,i,e['rate_ave_out'],e['judge_today']]
        frame.loc[len(frame.index)] = data1.sort_values('rate_ave_out').head(1).values[0]
    print(frame)
