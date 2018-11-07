import sys
import numpy as np
from Tools.DataProcess import *
from scipy import stats


SegmentSize = 10
valVarQualifier = 0

PRE_NONMOVE_WINDOWSIZE = 5
MIN_NONMOVE_WINDOWSIZE = 5

def getPreNonMovingSegmentId(file):
    df = pd.read_csv(file, encoding="ISO-8859-1")
    body_data = []
    output = []
    for index, row in df.iterrows():
        body_data.append((row[0], row[2], row[3], row[4], row[5]))
    pre_eating = -1
    pre_segid = -1
    start_of_nonmove = -1
    for index, row in enumerate(body_data):
        segid, heartrate, step, moving, status = row
        if status == 'eating':
            if index > 0 and body_data[index - 1][3]:
                if pre_eating != -1:
                    i = pre_eating
                    j = 0
                    total = 0
                    while not body_data[i][3] and j < PRE_NONMOVE_WINDOWSIZE:
                        # print(body_data)
                        total += body_data[i][1]
                        j += 1
                        i -= 1
                    output.append((pre_segid, total/PRE_NONMOVE_WINDOWSIZE))
                    # print(output)
                    pre_segid = -1
                    pre_eating = -1
        else:
            if index > 0 and body_data[index - 1][3]:
                start_of_nonmove = index

            if not moving and index < len(body_data)-1 and (body_data[index + 1][3] or body_data[index + 1][4] == 'eating'):
                if start_of_nonmove!= -1 and index - start_of_nonmove > MIN_NONMOVE_WINDOWSIZE:
                    pre_eating = index
                    pre_segid = segid

    with open('output.txt', 'w') as f:
        for row in output:
            f.write(str(row[0]) + ',' + str(row[1]) + '\n')

    return output




def getNpMaxVar(inputArray, segsize = SegmentSize):
    '''
    Todo: Get the highest segment Variation of the array and the segment with that Variation
    '''
    maxVar = -sys.maxsize
    outSegment = []
    N = len(inputArray)
    for begpoint in range(N-segsize):
        subSeg = inputArray[begpoint : begpoint+segsize]
        curVar = np.var(subSeg)
        if curVar > maxVar:
            maxVar = curVar
            outSegment = subSeg
    return maxVar, outSegment


def getAccMaxVar(inputArray, segsize = SegmentSize):
    '''
    Todo: Get the highest segment Variation of the array and the segment with that Variation
    '''
    maxVar = -sys.maxsize
    outSegment = []
    N = len(inputArray)
    for begpoint in range(N-segsize):
        subSeg = inputArray[begpoint : begpoint+segsize]
        curVar = getPartVar(subSeg)
        if curVar > maxVar:
            maxVar = curVar
            outSegment = subSeg
    return maxVar, outSegment


def getPartVar(inputArray):
    res = 0
    for i in range(1, len(inputArray)):
        res += (inputArray[i] - inputArray[i-1])
    return res

def getVar(inputArray, segsize = SegmentSize):
    outSegment = []
    N = len(inputArray)
    for begpoint in range(N-segsize):
        outSegment.append(getPartVar(inputArray[begpoint:begpoint+segsize]))
    return outSegment

def getAve(inputArray, segsize = SegmentSize):
    outSegment = []
    N = len(inputArray)
    for begpoint in range(N-segsize):
        outSegment.append(np.average(inputArray[begpoint:begpoint+segsize]))
    return outSegment

def getValidMaxArray(inputArray, segsize = SegmentSize):
    '''
    Todo: Get the segment with the greatest average value while the variation is not neagtive
    :param inputArray:
    :param segsize:
    :return:
    '''
    ave_var_comb = []
    N = len(inputArray)
    for begpoint in range(N - segsize):
        part = inputArray[begpoint:begpoint + segsize]
        part_ave = np.average(part)
        part_var = np.var(part)
        ave_var_comb.append((part_ave, part_var, part))

    ave_var_comb.sort(key = lambda x: x[0], reverse=True)
    i = 0
    while i < len(ave_var_comb) and ave_var_comb[i][1] < valVarQualifier:
        i += 1
    if i >= len(ave_var_comb): return None
    return ave_var_comb[i][2]


def comparison(input1, input2):
    name1, name2, arr1, arr2 = input1[0], input2[0], input1[1], input2[1]
    selData_1 = getValidMaxArray(input1[1])
    selData_2 = getValidMaxArray(input2[1])

    if name1 == name2:
        comparePlot(selData_1, selData_2, isSame=True, restName=name1)
        msg = "Pearson correlation coefficient of two datasets from %s is " % (name1)
    else:
        comparePlot(selData_1, selData_2, isSame=False, restName=[name1, name2])


    print("Max Variation from the %s set" % (name1), selData_1)
    print("Max Variation from the %s set" % (name2), selData_2)

    pearVal, _ = stats.pearsonr(selData_1, selData_2)
    if name1 == name2:
        print("Pearson correlation coefficient of two datasets from %s is %f" % (name1, pearVal))
    else:
        print("Pearson correlation coefficient of two datasets from %s and %s is %f" % (name1, name2, pearVal))


if __name__ == '__main__':
    output = getPreNonMovingSegmentId("jordan2_segment.csv")