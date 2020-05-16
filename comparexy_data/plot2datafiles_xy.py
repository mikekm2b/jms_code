# program to plot arbitrary set of data with x, y given a .csv file input
# help note 1:  file is assumed to have two lines of information at top, followed by x,y data.  

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('filename1', help="filename1 of csv file") #required
parser.add_argument('filename2', help="filename2 of csv file") #required
parser.add_argument('--ylo', help="highest y value to plot",type=float)
parser.add_argument('--yhi', help="highest y value to plot",type=float)
args = parser.parse_args()

def csv2list(data_csv):
    with open(data_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        lines = list(reader)
    return lines

def create_float_array(lines, nRow):
    # Create recipient float array for freq, R, X data
    data=np.zeros((nRow-2,2), dtype='float')  # Skip first 2 lines (text headers that contain no data).

    i=0  #Initial Index for recipient data array
    # Convert lines (as list) to data array (float)
    for j in range(2,nRow,1): 
        data[i,:]=np.asarray(lines[j], dtype='float')  # Convert List array lines to numpy float array lines
        i=i+1
    return data

def plot_data(data_csv1,data_csv2):
    
    nRow1 = sum(1 for line in open(data_csv1)) # Get number of rows in file
    nRow2 = sum(1 for line in open(data_csv2)) # Get number of rows in file

    # Read file into a csv.reader object
    lines1 = csv2list(data_csv1)
    lines2 = csv2list(data_csv2)
    
    data1 = create_float_array(lines1,nRow1)
    data2 = create_float_array(lines2,nRow2)

    # Set Plot Size
 #   fig_size = plt.rcParams["figure.figsize"]
 #   fig_size[0] = 10
 #   fig_size[1] = 5
 #   plt.rcParams['figure.figsize'] = fig_size
    # Set inside of graph facecolor (1,1,1) = white
    rfc = 1.0
    gfc = 1.0
    bfc = 1.0
    plt.rcParams['axes.facecolor'] = (rfc, gfc, bfc)
    #plt.rcParams['axes.alpha'] = 0.1

    # Set save figure directory
    plt.rcParams["savefig.directory"] = "D:\\plot2datafiles_xy"

    plt.gcf().subplots_adjust(bottom=0.15) # Avoid xlabel text cutoff
    # Generate plot basics
    data1_color=(0.5, 0.1, 0.1)
    data2_color=(0.1,0.4,0.1) 	
    fig1=plt.figure(1)
    plt.plot(data1[:,0],data1[:,1],linewidth=1.5, marker="o",fillstyle='none', markersize=4,c=data1_color)
    plt.plot(data2[:,0],data2[:,1],linewidth=1.5, marker="o",fillstyle='none',markersize=4,c=data2_color)
    plt.ylabel('SWR')
    plt.xlabel('Frequency, MHz')
    plt.suptitle('SWR from Bird Wattmeter Fwd/Rev Power')
    # Determine location of legend text
    xlo = data1[0,0]
    xhi = data1[nRow1-3,0]
    x1 = xlo + 1.0
    x2 = xlo + 1.0
    y1 = args.yhi-0.1
    y2 = args.yhi-0.2
    plt.text(x1,y1,args.filename1, c=data1_color)
    plt.text(x2,y2,args.filename2, c=data2_color)
    
   # Set Outside of Figure background color, (1,1,1)=white
    rbk = 0.93
    gbk = 0.93
    bbk = 0.93
    fig1.patch.set_facecolor((rbk, gbk, bbk))

    if args.ylo and args.yhi:
        plt.xlim(xlo,xhi)
        plt.ylim(args.ylo,args.yhi)

    #Set size and location of graph on screen
    wm = plt.get_current_fig_manager()
    wm.window.wm_geometry("700x400+500-400")

        
    plt.show()

plot_data(args.filename1,args.filename2)