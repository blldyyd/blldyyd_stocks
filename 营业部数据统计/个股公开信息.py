import pandas,datetime


class a:
    def __init__(self,data,date,except_type,logic):
        '''
        方法体：
        ①cleandata为清理数据的函数
        ②yidong为要输出的时间和异动类型的函数
        '''
        self.data=data#为读取到的数据
        self.date=date#为查看异动的时间
        self.except_type=except_type#为查看异动的类型
        self.logic=logic
        self.detail_table=None#为比self.data多了列 '修改后代码'和'净买入金额(万元)'的新DataFrame
        self.cleandata()#执行清理数据函数

    def cleandata(self):
        pandas.set_option('mode.chained_assignment', None)#忽略报错
        self.data.dropna(inplace=True)#删除有空值的数据
        # 创建一个比self.data多了 '修改后代码'和'净买入金额'的列
        self.detail_table = self.data
        self.detail_table['修改后代码'] = self.data['代码'].apply(lambda x:x[-2:]+'SE.'+x[:-3])
        self.detail_table = self.detail_table[['代码', '修改后代码','名称','公告日期', '异动类型', '异动起始日',
                                               '异动截止日', '异动天数','期间成交量(万股)','期间成交额(万元)',
                                               '期间涨跌幅(%)','营业部买入金额(万元)', '营业部买入占比(%)', '营业部卖出金额(万元)',
                                               '营业部卖出占比(%)', '营业部交易金额(万元)','营业部交易占比(%)',
                                               '营业部净买入金额(万元)','营业部净买入占比(%)','证监会行业(2012)',
                                               '东财行业']]
        self.detail_table.reset_index(inplace=True,drop=True)

    def selcet_data(self):
        detail_table=self.detail_table[self.detail_table['公告日期']==self.date]
        detail_table.reset_index(inplace=True,drop=True)
        if self.except_type=='all':
            pass


        else:
            if self.logic=='not':
                for i in self.except_type:
                    detail_table.drop(detail_table[(detail_table['异动类型'] == i)].index.tolist(), inplace=True)

            elif self.logic=='and':
                temporary=pandas.DataFrame()
                for i in self.except_type:
                    temporary=temporary.append(detail_table[detail_table['异动类型'] == i])
                if len(self.except_type)==1:
                    detail_table=temporary
                else:
                    a = temporary.duplicated(subset='修改后代码', keep=False)
                    a = temporary.loc[a == True]
                    for i in a['修改后代码'].value_counts().index:
                        if a['修改后代码'].value_counts().loc[i]!=len(self.except_type):
                            a.drop(a[(a['修改后代码'] == i)].index.tolist(), inplace=True)
                    detail_table=a

            elif self.logic=='or':
                temporary=pandas.DataFrame()
                for i in self.except_type:
                    temporary=temporary.append(detail_table[detail_table['异动类型'] == i])
                detail_table=temporary

        simple_table = detail_table[['修改后代码','营业部净买入金额(万元)','公告日期']]
        simple_table = simple_table.drop_duplicates('修改后代码')
        detail_table.reset_index(drop=True, inplace=True)
        simple_table.reset_index(inplace=True, drop=True)
        return detail_table,simple_table


if __name__=='__main__':
    data=pandas.read_excel('个股交易公开信息.xls',header=1)
    data1=pandas.read_excel('个股交易公开信息.xls').columns

    data.columns=[data.columns[0],data.columns[1],data.columns[2],data.columns[3],data.columns[4],
                  data.columns[5],data.columns[6],data.columns[7],data.columns[8],data.columns[9],
                  data1[10][:-2]+data.columns[10],data1[10][:-2]+data.columns[11],data1[12][:-2]+data.columns[12][:-2],
                  data1[12][:-2]+data.columns[13][:-2],data1[14][:-2]+data.columns[14][:-2],data1[14][:-2]+data.columns[15][:-2],
                  data1[16][:-2]+data.columns[16][:-2],data1[16][:-2]+data.columns[17][:-2],data.columns[18],data.columns[19],
    ]
    #异动的所有类型
    yidonglist = ['当日涨幅偏离值达7%的证券',
'连续三个交易日内收盘价格涨幅偏离值累计20%',
'当日换手率达到20%的证券',
'当日跌幅偏离值达7%的证券',
'当日价格振幅达到15%的证券',
'日涨幅达到15%的前5只证券',
'有价格涨跌幅限制的日换手率达到30%的前五只证券',
'连续三个交易日内收盘价跌幅偏离值累计20%',
'有价格涨跌幅限制的连续3个交易日内收盘价格涨幅偏离值累计达到30%的证券',
'S、ST、*ST连续三个交易日内涨幅偏离值累计达到12%',
'无价格涨跌幅限制的证券',
'S、ST、*ST连续三个交易日内跌幅偏离值累计达到12%',
'有价格涨跌幅限制的日收盘价格跌幅达到15%的前五只证券',
'S、ST、*ST连续三个交易日内涨幅偏离值累计达到15%',
'S、ST、*ST连续三个交易日内跌幅偏离值累计达到15%',
'当日无价格涨跌幅限制的A股，出现异常波动停牌的股票',
'有价格涨跌幅限制的日价格振幅达到30%的前五只证券',
'有价格涨跌幅限制的连续3个交易日内收盘价格跌幅偏离值累计达到30%的证券',
'日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的证券',
'当日融资买入数量占该证券总交易量50%以上',
'当日收盘价涨幅达到20%的前5只股票',
'严重异常期间日收盘价格跌幅偏离值累计达到50%的证券',
'北交所股票最近3个有成交的交易日以内收盘价涨跌幅偏离值累计达到+40%(-40%)',
'退市整理的证券',
'严重异常期间日收盘价格涨幅偏离值累计达到100%的证券',
'当日收盘价跌幅达到-20%的前5只股票',
'严重异常期间日收盘价格跌幅偏离值累计达到70%的证券',
'严重异常期间3次出现正向异常波动的证券',
'当日融券卖出数量占当日该证券总交易量50%以上',
]

    date=str(datetime.date(2020,1,6))

    except_type=['当日换手率达到20%的证券']
    #except_type =[1,2,3,4,5,6]
    #except_type='all'
    logic='or'

    b=a(data,date,except_type,logic)#初始化这个类

    c,d=b.selcet_data()#执行查看异动的函数
    print(c.to_string())
    print(d)


