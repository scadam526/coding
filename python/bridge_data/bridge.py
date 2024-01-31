import os
import sys
import glob
import subprocess
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd
# import pandas.plotting.table

workingDir = os.getcwd()
decoderDir = workingDir
decoderPath = decoderDir + '/Windows_NPDFileDecoder.exe'
bridgePath = workingDir + '/bridge.csv'
npdFileDir = workingDir

# pressure bridge sense constants
offsetConst = 0x800000
gainTrimConst = 0x555555
offsetReg = 0x800000    # this value will be read from the AD4130 and reported in metadata.csv
gainTrimReg = 0x555555  # this value will be read from the AD4130 and reported in metadata.csv
zeroCalPress = 750      # [mmHg] this value will be read from the AD4130 and reported in metadata.csv
sensitivity = 1e-5    # [1/mmHg] this value will be read from the AD4130 and reported in metadata.csv
bits = 24
maxCounts = 2**bits - 1
gain = 64

# plot settings
xlabel = 'Time [s]'
ylabel = 'Pressure [mmHg]'
plotlabel = 'Pressure vs Time'
colNames = ['time', 'counts']
trimFirstVals = 20
figXsize = 18
figYsize = 10


def decodeNPD(f):
    # run the decoder to convert the .npd file to a .csv file
    try:
        subprocess.run([decoderPath, f], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("File not found:", decoderPath)
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)
    print('NPD file decoded to:', bridgePath)

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

    except FileNotFoundError:
        print("File not found:", f)
    except Exception as e:
        print("An error occurred:", e)
    return time, counts


def countsToPress(counts):
    # convert from counts to volts and pressure
    # volts = ((counts - offsetConst) / (maxCounts * gain))*(gainTrimConst / gainTrimReg)+(offsetReg - offsetConst)
    pressure = []
    for count in counts:
        pressure.append(((count-offsetConst)/(sensitivity*maxCounts*gain))*(gainTrimConst/gainTrimReg)+(offsetReg-offsetConst)+zeroCalPress)
    return pressure


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
    plt.text(0.3, .95, 'Average: ' + '{:.2f}'.format(avg) + ' mmHg\nRange: ' + '{:.2f}'.format(range) + ' mmHg', fontsize=10, va='center', ha='left', transform=ax.transAxes, in_layout=False, bbox=dict(facecolor='white', alpha=0.5))
    plt.text(0.95, 0.01, 'Trimmed first ' + str(trimFirstVals) + ' values', fontsize=10, va='bottom', ha='right', transform=ax.transAxes)
    plt.text(0.03, 0.01, 'Cal pressure: ' + str(zeroCalPress) + ' mmHg \nSensitivity: ' + str(int(sensitivity/1e-6)) + ' uV/V/mmHg', fontsize=10, va='bottom', ha='left', transform=ax.transAxes)
    plt.text(0.3, 0.01, 'NPD File: ' + os.path.basename(npdFilePath), fontsize=10, va='bottom', ha='left', transform=ax.transAxes)

    mplcursors.cursor(hover=True)
    
    plt.tight_layout()
    plt.show()

        
if __name__ == "__main__":
    for file in glob.glob('*.csv'):
        os.remove(file)

    if len(sys.argv) == 2:
        npdFilePath = workingDir + '\\' + sys.argv[1]
    elif len(sys.argv) >= 2:
        print('Error: too many arguments')
        sys.exit(1)
    else:
        npdFiles = glob.glob(npdFileDir + '/*.npd')
        npdFiles.sort(key=os.path.getmtime, reverse=True)
        npdFilePath = npdFiles[0]
        print('Using:', npdFilePath)
    
    decodeNPD(npdFilePath)

    if os.path.exists(bridgePath):
        print('bridge file exists')
    else:
        print('bridge file does not exist')
        sys.exit(1)

    time, counts = processFile(bridgePath)
    pressure = countsToPress(counts)
    
    plotData(time, pressure) # change this to plot volts once conversion is implemented
