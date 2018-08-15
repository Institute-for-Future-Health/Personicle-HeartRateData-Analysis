import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

df = pd.read_csv('eating_jordan2.csv', encoding = "ISO-8859-1")

# dataframe = pd.DataFrame(df)

rate_segments = []
for index, row in df.iterrows():

    rate_segments.append([])
    # print(index, row[2])


plt.plot(heartrates)

plt.ylabel('heart rate')
plt.show()