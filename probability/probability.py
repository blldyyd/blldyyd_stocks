import pandas
import decimal
from sys import path
path.append('../')
import reuse


class a:
    def __init__(self,quantity:str,income:int,n:int,m:int):
        '''
        参数
        quantity为文件中持股数量的表头名称
        income为文件中涨跌幅的表头名称
        file_address文件夹地址或者名称
        n表示过去多少天，用'持股数量'计算增持还是减持
        m表示未来多少天，用’涨跌幅‘于计算未来上涨和下跌
        方法体
        ①clean_data()清洗数据的函数
        ②get_num()获得增持减持 和增持减持且未来上涨下跌的天数
        '''
        self.data=pandas.read_excel('000651.xls', na_values = ["n/a", "na", "-"])
        self.quantity=quantity
        self.income=income

        self.n=n#
        self.m=m#
        self.clean_data()#清洗data数据

    def clean_data(self):
        self.data.dropna(inplace = True)#删除包含空值的那一行
        self.data.reset_index(inplace=True,drop=True)#重新设置索引值

        #替换掉外国计数中的','号
        self.data[self.data.columns[3]]=self.data[self.data.columns[3]].str.replace(',','').astype('str')
        self.data[self.data.columns[4]]=self.data[self.data.columns[4]].str.replace(',', '').astype('str')

    def get_num(self,delay:bool=True,continuty:bool=False)->pandas.DataFrame:
        '''
        变量
        num_in是过去流入天数
        num_out是过去流出天数
        num_in_up流入且未来m天上涨天数
        num_in_down流入且未来m天下跌天数
        num_out_up流出且未来m天上涨天数
        num_out_down流出且未来m天下跌天数

        返回值:num
        '''
        num_in = 0
        num_out = 0
        num_in_up = 0
        num_in_down = 0
        num_out_up = 0
        num_out_down = 0
        rate_ave_in = 0
        rate_ave_out = 0
        frame=pandas.DataFrame(columns=['流入天数','流入概率','流出天数','流出概率',
                                        '流入且上涨天数','流入且上涨概率',
                                        '流入且下跌天数', '流入且下跌概率',
                                        '流出且上涨天数', '流出且上涨概率',
                                        '流出且下跌天数', '流出且下跌概率'])
        if delay:
            delay_true = -1
            delay_Flase = 1
        else:
            delay_true = 0
            delay_Flase = 0

        for i in range(self.m, self.data.shape[0] - self.n + delay_true):
            in_int = 0
            judge_in = None
            in_up_int = 1
            for j in range(self.m):
                in_up_int *= decimal.Decimal(1 + (self.data.loc[i - self.m + j, self.income] / 100))

            if continuty == True:
                in_int = decimal.Decimal(self.data.loc[i + delay_Flase, self.quantity]) - \
                         decimal.Decimal(self.data.loc[i + self.n + delay_Flase, self.quantity])
                if in_int >= 0:
                    judge_in = True

            else:
                for j in range(i + delay_Flase, i + self.n + delay_Flase):
                    if (decimal.Decimal(self.data.loc[j, self.quantity]) - \
                        decimal.Decimal(self.data.loc[j + 1, self.quantity])) >= 0:
                        in_int += 1
                if in_int == self.n:
                    judge_in = True

            if judge_in == True:
                num_in += 1
                rate_ave_in += in_up_int - 1
                if in_up_int >= 1:
                    num_in_up += 1
                else:
                    num_in_down += 1
            else:
                num_out += 1
                rate_ave_out += in_up_int - 1
                if in_up_int >= 1:
                    num_out_up += 1
                else:
                    num_out_down += 1

        rate_ave_in = float(rate_ave_in / num_in) * 100
        rate_ave_out = float(rate_ave_out / num_out) * 100

        num = {'num_in': num_in, 'num_out': num_out,
               'num_in_up': num_in_up, 'num_in_down': num_in_down,
               'num_out_up': num_out_up, 'num_out_down': num_out_down,
               'rate_ave_in': rate_ave_in, 'rate_ave_out': rate_ave_out}
        p_in=num['num_in']/(num['num_in']+num['num_out'])*100
        p_up_in=num['num_in_up']/num['num_in']*100
        p_up_out=num['num_out_up']/num['num_out']*100
        p_dict={'p_in':'%.2f'%p_in,
                'p_out':'%.2f'%(100-p_in),
                'p_up_in':'%.2f'%p_up_in,
                'p_down_in':'%.2f'%(100-p_up_in),
                'p_up_out':'%.2f'%p_up_out,
                'p_down_out':'%.2f'%(100-p_up_out)}

        # print('外资流入了总共%d天,概率百分之%s' % (num['num_in'],p_dict['p_in']))
        # print('外资流出了总共%d天,概率百分之%s' % (num['num_out'],p_dict['p_out']))
        # print('外资流入了且上涨总共%d天,概率百分之%s' % (num['num_in_up'],p_dict['p_up_in']))
        # print('外资流入了且未来下跌总共%d天,概率百分之%s' % (num['num_in_down'],p_dict['p_down_in']))
        # print('外资流出了且未来上涨总共%d天,概率百分之%s' % (num['num_out_up'],p_dict['p_up_out']))
        # print('外资流出了且未来下跌总共%d天,概率百分之%s' % (num['num_out_down'],p_dict['p_down_out']))
        frame.loc[len(frame.index)]=[num['num_in'],p_dict['p_in'],
                                     num['num_out'], p_dict['p_out'],
                                     num['num_in_up'], p_dict['p_up_in'],
                                     num['num_in_down'], p_dict['p_down_in'],
                                     num['num_out_up'], p_dict['p_up_out'],
                                     num['num_out_down'], p_dict['p_down_out']
                                    ]
        return frame


if __name__=='__main__':
    #n表示计算n天前到现在的收益率
    n=4

    #m表示计算未来m天后到现在的收益率
    m=3

    #delay表示如果为True就计算n+1天前，为False表示n不加1

    #quantity为文件中持股数量的表头名称
    quantity='深股通持股数量(万股)'

    #income为文件中涨跌幅的表头名称
    income='涨跌幅(%)'

    #file_address为文件存储地址
    #file_address='C:/Users/blldyyd/Desktop/工作/外资'

    shili=a(quantity,income,n,m)#实例化一个类

    #使用后获取外资持股数量的基本数据，增持减持，未来的上涨和下跌天数
    b=shili.get_num(True,True)
    print(b.to_string())
