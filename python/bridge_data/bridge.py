import sys
import subprocess
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
import pandas.plotting.table

working_dir = 'C:/Users/Shawn/NPD Dropbox/Projects/inQB8/Engineering/Hardware/code/AD4130 data'
offset = 0x800000
xlabel = 'Time'
ylabel = 'Counts'
plotlabel = 'Time v Counts'
colNames = [xlabel, ylabel]


# read in csv file and store it in a data array. then store each column into it's own array. 
def processFile(f):
    time = []
    counts = []
    try:
        with open(f, 'r') as file:
            df = pd.read_csv(f, names=colNames, index_col=xlabel)
            # trim the first 50 vlues in df
            df = df.iloc[50:]
            time = df.index.values.tolist()
            counts = df[ylabel].values.tolist()

    except FileNotFoundError:
        print("File not found:", f)
    except Exception as e:
        print("An error occurred:", e)
    return time, counts


def plotData(x, y):
    # Calculate average and range
    avg = np.mean(y)
    range = np.max(y) - np.min(y)
    print(avg, range)

    # # use pandas to plot the data and add a table showing avg and range
    # df = pd.DataFrame({xlabel: x, ylabel: y})
    # ax = df.plot(x=xlabel, y=ylabel, kind='line', title=plotlabel)
    # ax.set_xlabel(xlabel)
    # ax.set_ylabel(ylabel)
    
    # # Create a table with the average and range
    # table_data = [['Average', 'Range'], [avg, range]]
    # fig, axs = plt.subplots(2, 1, figsize=(10, 8))  # 2 rows, 1 column
    # axs[1].axis('tight')
    # axs[1].axis('off')
    # axs[1].table(cellText=table_data, cellLoc='center', loc='center')

    fig, ax = plt.subplots(1, 1)
    table(ax, cellText=table_data, cellLoc='center', loc='upper right')

    # plt.tight_layout()
    plt.show()

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = working_dir + '\\' + sys.argv[1]
    elif len(sys.argv) >= 2:
        print('Error: too many arguments')
        sys.exit(1)
    else:
        filename = working_dir + '/bridge.csv'
    time, counts = processFile(filename)
    plotData(time, counts)
