from pandas import DataFrame


def read_csv(address: str)->list[DataFrame]:
    from os import walk
    from pandas import read_csv
    for i, o, p in walk(address):  # 获取csv文件
        csv_names = [x for x in p if x[-4:] == '.csv']
        data = [read_csv(i + x) for x in csv_names]

        return data

def read_xlsx(address: str)->list[DataFrame]:
    from os import walk
    from pandas import read_excel
    for i, o, p in walk(address):  # 获取csv文件
        csv_names = [x for x in p if x[-4:] == '.xls' or x[-5:] == '.xlsx']
        data = [read_excel(i + x) for x in csv_names]
        
        return data

