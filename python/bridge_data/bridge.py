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
decoderPath = decoderDir + '\Windows_NPDFileDecoder.exe'
bridgePath = workingDir + '\\raw_bridge.csv'
npdFileDir = workingDir

# pressure bridge sense constants
offsetConst = 0x800000
zeroCalPress = 750      # [mmHg] this value will be read from the AD4130 and reported in metadata.csv
sensitivity = 10e-6    # [1/mmHg] this value will be read from the AD4130 and reported in metadata.csv
bits = 24
maxCounts = 2**(bits - 1)
gain = 64
sample_rate = 200
nyquist = 0.5 * sample_rate

# plot settings
xlabel = 'Time [s]'
ylabel = 'Pressure [mmHg]'
plotlabel = 'Pressure vs Time'
colNames = ['time', 'counts']
trimFirstVals = 5 # trim the leading values to remove startup transient. # TODO: remove this once transient is fixed 
figXsize = 18
figYsize = 10


def decodeNPD(f):
    # run the decoder to convert the .npd file to a .csv file
    # TODO: add a popup with option to cancel or browse for the .npd file if no file is found. 
    # TODO: add ability to drop a file onto the script to run it.
    try:
        print(decoderPath, '-r ' + f)
        # use subprocess.run to run the decoder with the -r flag to decode the .npd file
        subprocess.run([decoderPath, '-r', f], check=True)
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


def processFile(f):
    # read in csv file and store it in a data array. then store each column into it's own array.
    # TODO: add importing of metadata.csv to get the zeroCalPress and sensitivity values as well as storing them in dict for display
    time = np.array([])
    counts = np.array([])
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
    mplcursors.cursor(hover=True)
    plt.show()


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

    # add a button to the plot that runs the calcFFT function
    ax_button = plt.axes([0.08, 0.92, 0.1, 0.04])
    button = plt.Button(ax_button, 'FFT', color='lightgoldenrodyellow', hovercolor='0.975')
    button.on_clicked(lambda x: calcFFT(y))


    mplcursors.cursor(hover=True)
    
    plt.tight_layout()
    plt.show()

        
if __name__ == "__main__":
    # get program start time
    startTime = pd.Timestamp.now()

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
        
    time, counts = processFile(bridgePath)
    pressure = countsToPress(counts)
    
    # print the time it took to process the data
    print(f'Data processing time: {(pd.Timestamp.now() - startTime).total_seconds():.3f} seconds')
    plotData(time, pressure) # change this to plot volts once conversion is implemented
    