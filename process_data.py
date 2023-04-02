import pandas as pd
import os
from datetime import timedelta
import datetime
import math


def get_avg(root_dir):
    sum = [0, 0, 0]
    n = 0
    for dirPath, dirnames, filenames in os.walk(root_dir):
        for file_name in filenames:
            df = pd.read_csv(root_dir + '/' + file_name, encoding='utf-8')
            sum[0] += df['x'].sum()
            sum[1] += df['y'].sum()
            sum[2] += df['z'].sum()
            n += len(df)
    return sum[0] / n, sum[1] / n, sum[2] / n


def get_std(root_dir, avg):
    sum = [0, 0, 0]
    n = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file_name in filenames:
            df = pd.read_csv(root_dir + '/' + file_name, encoding='utf-8')
            sum[0] += ((df['x'] - avg[0]) ** 2).sum()
            sum[1] += ((df['y'] - avg[1]) ** 2).sum()
            sum[2] += ((df['z'] - avg[2]) ** 2).sum()
            n += len(df)
    return math.sqrt(sum[0] / (n - 1)), math.sqrt(sum[1] / (n - 1)), math.sqrt(sum[2] / (n - 1))


def standardization_data(root_dir):
    avg_x, avg_y, avg_z = get_avg(root_dir)
    avg = [avg_x, avg_y, avg_z]
    std_x, std_y, std_z = get_std(root_dir, avg)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file_name in filenames:
            df = pd.read_csv(root_dir + '/' + file_name, encoding='utf-8')
            df['x'] = (df['x'] - avg_x) / std_x
            df['y'] = (df['y'] - avg_y) / std_y
            df['z'] = (df['z'] - avg_z) / std_z
            df.to_csv(root_dir.replace("standard_data", "test_data") + file_name, index=False, sep=',')
    file = open(root_dir.replace("standard_data/", "") + "std_avg_test.txt", 'w')
    file.write(str(avg_x) + ',' + str(avg_y) + ',' + str(avg_z) +
               ',' + str(std_x) + ',' + str(std_y) + ',' + str(std_z))
    file.close()


def process_data2(root_dir, datas, idx):
    datas.columns = ['date', 'nanosecond', 'AirId', 'x', 'y', 'z']
    file_num = int(datas.size / 6 / 20000)
    print(str(idx) + "文件,记录数:" + str(datas.size / 6) + "，将拆分为" + str(file_num + 1) + "个文件")
    for index, line in datas.iterrows():
        print("\r", '正在处理第{}/{}条记录...'.format(index + 1, int(datas.size / 6)), end="", flush=True)
        time = datetime.datetime.strptime(line['date'], "%Y-%m-%d %H:%M:%S")
        time = time + timedelta(microseconds=int(line['nanosecond']) / 1000)
        datas['date'][index] = time
    datas.drop('nanosecond', axis=1, inplace=True)
    for i in range(0, file_num + 1):
        print("生成" + str(idx) + "_" + str(i) + ".csv文件")
        datas.iloc[i * 20000: (i + 1) * 20000].to_csv(root_dir.replace("processed_data", "sorted_data")
                                                      + str(idx)
                                                      + "_" + str(i)
                                                      + ".csv",
                                                      index=False, sep=',')


def process_data1(root_dir, datas, idx):
    datas.to_csv(root_dir.replace("raw_data", "processed_data") + idx + ".csv", index=False, sep=',')


def load_data(root_dir, file_name):
    global MAX, MIN
    df = pd.read_csv(root_dir + '/' + file_name, encoding='utf-8')
    # df.fillna(df.mean(), inplace=True)  # 填充空值
    idxs = df['AirId'].unique()
    files_name = []
    for idx in idxs:
        datas = df[df['AirId'].isin([idx])]
        files_name.append(process_data2(root_dir, datas, idx))
    return files_name


def load_datas(root_dir):
    datas = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            df = load_data(root_dir, filename)
            datas.append(df)
    return datas


if __name__ == "__main__":
    standardization_data("../ChengDuAirAll/standard_data/")
    # print(load_datas("../ChengDuAirAll/processed_data/"))
    # print(load_datas("../ChengDuAirAll/raw_data/"))
