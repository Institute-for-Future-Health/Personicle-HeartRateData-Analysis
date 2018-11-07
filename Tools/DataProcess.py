from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt

GlobalYLabel = 'Heart Rate'

def fileReader(files):
    '''
    Todo: Using getRestData() to do a simple "MapReduce" on the heartrate data from different resturants
    '''

    if not isinstance(files, list):
        files = [files]
    res = []
    restRateMap = defaultdict(list)
    pre_res = ""
    for file in files:
        df = pd.read_csv(file,encoding = "ISO-8859-1")
        for index, row in df.iterrows():
            if row[5] != pre_res:
                restRateMap[row[5]].append([])
                pre_res = row[5]
            if row[3] > 0: continue
            restRateMap[row[5]][-1].append(row[2])
    return restRateMap


def comparePlot(arr1, arr2, **kwargs):
    '''
    Function to plot the a pair of datasets
    '''
    isSame = kwargs.pop('isSame')
    suptitle, title1, title2 = "", "", ""
    restName = kwargs.pop('restName')
    if isSame:
        rest = restName
        suptitle = 'Plots for %s' % (rest)
        title1 = "First Set"
        title2 = "Second Set"
    else:
        rest1 = restName[0]
        rest2 = restName[1]
        suptitle = 'Plots for %s and %s' % (rest1, rest2)
        title1 = rest1
        title2 = rest2

    plt.subplot(121)
    plt.plot(arr1)
    plt.title(title1)
    plt.xlabel('time (m)')
    plt.ylabel(GlobalYLabel)
    plt.suptitle(suptitle, fontsize=16)

    plt.subplot(122)
    plt.plot(arr2)
    plt.xlabel('time (m)')
    plt.title(title2)
    plt.ylabel(GlobalYLabel)
    plt.show()