def index_closest_value(search_list,search_value):
    import numpy as np
    search_list = np.array(search_list)
    idx = (np.abs(search_list-search_value)).argmin()
    return idx
    
def runningMean(x, N):
    import numpy as np
    return np.convolve(x, np.ones((N,))/N, mode='valid')

def plotVariable(xtime,y,xlabel='x-axis',ylabel='y-axis'):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig, ax = plt.subplots(1)
    Plot  = ax.plot(xtime,y)
    ax.xaxis_date()
    dateFormat = mdates.DateFormatter('%d/%m %H:%M:%S')
    ax.xaxis.set_major_formatter(dateFormat)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.autofmt_xdate()
    
def plotMultiple(x_list, y_list, xlabel='x-axis', ylabel='y-axis', x_time=True):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    if len(x_list) != len(y_list):
        print('Not an equal amount of x and y plots')
        return
    
    colors=['r','g','b']*5
    
    plotAmount = len(x_list)
    fig, ax = plt.subplots(1)
    
    plots = [0]*plotAmount
    for i in range(0,plotAmount):
        plots[i] = ax.plot(x_list[i], y_list[i], color=colors[i])
    
    if x_time:
        ax.xaxis_date()
        dateFormat = mdates.DateFormatter('%d/%m %H:%M:%S')
        ax.xaxis.set_major_formatter(dateFormat)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.autofmt_xdate()
    
def timeAveraged2d(avg_list, numAvg):
    import numpy as np
    #Average an array over time (x axis)
    newlength = len(avg_list)//numAvg
    new_list  = np.empty((newlength,np.shape(avg_list)[1]))
    
    for i in range(0,newlength):
        newSum = 0
        for j in range(0,numAvg):
            newSum += avg_list[i*numAvg+j]
        
        new_list[i][:] = newSum/numAvg
    
    return new_list
    
def timeAverageMiddle(avg_list, numAvg):
    #Average a list in steps
    newlength = len(avg_list)//numAvg
    new_list = [0]*newlength
    for i in range(0,newlength):
        new_list[i] = avg_list[i*numAvg+numAvg//2]
        
    return new_list
    
def wetTemperature_opt(Twet_est, Tdry, RH):
    #Tdry, RH = args
    from math import exp
    Es_Tw = 0.61*exp(19.9*Twet_est/(Twet_est+273))
    Es_Td = 0.61*exp(19.9*Tdry/(Tdry+273))
    Ea    = Es_Tw - 0.066*(Tdry-Twet_est)
    RHest = Ea/Es_Td*100
    
    return abs(RHest-RH)
    
#Function to add ticks
def addticks(ax,newLocs,newLabels,pos='x'):
    import matplotlib.pyplot as plt
 
    # Draw to get ticks
    plt.draw()

    # Get existing ticks
    if pos=='x':
        locs = ax.get_xticks().tolist()
        labels=[x.get_text() for x in ax.get_xticklabels()]
    elif pos =='y':
        locs = ax.get_yticks().tolist()
        labels=[x.get_text() for x in ax.get_yticklabels()]
    else:
        print("WRONG pos. Use 'x' or 'y'")
        return

    # Build dictionary of ticks
    Dticks=dict(zip(locs,labels))

    # Add/Replace new ticks
    for Loc,Lab in zip(newLocs,newLabels):
        Dticks[Loc]=Lab

    # Get back tick lists
    locs=list(Dticks.keys())
    labels=list(Dticks.values())

    # Generate new ticks
    if pos=='x':
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)
    elif pos =='y':
        ax.set_yticks(locs)
        ax.set_yticklabels(labels)
        
def solarAngleCorrection(mtime):
    from pysolar import solar
    import pytz
    from datetime import datetime
    from datetime import timedelta
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    lat, long = 52.2398473,5.6908362
    
    time = mtime - 2/24
    date = mdates.num2date(time)
    
    altitude = solar.get_altitude(lat, long, date, elevation = 90)
    
    #correctionFactor = np.cos(altitude*np.pi/180)
    correctionFactor = 1/np.tan(altitude*np.pi/180)
    
    return correctionFactor
