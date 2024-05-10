import os
import shutil
import sys
import glob
import subprocess
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd

workingDir = os.getcwd()
decoderDir = workingDir
decoderPath = decoderDir + '\\Windows_NPDFileDecoder.exe'
bridgePath = workingDir + '\\bridge.csv'
npdFileDir = workingDir

# pressure bridge sense constants
offsetConst = 0x800000
zeroCalPress = 750      # [mmHg] this value will be read from the AD4130 and reported in metadata.csv
sensitivity = 10e-6   # [1/mmHg] this value will be read from the AD4130 and reported in metadata.csv
bits = 24
maxCounts = 2**(bits - 1)
gain = 64
sample_rate = 200
nyquist = 0.5 * sample_rate

# plot settings
xlabel = 'Time [s]'
ylabel = 'Pressure [mmHg]'
plotlabel = 'Pressure vs Time'
colNames = ['time', 'counts', 'decoderPress']
trimFirstVals = 0 # trim the leading values to remove startup transient. # TODO: remove this once transient is fixed 
figXsize = 18
figYsize = 10


def decodeNPD(f):
    # run the decoder to convert the .npd file to a .csv file
    # TODO: add a popup with option to cancel or browse for the .npd file if no file is found. 
    try:
        print('Running decoder:', decoderPath, '-r ' + f)
        # use subprocess.run to run the decoder
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
    print('Bridge data decoded to:', bridgePath)


def processBridgeFile(f):
    # read in csv file and store it in a data array. then store each column into it's own array.
    time = np.array([])
    counts = np.array([])
    try:
        with open(f, 'r') as file:
            df = pd.read_csv(f, names=colNames, index_col=colNames[0])
            if trimFirstVals > 0: 
                df = df.iloc[trimFirstVals:] # trim the first 50 vlues in df
            df.index = df.index / 1e6 # divide all time values by 1e6 to convert from microseconds to seconds
            time = df.index.values.tolist()
            decoderPress = df['decoderPress'].values.tolist()
            counts = df['counts'].values.tolist()

    except FileNotFoundError:
        print("File not found:", f)
    except Exception as e:
        print("An error occurred:", e)
    return time, counts, decoderPress

# function to bring in metadata.csv and create a dictionary of the values with column 1 as the key and column 2 as the value
def getMetaData(f):
    # read in metadata.csv and store it in a dictionary
    try:
        with open(f, 'r') as file:
            df = pd.read_csv(f, names=['key', 'value'], index_col='key')
            # trim trailing zeros from the key and value columns
            df.index = df.index.str.strip()
            df['value'] = df['value'].str.strip()
            # print(df.to_dict()['value'])
            return df.to_dict()['value']
    except FileNotFoundError:
        print("File not found:", f)
    except Exception as e:
        print("An error occurred:", e)


def countsToPress(counts):  
    # convert counts to pressure
    return ((np.array(counts) - offsetConst) / (sensitivity * maxCounts * gain)) + zeroCalPress

def calcFFT(press):
    # compute frequency and amplitude of the FFT
    fft_values = np.fft.fft(press)
    frequencies = np.fft.fftfreq(len(fft_values), 1/(sample_rate-1))

    plt.figure(figsize=(15,10))
    plt.plot(frequencies, np.abs(fft_values), linewidth=0.5)  # Set line width to 0.5
    plt.title('FFT of Pressure vs Time')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim([0, nyquist])  # Set x-axis limits to 0-100Hz
    plt.ylim([0, 600])  # Set x-axis limits to 0-100Hz
    plt.xticks(np.arange(0, 101, 5)) 
    plt.grid(True)
    plt.tight_layout()
    plt.show()
 

def plotData(x, y1, y2):
    # Calculate average and range
    avg = np.mean(y1)
    range = np.max(y1) - np.min(y1)

    # plot the data
    # df = pd.DataFrame({xlabel: x, ylabel: y1})
    # ax = df.plot(x=xlabel, y=ylabel, figsize=(15, 10), kind='line', title=plotlabel)
    # plot y1 and y2 vs x on the same axis
    fig, ax = plt.subplots(figsize=(figXsize, figYsize))
    ax.plot(x, y2, label='Decoder Pressure', color='lightblue')
    ax.plot(x, y1, label='Calculated Pressure', color='b')
    ax.legend()
    ax.set_title(plotlabel)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    # print pertinant data on the plot
    plt.text(0.3, .95, 'Average: ' + '{:.2f}'.format(avg) + ' mmHg\nRange: ' + '{:.2f}'.format(range) + ' mmHg', fontsize=10, va='center', ha='left', transform=ax.transAxes, in_layout=False, bbox=dict(facecolor='white', alpha=0.5))
    plt.text(0.95, 0.01, 'Trimmed first ' + str(trimFirstVals) + ' values', fontsize=10, va='bottom', ha='right', transform=ax.transAxes)
    plt.text(0.03, 0.01, 'Cal pressure: ' + str(zeroCalPress) + ' mmHg \nSensitivity: ' + str(int(sensitivity/1e-6)) + ' uV/V/mmHg', fontsize=10, va='bottom', ha='left', transform=ax.transAxes)
    plt.text(0.3, 0.01, 'NPD File: ' + os.path.basename(npdFilePath), fontsize=10, va='bottom', ha='left', transform=ax.transAxes)

    # add a button to the plot that runs the calcFFT function
    ax_button = plt.axes([0.075, 0.9, 0.1, 0.04])
    button = plt.Button(ax_button, 'FFT', color='lightgoldenrodyellow', hovercolor='0.975')
    button.on_clicked(lambda x: calcFFT(y1))

    # add a button to show the contents of matadata in a table
    # ax_button2 = plt.axes([0.08, 0.85, 0.1, 0.04])
    # button2 = plt.Button(ax_button2, 'Metadata', color='lightgoldenrodyellow', hovercolor='0.975')
    # button2.on_clicked(showMetadata(metadata))

    mplcursors.cursor(hover=True)
    plt.subplots_adjust(left=0.05, right = 0.98, top = 0.95, bottom = 0.05, wspace=0.2, hspace=0.2)
    plt.show()

        
if __name__ == "__main__":
    # get program start time
    startTime = pd.Timestamp.now()

    # get current user home directory
    home = os.path.expanduser("~")
    for file in glob.glob(home + '/Desktop/*.npd'):
        # move any .npd files on the desktop to the working directory
        os.rename(file, npdFileDir + '\\' + os.path.basename(file))

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

    if not os.path.exists(bridgePath):
        print('bridge file does not exist')
        sys.exit(1)
        
    metadata = getMetaData(workingDir + '\\metadata.csv')
    zeroCalPress = int(metadata['bridgeAmbientReference'])
    sensitivity = float(metadata['bridgeSensitivity']) / 1e6
    gain = int(metadata['bridgeGain'])
    serialNumber = metadata['serialNumber']
    time, counts, decoderPress = processBridgeFile(bridgePath)
    pressure = countsToPress(counts)

    # copy the npd file to C:\Users\Shawn\NPD Dropbox\Projects\inQB8\Engineering\Hardware\logs\Rev1 Implant Scale Test Logs
    # shutil.copy(npdFilePath, 'C:\\Users\\Shawn\\NPD Dropbox\\Projects\\inQB8\\Engineering\\Hardware\\logs\\Rev1 Implant Scale Test Logs\\' + serialNumber + '.npd')

    # print the time it took to process the data
    print(f'Data processing time: {(pd.Timestamp.now() - startTime).total_seconds():.3f} seconds')
    plotData(time, pressure, decoderPress) # change this to plot volts once conversion is implemented
    