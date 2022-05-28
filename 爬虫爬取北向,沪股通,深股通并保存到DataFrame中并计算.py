#coding='utf-8'
import pandas,datetime,time
from requests import get
from json import loads


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
}
def request_data(i,o):
    data = pandas.DataFrame(columns=['交易日期',
                                     '涨跌幅(%)',
                                     '净买入额(亿元/CNY)',
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
        time.sleep(1)
        url = '''https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery1123006899198984723132_1651300577873&sortColumns=HOLD_DATE&sortTypes=-1&pageSize=50&pageNumber=%d&columns=ALL&source=WEB&client=WEB&reportName=RPT_%sMUTUAL_MARKET_STA&filter=(MARKET_CODE="00%d")''' %(j,o,i)
        a =get(url, headers=headers).text
        b = loads(a[43:-2])
        for k in range(1000):
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
    return data


class a():
    def __init__(self, data, delay, reference,delta,n, m):
        self.m = m
        self.n = n
        self.delay = delay
        self.data = data
        self.delta=delta
        self.clean_data()

    def clean_data(self):
        self.data.dropna(inplace=True)
        self.data['交易日期'] = self.data['交易日期'].str.split(" ", expand=True)[0]
        self.data['净买入额(亿元/CNY)']=self.data['净买入额(亿元/CNY)'].astype('float')
        self.data['涨跌幅(%)']=self.data['涨跌幅(%)'].astype('float')
        self.data=self.data.head(self.delta)

    def judger1(self, dtime, up_limit=0, dowm_limit=-0):
        if self.delay == True:
            delay_true = 1
        elif self.delay == False:
            delay_true = 0
        for i in range(0, self.data.shape[0]):
            a = i
            b = self.data.loc[i, '交易日期']
            if self.data.loc[i, '交易日期'] <= dtime:
                break

        intt = 0
        in_up_int = 1
        try:
            for i in range(a + delay_true, a + self.n + delay_true):
                intt += self.data.loc[i, '净买入额(亿元/CNY)']

        except:
            return None,0
        try:
            for i in range(a - self.m, a):
                in_up_int *= 1 + (self.data.loc[i, '涨跌幅(%)'] / 100)
        except:
            in_up_int = '未来天数不足'
        if intt > up_limit:
            return '流入', in_up_int
        elif intt < dowm_limit:
            return '流出', in_up_int
        else:
            return '中性', in_up_int

    def judger2(self, dtime):
        if self.delay == True:
            delay_true = 1
        elif self.delay == False:
            delay_true = 0
        for i in range(0, self.data.shape[0]):
            a = i
            b = self.data.loc[i, '交易日期']
            if self.data.loc[i, '交易日期'] <= dtime:
                break

        intt = 0
        in_up_int = 1
        try:
            for i in range(a + delay_true, a + self.n + delay_true):
                if self.data.loc[i, '净买入额(亿元/CNY)'] > 0:
                    intt += 1
        except:
            return None, 0
        try:
            for i in range(a - self.m, a):
                in_up_int *= 1 + (self.data.loc[i, '涨跌幅(%)'] / 100)
        except:
            in_up_int = '未来天数不足'
        if intt == self.n:
            return '流入', in_up_int
        elif intt == 0:
            return '流出', in_up_int
        else:
            return '中性', in_up_int

    def get_statistic_info(self, fun, start_time, end_time):
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
        num_in = 0
        num_in_up = 0
        num_in_down = 0
        num_out = 0
        num_out_up = 0
        num_out_down = 0
        num_med = 0
        num_med_up = 0
        num_med_down = 0
        rate_ave_in = 0
        rate_ave_out = 0
        rate_ave_med = 0
        if self.delay == True:
            delay_true = 0
        elif self.delay == False:
            delay_true = 1
        start_index = None
        end_index = None
        for i in range(0, self.data.shape[0]):
            if self.data.loc[i, '交易日期'] <= start_time:
                end_index = i
                break
        for i in range(0, self.data.shape[0]):
            if self.data.loc[i, '交易日期'] <= end_time:
                start_index = i
                break
        if end_index == None:
            end_index = self.data.shape[0] - 1
        back_up = self.data.loc[start_index:end_index]
        back_up.index = [i for i in range(0, back_up.shape[0])]

        for i in range(back_up.shape[0]):
            if fun == 'judger1':a, b = self.judger1(back_up.loc[i, '交易日期'])
            elif fun == 'judger2':a, b = self.judger2(back_up.loc[i, '交易日期'])
            if a=='流入':
                num_in+=1
                if b=='未来天数不足':pass
                else:
                    if b!=0:rate_ave_in += (b - 1)
                    if b>1 and b!='未来天数不足':num_in_up+=1
                    else:num_in_down+=1
            elif a=='流出':
                num_out+=1
                if b=='未来天数不足':
                    pass
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
        if fun == 'judger1':a, b = self.judger1(back_up.loc[0, '交易日期'])
        elif fun == 'judger2':a, b = self.judger2(back_up.loc[0, '交易日期'])
        if num_in != 0: rate_ave_in = float(rate_ave_in) / num_in
        if num_out != 0: rate_ave_out = float(rate_ave_out) / num_out
        if num_med != 0: rate_ave_med = float(rate_ave_med) / num_med
        num = {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out,
               'rate_ave_med': rate_ave_med, 'num_med': num_med, 'num_med_up': num_med_up, 'num_med_down': num_med_down,'judge_today':a}
        return num


if __name__=='__main__':
    list=[5,1,3]
    list1=['','H','S']
    name=['北向','沪股通','深股通']

    judger = 'judger2'
    n = 1
    m = 1
    delta = 30
    delay = False
    frame = pandas.DataFrame(columns=['name','m', 'best_n', 'rate_ave_out', 'Judge_today'])
    for j,k,l in zip(list,list1,name):
        data = request_data(j,k)
        data1 = pandas.DataFrame(columns=['name','m', 'best_n', 'rate_ave_out', 'judge_today'])
        for i in range(1,11):
            b = a(data, delay,delta, i, m)
            e = b.get_statistic_info(judger,str(datetime.date(2000,2,8)-datetime.timedelta(days=delta)),data.loc[0]['交易日期'])
            data1.loc[len(data1.index)]=[l,m,i,e['rate_ave_out'],e['judge_today']]
        frame.loc[len(frame.index)] = data1.sort_values('rate_ave_out').head(1).values[0]
    print(frame)
