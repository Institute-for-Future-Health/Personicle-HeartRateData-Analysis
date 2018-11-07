import pandas as pd
import numpy as np

class DataAnalyzer(object):
    def __init__(self):
        self.body_data = []
        self.PRE_NONMOVE_WINDOWSIZE = 5
        self.MIN_NONMOVE_WINDOWSIZE = 5

    def readfiles(self, files):
        df = pd.read_csv(files, encoding="ISO-8859-1")
        for index, row in df.iterrows():
            if row[2] != 0:
                self.body_data.append((row[0], row[2], row[3], row[4], row[5]))

    def getEatingSeg(self):
        index = 0
        start = -1
        output = []
        while index < len(self.body_data):
            segid, heartrate, step, moving, status = self.body_data[index]

            if status == 'eating' and index > 0 and self.body_data[index - 1][4] != 'eating':
                start = index
                # print(start)
            elif status == 'eating' and ((index < len(self.body_data) - 1 and self.body_data[index + 1][4] != 'eating') or index == len(self.body_data)-1):
                _, hr, _, _, _= zip(*self.body_data[start:index+1])
                ave = np.mean(hr)
                output.append((segid, ave))
            index += 1

        print(output)
        return output

    def getPreNonMovingSegmentId(self):
        output = []
        pre_eating = -1
        pre_segid = -1
        start_of_nonmove = -1
        for index, row in enumerate(self.body_data):
            segid, heartrate, step, moving, status = row
            if status == 'eating':
                if index > 0 and self.body_data[index - 1][3]:
                    if pre_eating != -1:
                        i = pre_eating
                        j = 0
                        total = 0
                        while not self.body_data[i][3] and j < self.PRE_NONMOVE_WINDOWSIZE:
                            # print(body_data)
                            total += self.body_data[i][1]
                            j += 1
                            i -= 1
                        output.append((pre_segid, total / self.PRE_NONMOVE_WINDOWSIZE))
                        # print(output)
                        pre_segid = -1
                        pre_eating = -1
            else:
                if index > 0 and self.body_data[index - 1][3]:
                    start_of_nonmove = index

                if not moving and index < len(self.body_data) - 1 and (
                        self.body_data[index + 1][3] or self.body_data[index + 1][4] == 'eating'):
                    if start_of_nonmove != -1 and index - start_of_nonmove > self.MIN_NONMOVE_WINDOWSIZE:
                        pre_eating = index
                        pre_segid = segid

        with open('output.txt', 'w') as f:
            for row in output:
                f.write(str(row[0]) + ',' + str(row[1]) + '\n')
        print(output)
        return output


if __name__ == "__main__":
    d = DataAnalyzer()

    d.readfiles('jordan2.csv')
    d.getEatingSeg()
    d.getPreNonMovingSegmentId()