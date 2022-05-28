import pandas,datetime


class a():
    def __init__(self,market,small_disc,n):
        self.market=market
        self.small_disc=small_disc
        self.n=n
        self.time_list=None
        self.clean_data()

    def clean_data(self):
        self.market['eob']=self.market['eob'].apply(lambda x:x[:-15])
        self.small_disc['eob'] = self.small_disc['eob'].apply(lambda x: x[:-15])
        self.time_list=self.market['eob']

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

    def rotation_of_index(self, date):
        start_date=self.type_conversion(date)

        start_index=None
        end_index=None

        try:
            end_index=self.time_list[self.time_list.values>=start_date].head(1).index[0]
        except:
            end_index=self.time_list.shape[0]-1
        if end_index-self.n<0:
            return '过去天数不足'
        if self.time_list[end_index]>start_date:
            end_index-=1


        x=self.market.loc[end_index,'close']/self.market.loc[end_index-self.n,'close']-1
        y = self.small_disc.loc[end_index,'close'] / self.small_disc.loc[end_index-self.n,'close'] - 1

        if x<0 and y<0:
            return '下日空仓'
        else:
            if x>y:
                return '下日持有大盘'
            else:
                return '下日持有小盘'


if __name__=='__main__':
    n=3
    market=pandas.read_csv('HS300.csv')
    small_disc=pandas.read_csv('ZZ1000.csv')
    b=a(market,small_disc,n)

    #输入一个日期判断那天是空仓还是大盘或者小盘
    c=b.rotation_of_index('2022-5-10')
    print(c)