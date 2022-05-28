import pandas,datetime,time,numpy


spring_festival = {'1991': '2-15', '1992': '2-4', '1993': '1-23', '1994': '2-10', '1995': '1-31',
                   '1996': '2-19', '1997': '2-7', '1998': '1-28', '1999': '2-16', '2000': '2-5',
                   '2001': '1-24', '2002': '2-12', '2003': '2-1', '2004': '1-22', '2005': '2-9',
                   '2006': '1-29', '2007': '2-18', '2008': '2-7', '2009': '1-26', '2010': '2-14',
                   '2011': '2-3', '2012': '1-23', '2013': '2-10', '2014': '1-31', '2015': '2-19',
                   '2016': '2-8', '2017': '1-28', '2018': '2-16', '2019': '2-5', '2020': '1-25',
                   '2021': '2-12', '2022': '2-1'}

week_enumeration = {
    1: '周一',
    2: '周二',
    3: '周三',
    4: '周四',
    5: '周五'}



class a:
    def __init__(self,data):
        self.data=data
        self.time_list = None
        self.clean_data()


    def clean_data(self):
        self.data['eob']=self.data['eob'].apply(lambda x:x[:-15])
        self.data['weekday'] = self.data['eob'].apply(lambda x: time.strptime(x,'%Y-%m-%d').tm_wday+1)
        self.data['weekday']=self.data['weekday'].apply(lambda x: week_enumeration[x])
        self.time_list = self.data['eob']

    def type_conversion(self,date):
        date=str(date)
        if len(date) > 11:
            date = date.split(' ')[0]
        if len(date) == 8:
            date = date[0:4] + '-0' + date[5] + '-0' + date[7]
        if len(date) == 9:
            if date[5:7]=='11' or date[5:7]=='12'or date[5:7]=='10':
                date = date[0:4] + '-' + date[5:7] + '-0' + date[8]
            else:
                date = date[0:4] + '-0' + date[5] + '-' + date[7:9]

        return date

    def judge_date(self,date):
        date=self.type_conversion(date)
        try:
            weekday = self.data[self.data['eob'] == date]['weekday'].values[0]
            return weekday
        except:
            return '输入的日期不存在'

    def select_data(self,start_date,end_date,judge=False):
        start_date=self.type_conversion(start_date)
        end_date=self.type_conversion(end_date)
        start_index=None
        end_index=None


        start_index=self.time_list[self.time_list.values>=start_date].head(1).index[0]
        if judge==True:
            start_index -= 1
        try:
            end_index=self.time_list[self.time_list.values>=end_date].head(1).index[0]
            if self.time_list[end_index] > end_date:
                end_index -= 1
        except:
            end_index = self.time_list.shape[0] - 1

        data=self.data.loc[start_index:end_index]
        data.reset_index(inplace=True,drop=True)
        return data

    def week_research(self,start_date,end_date):
        data=self.select_data(start_date,end_date)
        week_yield={'周一':0,
        '周二':0,
        '周三':0,
        '周四':0,
        '周五':0}
        data1=pandas.DataFrame([[0 for i in range(1,6)]for j in range(1,6)],
                               index=['上涨天数','下跌天数','上涨概率','下跌概率','平均收益率'],
                               columns=['周一','周二','周三','周四','周五'])
        up_or_down=0

        for i in range(data.shape[0]-1):
            up_or_down=data.loc[i+1, 'close']/data.loc[i, 'close']-1

            if up_or_down>=0:

                week_yield[data.loc[i+1,'weekday']]+=up_or_down
                data1.loc['上涨天数',data.loc[i+1,'weekday']]+=1

            elif up_or_down<0:

                week_yield[data.loc[i+1,'weekday']]+=up_or_down
                data1.loc['下跌天数',data.loc[i+1,'weekday']]+=1

        for i in data1.columns:
            data1.loc['上涨概率',i]=data1.loc['上涨天数',i]/(data1.loc['上涨天数',i]+data1.loc['下跌天数',i])
            data1.loc['下跌概率',i]=1-data1.loc['上涨天数',i]/(data1.loc['上涨天数',i]+data1.loc['下跌天数',i])
            data1.loc['平均收益率',i] = week_yield[i]/(data1.loc['上涨天数',i]+data1.loc['下跌天数',i])

        temporary1=data1.loc['上涨概率'].reset_index()
        temporary1.sort_values(by='上涨概率',inplace=True,ascending=False)
        temporary2 = data1.loc['下跌概率'].reset_index()
        temporary2.sort_values(by='下跌概率', inplace=True,ascending=False)
        temporary3 = data1.loc['平均收益率'].reset_index()
        temporary3.sort_values(by='平均收益率', inplace=True,ascending=False)

        best_day={'概率':temporary1.head(1)['index'].values[0],'平均收益率':temporary3.head(1)['index'].values[0]}
        worst_day={'概率':temporary2.head(1)['index'].values[0],'平均收益率':temporary3.tail(1)['index'].values[0]}

        return data1,best_day,worst_day

    def month_research(self,start_date,end_date,judge=False):
        month = {'1月': 0, '2月': 0, '3月': 0, '4月': 0, '5月': 0, '6月': 0,
                 '7月': 0, '8月': 0, '9月': 0, '10月': 0, '11月': 0, '12月': 0, }

        month_enumeration = {'01': '1月', '02': '2月', '03': '3月', '04': '4月', '05': '5月', '06': '6月',
                             '07': '7月', '08': '8月', '09': '9月', '10': '10月', '11': '11月', '12': '12月', }

        data=self.select_data(start_date,end_date,judge)

        data['eob']=data['eob'].apply(lambda x:x[:-3])
        data.drop_duplicates('eob',keep='last',inplace=True,ignore_index=True)
        data1=pandas.DataFrame([[0 for i in range(1,13)]for j in range(1,6)],
                               index=['上涨月数','下跌月数','上涨概率','下跌概率','平均收益率'],
                               columns=[str(i)+'月' for i in range(1,13)])

        for i in range(1,data.shape[0]):
            #print(data.loc[i,'eob'],data.loc[i-1,'eob'])

            up_or_down=data.loc[i,'close']/data.loc[i-1,'close']-1
            if up_or_down>0:
                data1.loc['上涨月数',month_enumeration[data.loc[i,'eob'][5:]]]+=1
                month[month_enumeration[data.loc[i,'eob'][5:]]]+=up_or_down

            elif up_or_down<0:
                data1.loc['下跌月数', month_enumeration[data.loc[i, 'eob'][5:]]] += 1

                month[month_enumeration[data.loc[i, 'eob'][5:]]] += up_or_down
            #print(month_enumeration[data.loc[i, 'eob'][5:]])
        for i in month_enumeration:
            #print(i)
            data1.loc['上涨概率',month_enumeration[i]]=data1.loc['上涨月数',month_enumeration[i]]/(data1.loc['上涨月数',month_enumeration[i]]+data1.loc['下跌月数',month_enumeration[i]])
            data1.loc['下跌概率', month_enumeration[i]] = 1-data1.loc['上涨月数', month_enumeration[i]] / (
                        data1.loc['上涨月数', month_enumeration[i]] + data1.loc['下跌月数', month_enumeration[i]])
            data1.loc['平均收益率', month_enumeration[i]] = month[month_enumeration[i]]/ (
                        data1.loc['上涨月数', month_enumeration[i]] + data1.loc['下跌月数', month_enumeration[i]])

        temporary1=data1.loc['上涨概率'].reset_index()
        temporary1.sort_values(by='上涨概率',inplace=True,ascending=False)

        temporary2 = data1.loc['下跌概率'].reset_index()
        temporary2.sort_values(by='下跌概率', inplace=True,ascending=False)

        temporary3 = data1.loc['平均收益率'].reset_index()
        temporary3.sort_values(by='平均收益率', inplace=True,ascending=False)

        best_month={'概率':temporary1.head(1)['index'].values[0],'平均收益率':temporary3.head(1)['index'].values[0]}
        worst_month={'概率':temporary2.head(1)['index'].values[0],'平均收益率':temporary3.tail(1)['index'].values[0]}

        return data1,best_month,worst_month

    def best_week(self,start_date,end_date):
        data1=pandas.DataFrame(columns=['最好概率','最好涨幅','最差概率','最差涨幅'])

        for i in range((int(end_date)-int(start_date)+1)):
            data,best_week,worst_week=self.week_research(start_date+'-1-1',
                                                          str(int(start_date)+1)+'-12-31')
            data1.loc[start_date]=[best_week['概率'],best_week['平均收益率'],
                                          worst_week['概率'],worst_week['平均收益率']]
            start_date=str(int(start_date)+1)
        a=self.data[self.data['weekday']=='周三']

        return data1

    def five_y_best_month(self,start_date,end_date):
        data1=pandas.DataFrame(columns=['最好概率','最好涨幅','最差概率','最差涨幅'])

        for i in range(int((int(end_date)-int(start_date)+1)/5)):
            data,best_month,worst_month=self.month_research(str(int(start_date)-1)+'-12-20',
                                                          str(int(start_date)+4)+'-12-31')
            data1.loc[start_date+'-'+str(int(start_date)+4)]=[best_month['概率'],best_month['平均收益率'],
                                          worst_month['概率'],worst_month['平均收益率']]
            #print(str(int(start_date)-1)+'-12-20',str(int(start_date)+4)+'-12-31')
            start_date=str(int(start_date)+5)

        return data1

    def year_bs_month(self,start_date,end_date,judge=True):

        data1 = pandas.DataFrame(columns=['春节日期（大年初一）', '涨幅最好月份', '涨幅最差月份'])

        for i in range(int(end_date)-int(start_date)+1):
            print(str(int(start_date)-1)+'-12-31',start_date+'-12-31')
            data,best_month,worst_month=self.month_research(str(int(start_date)-1)+'-12-31',
                                                          start_date+'-12-31',judge)

            data1.loc[start_date]=[spring_festival[start_date],best_month['平均收益率'],
                                          worst_month['平均收益率']]
            #print(str(int(start_date)-1)+'-12-31',start_date+'-12-31')
            start_date=str(int (start_date)+1)

        return data1

    def spring_festival_research(self,start_date,end_date):
        start_date=str(start_date)
        end_date=str(end_date)
        data1 = pandas.DataFrame(columns=['春节日期（大年初一）', '节前最后交易日', 'day1', 'day2', 'day3', 'day4', 'day5'])

        for i in range(int(end_date)-int(start_date)+1):
            profit = []
            _date = self.type_conversion(start_date +'-'+ spring_festival[start_date])
            index = self.time_list[self.time_list.values >= _date].head(1).index[0] - 1

            for i in range(1,6):
                profit.append(self.data.loc[index,'close']/self.data.loc[index-i,'close']-1)

            data1.loc[start_date]=[start_date+'-'+spring_festival[start_date],self.data.loc[index,'eob'],
                                   profit[0],profit[1],profit[2],profit[3],profit[4]]

            start_date=str(int(start_date)+1)

        return data1


if __name__=='__main__':
    data=pandas.read_csv('000001.csv')

    b=a(data)

    #传入一个时间获得该时间是星期几
    # c=b.judge_date('2022-2-16')
    # print(c)

    #传入两个时间，第一个时间是开始时间，第二个是结束时间，截取这个时间段的数据
    # d=b.select_data('1991-1-1','1991-1-19')
    # print(d.to_string())

    #传入两个时间，第一个时间是开始时间，第二个是结束时间，获取这个时间段周一到周五的上涨和下跌天数
    #并计算概率和平均收益率
    # e,f,g=b.week_research('1991-1-1','1991-12-31')
    # print(e)
    # print(f)
    # print(g)

    #传入两个时间和一个布偶值，第一个时间是开始时间，第二个是结束时间，第三个布偶值表示计算月份的时候找到前一年12月份最后一天
    # 计算某一年到某一年的所有月份上涨和下跌概率和平均收益率
    #注意！！！如果时间段是1年，那么上涨概率就要么是1或者是0所以排序数据并不可以参考
    #注意！！！第一个参数必须是前一年的12-31号，不然1月的收益率会无法计算
    h,i,j=b.month_research('2017-12-31','2018-12-31',True)
    print(h.to_string())
    print(i)
    print(j)

    #输入两个时间，第一个时间是开始时间的年份，第二个是结束时间的年份
    #获取每一年最好和最差的概率和涨跌幅是星期几
    # k=b.best_week('2010','2020')
    # print(k)

    #输入两个时间，第一个时间是开始时间的年份，第二个是结束时间的年份
    #获取四年时间最好和最差的概率和涨跌幅的月份
    # l=b.five_y_best_month('1991','2020')
    # print(l)

    #输入两个时间，第一个时间是开始时间的年份，第二个是结束时间的年份
    #获取每一年的涨跌幅最好和最差的月份
    # m=b.year_bs_month('1991','2020')
    # print(m)

    #输入两个时间，第一个时间是开始时间的年份，第二个是结束时间的年份
    #获取每一年的春节前最后一天交易日之前1天，2天，3天，4天，5天的各天的收益率
    # n=b.spring_festival_research('1991','2020')
    # print(n)