import matplotlib.pyplot as plt
import os
import pandas as pd
import functools
import numpy as np
import matplotlib.colors as mcolors

bufferManagement = [
    # "AntBufferManagement",
                    "AntPlusBufferManagement",
                    "AntPlus2BufferManagement",
                    "BMBPBufferManagement",
                     "FifoBufferManagement",
                      # "HopsBufferManagement",
                      "TtlBufferManagement",
                      "RandomBufferManagement"]

markers = [',', 'o', '^', 'v', '<', '>', 'P', '+', 'D', '*']
linesType = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted']


def load_data(file_name):
    global MAX, MIN
    df = pd.read_csv(file_name, encoding='utf-8')
    # df.fillna(df.mean(), inplace=True)  # 填充空值
    idxs = df['AirId'].unique()
    files_name = []
    for idx in idxs:
        datas = df[df['AirId'].isin([idx])]
    return files_name


def sort_bufferSize(x, y):
    if int(x[0][:-1]) < int(y[0][:-1]):
        return -1
    if int(x[0][:-1]) > int(y[0][:-1]):
        return 1
    return 0

def sort_end_time(x, y):
    if int(x[0][:-1]) < int(y[0][:-1]):
        return -1
    if int(x[0][:-1]) > int(y[0][:-1]):
        return 1
    return 0

def load_datas(root_dir):
    datas = {}
    for bufferSizeDirs in os.listdir(root_dir):
        for endTimeDirs in os.listdir(root_dir + '/' + bufferSizeDirs):
            # if endTimeDirs == "7200":
                if bufferSizeDirs in datas.keys():
                    inDatas = datas[bufferSizeDirs]
                else:
                    inDatas = {}
                    datas[bufferSizeDirs] = inDatas

                for buffferManagementDirs in os.listdir(root_dir + '/' + bufferSizeDirs + '/' + endTimeDirs):
                    for fileName in os.listdir(root_dir + '/'
                                               + bufferSizeDirs + '/'
                                               + endTimeDirs + '/'
                                               + buffferManagementDirs):
                        fp = open(root_dir + '/'
                                  + bufferSizeDirs + '/'
                                  + endTimeDirs + '/'
                                  + buffferManagementDirs + '/'
                                  + fileName)
                        lines = fp.readlines()

                        if fileName == 'default_scenario_BufferAvgUtilityReport.txt':
                            value = float(lines[-2][-8:-1])
                            key = 'bufferUtilityRatioAvg'
                            if 'bufferUtilityRatioAvg' in inDatas.keys():
                                targetData = inDatas['bufferUtilityRatioAvg']
                            else:
                                targetData = {}
                                inDatas['bufferUtilityRatioAvg'] = targetData

                        if fileName == 'default_scenario_MessageDeliveryReport.txt':
                            value = float(lines[-2][-7:-1])
                            key = 'messageDelivery'
                            if 'messageDelivery' in inDatas.keys():
                                targetData = inDatas['messageDelivery']
                            else:
                                targetData = {}
                                inDatas['messageDelivery'] = targetData

                        if fileName == 'default_scenario_NetworkOverheadReport.txt':
                            value = float(lines[-1][-9:-1])
                            key = 'networkOverhead'
                            if 'networkOverhead' in inDatas.keys():
                                targetData = inDatas['networkOverhead']
                            else:
                                targetData = {}
                                inDatas['networkOverhead'] = targetData

                        if buffferManagementDirs in targetData.keys():
                            array = targetData[buffferManagementDirs]
                        else:
                            array = []
                            targetData[buffferManagementDirs] = array
                        array.append([endTimeDirs, value])

    for bufferSize in datas.keys():
        for target in datas[bufferSize].keys():
            for bufferManagement in datas[bufferSize][target].keys():
                array = datas[bufferSize][target][bufferManagement]
                array.sort(key=functools.cmp_to_key(sort_end_time))
                # x = datas[endTime][bufferManagement][0]
                # y_bufferUtilityRatioAvg = datas[endTime][bufferManagement][1]
                # y_messageDelivery = datas[endTime][bufferManagement][2]
                # y_networkOverhead = datas[endTime][bufferManagement][3]

    colors = list(mcolors.TABLEAU_COLORS.keys())

    result_y = {}

    for bufferSize in datas.keys():
        for target in datas[bufferSize].keys():
            print(bufferSize + " " + target)
            x = []
            for v in datas[bufferSize][target][list(datas[bufferSize][target].keys())[0]]:
                x.append(v[0])
            y = []
            for bufferManagement in datas[bufferSize][target].keys():
                array = []
                for v in datas[bufferSize][target][bufferManagement]:
                    array.append(v[1])
                y.append(array)
            x = np.array(x)
            y = np.array(y)
            x = x.astype('int')
            for i, strs in np.ndenumerate(x):
                x[i] /= 60
                # x[i] = str.replace("M", "")
                # x[i] = str.replace("k", "")
            x = x.astype('str')
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure()
            count = 0
            for index, bufferManagement in enumerate(datas[bufferSize][target].keys()):
                if (bufferManagement == "RandomBufferManagement" or bufferManagement == "BMBPBufferManagement" or
                        bufferManagement == "FifoBufferManagement" or bufferManagement == "TtlBufferManagement"):
                    BFName = bufferManagement
                    if BFName == "FifoBufferManagement":
                        BFName = "DF"
                    if BFName == "TtlBufferManagement":
                        BFName = "DO"
                    if BFName == "RandomBufferManagement":
                        BFName = "DR"
                    if BFName == "BMBPBufferManagement":
                        BFName = "CMBP"
                    count += 1

                    if target == "networkOverhead" or target == "Network Overhead":
                        result_y[BFName] = y[index]
                    if target == "messageDelivery":
                        target = "Delivery Ratio"
                        y_label = "Delivery Ratio(%)"
                        y *= 100
                    if target == "networkOverhead":
                        target = "Network Overhead"
                        y_label = "Network Overhead(hop)"
                    if target == "bufferUtilityRatioAvg":
                        target = "Buffer Utilization"
                        y_label = "Buffer Utilization(%)"
                    plt.plot(x, y[index],
                             color=mcolors.TABLEAU_COLORS[colors[index]],
                             label=BFName.replace("CacheManagement", ""),
                             ls=linesType[count],
                             marker=markers[count])
                    plt.ylabel(y_label)
                    # plt.xlabel('Transmit Speed/KBps')
                    plt.xlabel('End Time(minute)')
                    plt.legend()
            if not os.path.exists('./datas/' + bufferSize):
                os.mkdir('./datas/' + bufferSize)
            if not os.path.exists('./datas/' + bufferSize + '/' + target):
                os.mkdir('./datas/' + bufferSize + '/' + target)
            plt.savefig('./datas/' + bufferSize + '/' + target + '/result.jpg')

    # return datas

    # for index in result_y:
    #     if index != "BMBP":
    #         sum = 0
    #         for i, array in enumerate(result_y[index]):
    #                sum += array / result_y['BMBP'][i]
    #         sum /= 19
    #         sum = str(sum)
    #         print(index+":" + sum)

if __name__ == '__main__':
    load_datas("./reports_times")
