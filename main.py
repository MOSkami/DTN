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
                    "AntPlus3BufferManagement",
                     "FifoBufferManagement",
                      "HopsBufferManagement",
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


def load_datas(root_dir):
    datas = {}
    for bufferSizeDirs in os.listdir(root_dir):
        for endTimeDirs in os.listdir(root_dir + '/' + bufferSizeDirs):
            if endTimeDirs == "7200":
                if endTimeDirs in datas.keys():
                    inDatas = datas[endTimeDirs]
                else:
                    inDatas = {}
                    datas[endTimeDirs] = inDatas

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
                        array.append([bufferSizeDirs, value])

    for endTime in datas.keys():
        for target in datas[endTime].keys():
            for bufferManagement in datas[endTime][target].keys():
                array = datas[endTime][target][bufferManagement]
                array.sort(key=functools.cmp_to_key(sort_bufferSize))
                # x = datas[endTime][bufferManagement][0]
                # y_bufferUtilityRatioAvg = datas[endTime][bufferManagement][1]
                # y_messageDelivery = datas[endTime][bufferManagement][2]
                # y_networkOverhead = datas[endTime][bufferManagement][3]

    colors = list(mcolors.TABLEAU_COLORS.keys())

    result_y = {}

    for endTime in datas.keys():
        for target in datas[endTime].keys():
            print(endTime + " " + target)
            x = []
            for v in datas[endTime][target][list(datas[endTime][target].keys())[0]]:
                x.append(v[0])
            y = []
            for bufferManagement in datas[endTime][target].keys():
                array = []
                for v in datas[endTime][target][bufferManagement]:
                    array.append(v[1])
                y.append(array)
            x = np.array(x)
            y = np.array(y)
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure()
            count = 0
            for index, bufferManagement in enumerate(datas[endTime][target].keys()):
                if (bufferManagement == "RandomBufferManagement" or bufferManagement == "AntPlus3BufferManagement" or
                        bufferManagement == "FifoBufferManagement" or bufferManagement == "TtlBufferManagement"):
                    BFName = bufferManagement
                    if BFName == "FifoBufferManagement":
                        BFName = "DF"
                    if BFName == "TtlBufferManagement":
                        BFName = "DO"
                    if BFName == "RandomBufferManagement":
                        BFName = "DR"
                    if BFName == "AntPlus3BufferManagement":
                        BFName = "CMBP"
                    count += 1
                    for i, strs in np.ndenumerate(x):
                        x[i] = strs.replace("M", "")
                        x[i] = x[i].replace("k", "")
                    if target == "messageDelivery" or target == "Delivery Ratio":
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
                    plt.xlabel('Transmit Speed(KBps)')
                    # plt.xlabel('Cache Size(MB)')
                    plt.legend()
            if not os.path.exists('./datas/' + endTime):
                os.mkdir('./datas/' + endTime)
            if not os.path.exists('./datas/' + endTime + '/' + target):
                os.mkdir('./datas/' + endTime + '/' + target)
            plt.savefig('./datas/' + endTime + '/' + target + '/result.jpg')

    # for index in result_y:
    #     if index != "BMBP":
    #         sum = 0
    #         for i, array in enumerate(result_y[index]):
    #                sum += array / result_y['BMBP'][i]
    #         sum /= 10
    #         sum = str(sum)
    #         print(index+":" + sum)
    # return datas

if __name__ == '__main__':
    load_datas("./reports_transmitSpeed")
