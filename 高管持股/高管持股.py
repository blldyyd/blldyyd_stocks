import time,pandas,matplotlib
from requests import get
from json import loads


headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
def requests_data(name):
    data=pandas.DataFrame(columns=['日期','代码','名称','变动人','变动股数','成交均价','变动金额',
                                   '变动原因','变动比例(‰)','变动后持股数','持股种类','董监高人员姓名',
                                   '职务','变动人与董监高的关系'])
    for i in range(1,3):
        time.sleep(1)
        url='https://datacenter-web.eastmoney.com/api/data/v1/get?callback=datatable7896333&reportName=RPT_EXECUTIVE_HOLD_DETAILS&columns=ALL&quoteColumns=&filter=(SECURITY_CODE="%s")&pageNumber=%d&pageSize=30&sortTypes=-1,1,1&sortColumns=CHANGE_DATE,SECURITY_CODE,PERSON_NAME&source=WEB&client=WEB&_=1652496732661'%(name,i)
        json_text=get(url,headers).text[17:-2]
        json_data=loads(json_text)
        for j in range(50):
            # print(json_data['result']['data'][j]['CHANGE_DATE'])
            # print(json_data['result']['data'][j]['DERIVE_SECURITY_CODE'])
            # print(json_data['result']['data'][j]['SECURITY_NAME'])
            # print(json_data['result']['data'][j]['PERSON_NAME'])
            # print(json_data['result']['data'][j]['CHANGE_SHARES'])
            # print(json_data['result']['data'][j]['AVERAGE_PRICE'])
            # print(json_data['result']['data'][j]['CHANGE_AMOUNT'])
            # print(json_data['result']['data'][j]['CHANGE_REASON'])
            # print(json_data['result']['data'][j]['CHANGE_RATIO'])
            # print(json_data['result']['data'][j]['CHANGE_AFTER_HOLDNUM'])
            # print(json_data['result']['data'][j]['HOLD_TYPE'])
            # print(json_data['result']['data'][j]['DSE_PERSON_NAME'])
            # print(json_data['result']['data'][j]['POSITION_NAME'])
            # print(json_data['result']['data'][j]['PERSON_DSE_RELATION'])
            # print()
            try:
                data.loc[len(data.index)]=[json_data['result']['data'][j]['CHANGE_DATE'] ,
                                           json_data['result']['data'][j]['DERIVE_SECURITY_CODE'],
                                           json_data['result']['data'][j]['SECURITY_NAME'],
                                           json_data['result']['data'][j]['PERSON_NAME'],
                                           json_data['result']['data'][j]['CHANGE_SHARES'],
                                           json_data['result']['data'][j]['AVERAGE_PRICE'],
                                           json_data['result']['data'][j]['CHANGE_AMOUNT'],
                                           json_data['result']['data'][j]['CHANGE_REASON'],
                                           json_data['result']['data'][j]['CHANGE_RATIO'],
                                           json_data['result']['data'][j]['CHANGE_AFTER_HOLDNUM'],
                                           json_data['result']['data'][j]['HOLD_TYPE'],
                                           json_data['result']['data'][j]['DSE_PERSON_NAME'],
                                           json_data['result']['data'][j]['POSITION_NAME'],
                                           json_data['result']['data'][j]['PERSON_DSE_RELATION']]
            except:
                break
    return data

class a:
    def __init__(self,data):
        self.data=data
        self.clean_data()

    def clean_data(self):
        self.data['日期']=self.data['日期'].apply(lambda x:x[:-9])
        self.data['变动金额']=self.data['变动金额'].astype('int')

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

    def select_data(self,start_date,end_date,method='减持',percentage=0,amount=20000000,logic='or'):
        start_date=self.type_conversion(start_date)
        end_date=self.type_conversion(end_date)
        start_index = None
        end_index = None

        try:
            start_index = self.data[self.data['日期'] >= start_date].tail(1).index[0]
            if self.data.loc[start_index, '日期'] > start_date:
                start_index += 1
        except:
            start_index = self.data.shape[0] - 1

        try:
            end_index = self.data[self.data['日期'] >= end_date].tail(1).index[0]
        except:
            end_index = self.data.shape[0] - self.data.shape[0]
        data = self.data[end_index:start_index]

        if method=='增持':
            data=data[data['变动股数'] >= 0]
        elif method=='减持':
            data =data[data['变动股数'] < 0]
            amount=-amount
        data.reset_index(drop=True, inplace=True)

        if logic=='and':
            for i in range(data.shape[0]):
                if data.loc[i,'变动比例(‰)'] >= percentage and data.loc[i,'变动金额'] < amount:
                    pass
                else:
                    data.drop(i,inplace=True)
        if logic=='or':
            for i in range(data.shape[0]):
                if data.loc[i,'变动比例(‰)'] >= percentage or data.loc[i,'变动金额'] < amount:
                    pass
                else:
                    data.drop(i,inplace=True)

        data.reset_index(drop=True, inplace=True)
        return data.copy()

    def get_table(self,data):
        try:
            data.loc[0,'日期']
        except:
            return 0,0

        seq=(str(i)+'d' for i in range(10,201,10))
        days10_dict={}
        days10_dict =days10_dict.fromkeys(seq)
        days10_dict1={}
        days10_dict1 =days10_dict.fromkeys(seq)

        days_dict={'1d':1, '2d':2, '3d':3, '4d':4, '5d':5, '6d':6, '7d':7, '8d':8, '9d':9, '10d':10}
        days_dict1= {'1d': 0, '2d': 0, '3d': 0, '4d': 0, '5d': 0, '6d': 0, '7d': 0, '8d': 0, '9d': 0, '10d': 0}

        for i in range(10,201,10):
            days10_dict[str(i)+'d']=i
            days10_dict1[str(i)+'d']=0


        data1=pandas.read_csv('300059.csv')
        data1['eob']=data1['eob'].apply(lambda x:x[:-15])
        frame=pandas.DataFrame(columns=[i for i in days_dict1])
        frame1 = pandas.DataFrame(columns=[i for i in days10_dict1])


        for i in range(data.shape[0]):
            for j in days_dict:
                try:
                    frame.loc[data.loc[i,'日期'],j]=data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0]+days_dict[j],'close']/data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]-1
                    days_dict1[j]+=data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0]+days_dict[j],'close']/data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]-1
                except:
                    frame.loc[data.loc[i, '日期'], j] ='未来数据不足'
        for i in range(data.shape[0]):
            for j in days10_dict:
                try:
                    frame1.loc[data.loc[i, '日期'], j] = data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0] +days10_dict[j], 'close']/ data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]  - 1
                    days10_dict1[j] += data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0] +days10_dict[j], 'close']/ data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]  - 1
                except:
                    frame1.loc[data.loc[i, '日期'], j] ='未来数据不足'


        frame.loc['平均收益率']=0
        frame1.loc['平均收益率'] = 0
        for i in days_dict1:
            aa = frame[i].value_counts()
            try:
                frame.loc['平均收益率',i] =days_dict1[i]/(len(frame.index)-1-aa.loc['未来数据不足'])
            except:
                frame.loc['平均收益率', i] = days_dict1[i] / (len(frame.index) - 1)
        for i in days10_dict1:
            try:
                aa=frame1[i].value_counts()
                frame1.loc['平均收益率',i] =days10_dict1[i]/(len(frame1.index)-1-aa.loc['未来数据不足'])
            except:
                frame1.loc['平均收益率', i] = days10_dict1[i] / (len(frame1.index) - 1)

        return frame,frame1

    def get_table_v2(self,data):
        try:
            data.loc[0,'日期']
        except:
            return 0,0
        seq=(str(i)+'d' for i in range(10,201,10))
        days10_dict={}
        days10_dict =days10_dict.fromkeys(seq)
        days10_dict1={}
        days10_dict1 =days10_dict.fromkeys(seq)

        days_dict={'1d':1, '2d':2, '3d':3, '4d':4, '5d':5, '6d':6, '7d':7, '8d':8, '9d':9, '10d':10}
        days_dict1= {'1d': 0, '2d': 0, '3d': 0, '4d': 0, '5d': 0, '6d': 0, '7d': 0, '8d': 0, '9d': 0, '10d': 0}

        for i in range(10,201,10):
            days10_dict[str(i)+'d']=i
            days10_dict1[str(i)+'d']=0


        data1=pandas.read_csv('300059.csv')
        data2=pandas.read_csv('HS300.csv')
        data1['eob']=data1['eob'].apply(lambda x:x[:-15])
        data2['eob'] = data2['eob'].apply(lambda x: x[:-15])
        frame=pandas.DataFrame(columns=[i for i in days_dict1])
        frame1 = pandas.DataFrame(columns=[i for i in days10_dict1])

        for i in range(data.shape[0]):
            for j in days_dict:
                try:
                    frame.loc[data.loc[i,'日期'],j]=(data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0]+days_dict[j],'close']/data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]-1)-\
                                                  (data2.loc[data2[data2['eob'] == data.loc[i, '日期']].index[0] + days_dict[j], 'close'] / data2[data2['eob'] == data.loc[i, '日期']]['close'].values[0] - 1)
                    days_dict1[j]+=(data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0]+days_dict[j],'close']/data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0]-1)-\
                                   (data2.loc[data2[data2['eob'] == data.loc[i, '日期']].index[0] + days_dict[j], 'close'] / data2[data2['eob'] == data.loc[i, '日期']]['close'].values[0] - 1)
                except:
                    frame.loc[data.loc[i, '日期'], j] ='未来数据不足'
        for i in range(data.shape[0]):
            for j in days10_dict:
                try:
                    frame1.loc[data.loc[i, '日期'], j] = (data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0] +days10_dict[j], 'close'] /data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0] - 1) - \
                    (data2.loc[data2[data2['eob'] == data.loc[i, '日期']].index[0] + days10_dict[j], 'close'] / data2[data2['eob'] == data.loc[i, '日期']]['close'].values[0] - 1)
                    days10_dict1[j] += (data1.loc[data1[data1['eob'] == data.loc[i, '日期']].index[0] + days10_dict[j], 'close'] / data1[data1['eob'] == data.loc[i, '日期']]['close'].values[0] - 1) - \
                                       (data2.loc[data2[data2['eob'] ==data.loc[i, '日期']].index[0] +days10_dict[j], 'close'] / data2[data2['eob'] ==data.loc[i, '日期']]['close'].values[0] - 1)
                except:
                    frame1.loc[data.loc[i, '日期'], j] ='未来数据不足'

        frame.loc['平均收益率']=0
        frame1.loc['平均收益率'] = 0
        for i in days_dict1:
            aa = frame[i].value_counts()
            try:
                frame.loc['平均收益率',i] =days_dict1[i]/(len(frame.index)-1-aa.loc['未来数据不足'])
            except:
                frame.loc['平均收益率', i] = days_dict1[i] / (len(frame.index) - 1)
        for i in days10_dict1:
            aa = frame1[i].value_counts()
            try:

                frame1.loc['平均收益率',i] =days10_dict1[i]/(len(frame1.index)-1-aa.loc['未来数据不足'])
            except:
                frame1.loc['平均收益率', i] = days10_dict1[i] / (len(frame1.index) - 1)

        return frame,frame1

if __name__=='__main__':
    name='600519'
    data=requests_data(name)
    # print(data)

    b=a(data)

    #输入两个时间获得这个时间段的数据
    c=b.select_data('2021-1-1','2022-5-16')
    # print(c)

    try:
        d,e=b.get_table(c)
        print(d.to_string())
        print(e.to_string())


        e.loc['平均收益率'].plot(kind="bar")

        matplotlib.pyplot.show()
        d.loc['平均收益率'].plot(kind="bar")
        matplotlib.pyplot.show()
    except:
        pass

    try:
        f,g=b.get_table_v2(c)
        # print(f.to_string())
        # print(g.to_string())
    except:
        pass
