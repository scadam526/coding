import sys
import subprocess
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
# import pandas.plotting.table

workingDir = 'C:/Users/Shawn/NPD Dropbox/Projects/inQB8/Engineering/Hardware/code/AD4130 data'
decoderDir = workingDir

# pressure bridge sense constants
offsetConst = 0x800000
gainTrimConst = 0x555555
offsetReg = 0x800000    # this value will be read from the AD4130 and reported in metadata.csv
gainTrimReg = 0x555555  # this value will be read from the AD4130 and reported in metadata.csv
sensitivity = 1e-5    # [1/mmHg] this value will be read from the AD4130 and reported in metadata.csv
bits = 24
maxCounts = 2**bits - 1
gain = 64

xlabel = 'Time [s]'
ylabel = 'Pressure [mmHg]'
plotlabel = 'Pressure vs Time'
colNames = ['time', 'counts']
trimFirstVals = 20
figXsize = 15
figYsize = 10



# read in csv file and store it in a data array. then store each column into it's own array. 
def processFile(f):
    time = []
    counts = []
    try:
        with open(f, 'r') as file:
            df = pd.read_csv(f, names=colNames, index_col=colNames[0])
            if trimFirstVals > 0: 
                df = df.iloc[trimFirstVals:] # trim the first 50 vlues in df
            
            df.index = df.index / 1e6 # divide all time values by 1e6 to convert from microseconds to seconds
            
            time = df.index.values.tolist()
            counts = df['counts'].values.tolist()
            print(counts)

    except FileNotFoundError:
        print("File not found:", f)
    except Exception as e:
        print("An error occurred:", e)
    return time, counts

# def countsToVoltsPress(counts):
    # add AD4130 conversion code here
    # volts = df[ylabel]

    # pressure = []
    


def plotData(x, y):
    # Calculate average and range
    avg = np.mean(y)
    range = np.max(y) - np.min(y)

    # plot the data
    df = pd.DataFrame({xlabel: x, ylabel: y})
    ax = df.plot(x=xlabel, y=ylabel, figsize=(15, 10), kind='line', title=plotlabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # print pertinant data on the plot
    plt.text(0.3, .95, 'Average: ' + str(avg) + '\nRange: ' + str(range), fontsize=10, va='center', ha='left', transform=ax.transAxes, in_layout=False, bbox=dict(facecolor='white', alpha=0.5))
    plt.text(0.95, 0.02, 'Trimmed first ' + str(trimFirstVals) + ' values', fontsize=10, va='bottom', ha='right', transform=ax.transAxes)

    mplcursors.cursor(hover=True)
    
    plt.tight_layout()
    plt.show()

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = workingDir + '\\' + sys.argv[1]
    elif len(sys.argv) >= 2:
        print('Error: too many arguments')
        sys.exit(1)
    else:
        filename = workingDir + '/bridge.csv'
    time, counts = processFile(filename)
    # volts, pressure = countsToVoltsPress(counts)
    plotData(time, counts) # change this to plot volts once conversion is implemented
