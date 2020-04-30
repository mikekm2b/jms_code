# program to plot arbitrary set of data with x, y given a .csv file input
# help note 1:  file is assumed to have two lines of information at top, followed by x,y data.  

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('filename', help="filename of csv file") #Mandatory file name
parser.add_argument('--ylo', help="highest y value to plot",type=float)
parser.add_argument('--yhi', help="highest y value to plot",type=float)
args = parser.parse_args()

def create_float_array(lines, nRow):
    # Create recipient float array for freq, R, X data
    data=np.zeros((nRow-2,2), dtype='float')  # Skip first 2 lines (text headers that contain no data).

    i=0  #Initial Index for recipient data array
    # Convert lines (as list) to data array (float)
    for j in range(2,nRow,1): 
        data[i,:]=np.asarray(lines[j], dtype='float')  # Convert List array lines to numpy float array lines
        i=i+1
    return data

def plot_data(data_filen):
    
    nRow = sum(1 for line in open(data_filen)) # Get number of rows in fil

    # Read file into a csv.reader object
    with open(data_filen, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        lines = list(reader)
    
    data = create_float_array(lines,nRow)

    # Set Plot Size
 #   fig_size = plt.rcParams["figure.figsize"]
 #   fig_size[0] = 10
 #   fig_size[1] = 5
 #   plt.rcParams['figure.figsize'] = fig_size
    # Set inside of graph facecolor (1,1,1) = white
    rfc = 0.95
    gfc = 0.95
    bfc = 0.95
    plt.rcParams['axes.facecolor'] = (rfc, gfc, bfc)
    #plt.rcParams['axes.alpha'] = 0.1

    plt.gcf().subplots_adjust(bottom=0.15) # Avoid xlabel text cutoff

    	# Generate plot basics	
    fig1=plt.figure(1)
    plt.plot(data[:,0],data[:,1],'b-o',linewidth=2, markersize=4)
    plt.ylabel('SWR')
    plt.xlabel('Frequency')
    plt.suptitle('SWR from Bird Wattmeter Fwd/Rev Power')
    
   # Set Outside of Figure background color, (1,1,1)=white
    rbk = 0.93
    gbk = 0.93
    bbk = 0.93
    fig1.patch.set_facecolor((rbk, gbk, bbk))

    xlo = data[0,0]
    xhi = data[nRow-3,0]
    if args.ylo and args.yhi:
        plt.xlim(xlo,xhi)
        plt.ylim(args.ylo,args.yhi)

    wm = plt.get_current_fig_manager()
    wm.window.wm_geometry("900x500+500-400")

        
    plt.show()

plot_data(args.filename)