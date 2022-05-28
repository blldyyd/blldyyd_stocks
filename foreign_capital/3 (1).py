import pandas
import pandas as pd
import decimal,matplotlib
from os import walk


class a():
    def __init__(self, data,date, n, m):
        '''
        方法体
        ①clean_data
        ②return_num_in
        成员变量
        self.data是读取到的xls文件,DataFrame类型
        self.n过去n天流入，int类型
        self.m未来m天上涨，int类型
        '''
        self.data = data  # 读取的xls文件，dataframe类型
        self.n = n  # 过去n天流入，int类型
        self.m = m  # 未来m天上涨，int类型
        self.date=date
        self.clean_data()  # 清洗data数据

    def clean_data(self):
        '''
        作用是用来清洗data数据中的空值并删除
        '''
        self.data.dropna(subset=['外资持股数量变动(万股)',
                                 '涨跌幅(%)',
                                 '外资持股数量(万股)',
                                 '外资持股市值(万元)',
                                 '外资持股数量变动占当期成交比例(%)',
                                 '外资持股占全部A股比例(%)'], inplace=True)

        self.data.drop(self.data.index[self.data['交易日期'] >= self.date], inplace=True)
        self.data.index = [i for i in range(0, self.data.shape[0])]
        self.data['外资持股市值(万元)'] = self.data['外资持股市值(万元)'].str.replace(',', '').astype('str')
        self.data['外资持股数量(万股)'] = self.data['外资持股数量(万股)'].str.replace(',', '').astype('str')
        self.data['外资持股数量变动(万股)'] = self.data['外资持股数量变动(万股)'].str.replace(',', '').astype('str')

    def get_num(self, reference, delay=True, continuty=False):
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

        返回值：num
                'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out
        类型：dict

        '''
        num_in = 0
        num_out = 0
        num_in_up = 0
        num_in_down = 0
        num_out_up = 0
        num_out_down = 0
        rate_ave_in = 0
        rate_ave_out = 0

        if delay == True:
            delay_true = -1
            delay_Flase = 1
        else:
            delay_true = 0
            delay_Flase = 0

        for i in range(self.m, self.data.shape[0] - self.n + delay_true):
            in_int = 0
            judge_in = None
            in_up_int = 1

            if continuty == True:
                for j in range(i + delay_Flase, i + self.n + delay_Flase):
                    if (decimal.Decimal(self.data.loc[j, reference]) - \
                        decimal.Decimal(self.data.loc[j + 1, reference])) > 0:
                        in_int += 1
                if in_int == self.n:
                    judge_in = True
                else:
                    judge_in = False

            else:
                in_int = decimal.Decimal(self.data.loc[i + delay_Flase, reference]) - \
                         decimal.Decimal(self.data.loc[i + self.n + delay_Flase, reference])
                if in_int > 0:
                    judge_in = True
                else:
                    judge_in = False

            for j in range(self.m):
                in_up_int *= decimal.Decimal(1 + (self.data.loc[i - self.m + j, '涨跌幅(%)'] / 100))

            if judge_in:
                num_in += 1
                rate_ave_in += in_up_int - 1
                if in_up_int > 1:
                    num_in_up += 1
                else:
                    num_in_down += 1
            else:
                num_out += 1
                rate_ave_out += in_up_int - 1
                if in_up_int > 1:
                    num_out_up += 1
                else:
                    num_out_down += 1

        if num_in!=0:rate_ave_in = float(rate_ave_in / num_in) * 100
        if num_out!=0:rate_ave_out = float(rate_ave_out / num_out) * 100

        num = {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out}
        return num

    def get_num2(self, reference, delay=True, up_limit=0.05, down_limit=-0.05, continuty=False):
        '''
        变量
        num_in是后n天流入天数,int类型
        num_out是后n天流出的天数,int类型
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
        num_out = 0
        num_in_up = 0
        num_in_down = 0
        num_out_up = 0
        num_out_down = 0
        rate_ave_in = 0
        rate_ave_out = 0
        rate_ave_med = 0
        num_med = 0
        num_med_up = 0
        num_med_down = 0

        if delay == True:#表示用前一天的数据
            delay_true = -1
            delay_Flase = 1
        else:#表示不用前一天的数据
            delay_true = 0
            delay_Flase = 0

        for i in range(self.m, self.data.shape[0] - self.n + delay_true):
            in_int = 0
            judge_in = True
            in_up_int = 1
            for j in range(self.m):
                in_up_int *= decimal.Decimal(1 + (self.data.loc[i - self.m + j, '涨跌幅(%)'] / 100))

            if continuty == True:
                #print(i + delay_Flase, i + self.n + delay_Flase)
                for j in range(i + delay_Flase, i + self.n + delay_Flase):
                    if (decimal.Decimal(self.data.loc[j, reference]) - \
                        decimal.Decimal(self.data.loc[j + 1, reference])) > 0:
                        in_int += 1
                if in_int == self.n:
                    judge_in = True
                elif in_int != self.n and in_int > 0:
                    judge_in =None
                elif in_int ==0:
                    judge_in = False
            else:
                in_int = decimal.Decimal(self.data.loc[i + delay_Flase, reference]) / \
                         decimal.Decimal(self.data.loc[i + self.n + delay_Flase, reference])-1

                if in_int > up_limit:
                    judge_in = True
                elif in_int < down_limit:
                    judge_in = False
                else:
                    judge_in=None

            if judge_in:
                rate_ave_in += (in_up_int - 1)
                num_in += 1
                if in_up_int > 1:
                    num_in_up += 1
                else:
                    num_in_down += 1
            elif judge_in==None:
                rate_ave_med += (in_up_int - 1)
                num_med+=1
                if in_up_int > 1:
                    num_med_up += 1
                else:
                    num_med_down += 1
            else:
                rate_ave_out += (in_up_int - 1)
                num_out += 1
                if in_up_int > 1:
                    num_out_up += 1
                else:
                    num_out_down += 1
        if num_in!=0:rate_ave_in=float(rate_ave_in)/num_in
        if num_out!=0:rate_ave_out=float(rate_ave_out)/num_out
        if num_med!=0:rate_ave_med=float(rate_ave_med)/num_med

        num = {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out,
               'rate_ave_med': rate_ave_med, 'num_med': num_med, 'num_med_up': num_med_up, 'num_med_down': num_med_down
               }
        return num

    def cal_p(self, num):
        '''
        变量
        p_in外资流入的的概率
        p_out外资流出的的概率
        p_up_in在外资流入的情况下，上涨的概率
        p_down_in在外资流入的情况下，下跌的概率
        p_up_out在外资流出的情况下，上涨的概率
        p_down_out在外资流出的情况下，下跌的概率
        返回值:p_dict=
                {'p_in':p_in,
                'p_out':p_out,
                'p_up_in':p_up_in,
                'p_down_in':p_down_in,
                'p_up_out':p_up_out,
                'p_down_out':p_down_out}
        类型：dict

        '''
        p_in = num['num_in'] / (num['num_in'] + num['num_out'])
        p_out = num['num_out'] / (num['num_in'] + num['num_out'])
        p_up_in = num['num_in_up'] / num['num_in']
        p_down_in = num['num_in_down'] / num['num_in']
        p_up_out = num['num_out_up'] / num['num_out']
        p_down_out = num['num_out_down'] / num['num_out']
        p_dict = {'p_in': p_in,
                  'p_out': p_out,
                  'p_up_in': p_up_in,
                  'p_down_in': p_down_in,
                  'p_up_out': p_up_out,
                  'p_down_out': p_down_out}
        for i, j in p_dict.items():
            p_dict[i] = str(j * 100) + '%'
        return p_dict

    def n_finder(self,id,reference,delay=True,continuty=False):
        c=[]
        for i in range(1,31):
            self.n = i
            if id=='get_num':
                a=self.get_num(reference,delay,continuty)
                b=self.cal_p(a)
            elif id == 'get_num2':
                a=self.get_num2(reference,delay,continuty)
                b=self.cal_p(a)
            c.append([i,
               float(b['p_up_in'][:-1]),
               float(b['p_down_out'][:-1]),
               float(b['p_up_in'][:-1])+float(b['p_down_out'][:-1])])
        plot_table = pd.DataFrame(c, columns=['n', 'p_up_in', 'p_down_out', 'p_sum'])
        best_n=int(plot_table.sort_values('p_sum',ascending=False).head(1).values[0][0])
        return  plot_table,best_n

    def judge_today(self,id,best_n,reference,delay=False,continuty=False):
        self.n=best_n
        self.m=0
        if id == 'get_num':
            a = self.get_num(reference, delay, continuty)
        elif id == 'get_num2':
            a = self.get_num2(reference, delay, continuty)
        zts=a['num_in']+a['num_out']+a['num_med']
        judge_today_in='最好的n天流入的天数'+str(a['num_in'])+'天\n'+str(a['num_in']/zts*100)
        judge_today_out='\n最好的n天流出的天数'+str(a['num_out'])+'天\n'+str(a['num_out']/zts*100)
        judge_today_med='\n最好的n天中性的天数'+str(a['num_med'])+'天\n'+str(a['num_med']/zts*100)
        return judge_today_in+judge_today_out+judge_today_med


if __name__ == '__main__':
    header_names = ['交易日期', '收盘价(元)', '涨跌幅(%)', '外资持股市值(万元)',
                    '外资持股数量(万股)', '外资持股数量变动(万股)',
                    '外资持股数量变动占当期成交比例(%)', '外资持股占全部A股比例(%)',
                    '外资持股比例变动(%)', '外资成交金额']
    n = 4
    m = 3
    date = ''
    none = ["n/a", "na", "-"]  # 设置这三个值在DataFrame里都是空值
    data = pd.read_excel('000651.xls', na_values=none,parse_dates=['交易日期'])
    data.columns = header_names

    shili = a(data,date, n, m)  # 实例化一个类

    # 使用这个方法体算出外资流入流出的天数
    # 流入且上涨和下跌的天数，
    # 流出且上涨和下跌的天数,
    # 流入，流出情况下未来m天的平均收益值
    # b = shili.get_num(header_names[3])
    #print(b)

    #使用这个方法体算出外资连续n天前流入的天数
    #连续n天前流入且上涨和下跌的天数
    #连续n天前流出且上涨和下跌的天数,
    #流入大于0.05，流出小于-0.05情况下未来m天的平均收益值
    # c = shili.get_num2(header_names[3])
    #print(c)

    # d = shili.cal_p(b)
    #print(d)

    e,f=shili.n_finder('get_num',header_names[3])
    print(f)
    print(e)
    e.plot(x='n')

    matplotlib.pyplot.legend()
    matplotlib.pyplot.yticks([i for i in range(0,150,5)])
    matplotlib.pyplot.show()

    # g=shili.judge_today('get_num2',f,header_names[3])
    # print(g)