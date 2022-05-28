import pandas
from sys import path
path.append('../')
import reuse


class stocks_info:
    def __init__(self,price:str,stock_code:str,address:str,file_type:str):
        '''
        参数
        price，表中价格的表头名称
        stock_code，表中代码名称的表头名称
        address，表所在的文件夹的位置
        file_type，要读取表的类型，是csv或者xlsx|xls
        方法体
        1、get_single_day()获取n天前到现在的收益率
        2、get_many_day()获取1,2,3····10天前到现在的收益率
        3、st_ceiling_price_yd()获取历史最高价和最低价和所在的日期和价格，
        获取历史最高价和最低价到现在的收益率

        成员变量
        self.data，是从若干的csv文件中读取的
        self.price，是文件中收盘价的表头名称
        self.stock_code，是文件中股票代码的表头名称

        注意！！！
        所读到的csv文件中的时间，头部是现在时间，尾部是过去时间，如果不是就会计算出错
        '''
        self.data=None
        self.price=price
        self.stock_code=stock_code

        if file_type=='csv':
            self.data=reuse.reuse.read_csv(address)
        elif file_type=='xlsx' or file_type=='xls':
            self.data=reuse.reuse.read_xlsx(address)

    def get_single_day(self, day:int)-> pandas.DataFrame:
        '''
        参数
        day，为用于计算day天前到现在的收益率
        返回值：frame，每个股票day天前到现在收益率的一张表
        '''
        frame = pandas.DataFrame(columns=['%s天前到现在收益率' % day])
        for i in self.data:
            profit = i.loc[0, self.price] / \
                          i.loc[0 + day, self.price] - 1
            frame.loc[i.loc[0, self.stock_code]] = ['%.6f'%profit]#保留小数后6位
        return frame

    def get_many_day(self,days:list[int])->pandas.DataFrame:
        '''
        参数
        days为计算某天前收益率的列表，循环调用self.get_single_table来合并成一张表
        返回值：single_table，每个股票的每一个天数到现在的收益率的一张表
        '''
        frame = pandas.DataFrame()
        for i in days:
            frame1 = self.get_single_day(i)
            frame = pandas.concat([frame, frame1], axis=1)
        return frame

    def cg_and_fr_price(self)->pandas.DataFrame:
        frame=pandas.DataFrame(columns=['历史最高价时间','历史最高价格','历史最高价到现在的收益值','历史最低价时间','历史最低价','历史最低价到现在的收益值'])
        for i in self.data:
            max_price=max(i[self.price])
            min_price=min(i[self.price])
            max_data=i[i[self.price]==max_price]
            min_data = i[i[self.price] == min_price]
            profit_rate = str((i.loc[0, self.price] / max_price - 1)*100)[0:6].split('.')[0]+'%'
            profit_rate1 = str((i.loc[0, self.price] / min_price - 1)*100).split('.')[0]+'%'
            frame.loc[i.loc[max_data.index[0],self.stock_code]]=[i.loc[max_data.index[0],'eob'],
                            i.loc[max_data.index[0],self.price],
                            profit_rate ,
                            i.loc[min_data.index[0], 'eob'],
                            i.loc[min_data.index[0], self.price],
                            profit_rate1]
        return frame


if __name__=='__main__':
    #表中收盘价的表头名称
    price= 'close'
    #表中股票代码的表头名称
    stock_code='symbol'
    #如果文件后缀是xlsx就改变file_type变量
    file_type='csv'
    #读取文件的地址
    address = './'

    #实例化一个对象
    a=stocks_info(price,stock_code,address,file_type)

    #调用后返回5,7···240天前到现在的收益率，一个Dataframe对象
    required_days = [1, 5, 10, 20, 30, 60, 120, 240]
    c=a.get_many_day(required_days)
    print(c.to_string())

    # 调用后返回每个股票的历史最高价和时间，一个Dataframe对象
    h=a.cg_and_fr_price()
    print(h.to_string())
