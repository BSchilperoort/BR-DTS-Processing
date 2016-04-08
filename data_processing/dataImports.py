##DTS
def dts(fileName):
    '''Takes: filename
       Returns: timestamp, distances, temperature'''
    print('Importing the DTS file...')
    
    import numpy as np
    from datetime import datetime

    #Get length of file
    with open(fileName) as fileobject:
        file_length = sum(1 for line in fileobject)-3
    
    #Load the data line by line, into numpy arrays where possible
    with open(fileName) as fileobject:
        file_header_1 = fileobject.readline()
        distances = np.array([float(x) for x in fileobject.readline().split(';')])
        data_amount = len(distances)
        file_header_2 = fileobject.readline()
        
        timestamp   = [0]*file_length
        temperature = np.empty((file_length,data_amount))
        for i in range(0,file_length):
            row               = fileobject.readline().split('\t')
            timestamp[i]      = datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%S')
            temperature[i][:] = [float(x) for x in row[1].split(';')]
    return timestamp, distances, temperature

##Cesar Humidity
def cesar_humidity(cesar_file):
    '''Usage: cesar_humidity_data = cesar_humidity(fileName)
    Takes; A (raw) string
    Returns; Python dictionary with all the data.
    
    NOTE: Calibration coefficients and time correction are
          included in this function...'''
    print('Importing the temperature, RH file...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates

    #Get file length:
    with open(cesar_file) as fileobject:
        cesar_file_length = sum(1 for line in fileobject)-1
    
    #Initialise arrays:
    cesar_time  = [0]*cesar_file_length

    cesarT46m  = np.empty(cesar_file_length)
    cesarRH46m = np.empty(cesar_file_length)
    cesarT36m  = np.empty(cesar_file_length)
    cesarRH36m = np.empty(cesar_file_length)
    cesarT32m  = np.empty(cesar_file_length)
    cesarRH32m = np.empty(cesar_file_length)
    cesarT24m  = np.empty(cesar_file_length)
    cesarRH24m = np.empty(cesar_file_length)
    cesarT16m  = np.empty(cesar_file_length)
    cesarRH16m = np.empty(cesar_file_length)

    #Load the data from file
    with open(cesar_file) as fileobject:
        file_header_cesar = fileobject.readline()
        
        for i in range(0,cesar_file_length):
            row          = fileobject.readline().split(';')
            
            cesar_time[i] = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            
            cesarT46m[i]  = float(row[1])
            cesarRH46m[i] = float(row[2])
        
            cesarT36m[i]  = float(row[3])
            cesarRH36m[i] = float(row[4])
            
            cesarT32m[i]  = float(row[5])
            cesarRH32m[i] = float(row[6])
            
            cesarT24m[i]  = float(row[7])
            cesarRH24m[i] = float(row[8])
            
            cesarT16m[i]  = float(row[9])
            cesarRH16m[i] = float(row[10])
    
    cesar_time_correction = timedelta(minutes=60,seconds=0)
    cesar_time  = [x+cesar_time_correction for x in cesar_time]
    cesar_mtime = np.array([mdates.date2num(x) for x in cesar_time])
    
    cesarT46m  = -0.000787*cesarT46m**2  +  1.02*cesarT46m  - 0.115
    cesarRH46m = 0.00321  *cesarRH46m**2 + 0.613*cesarRH46m + 5.7
    
    cesarT36m  = 0.0000723*cesarT36m**2  +  0.98*cesarT36m  + 0.738
    cesarRH36m = 0.00127  *cesarRH36m**2 + 0.834*cesarRH36m - 0.248
    
    cesarT32m  =      cesarT32m  + 0.0354
    cesarRH32m = 0.99*cesarRH32m - 0.945
    
    cesarT16m  = cesarT16m  - 0.326
    cesarRH16m = cesarRH16m - 0.945
    
    
    cesarRH46m = np.clip(cesarRH46m, 0, 100)
    cesarRH36m = np.clip(cesarRH36m, 0, 100)
    cesarRH32m = np.clip(cesarRH32m, 0, 100)
    cesarRH24m = np.clip(cesarRH24m, 0, 100)
    cesarRH16m = np.clip(cesarRH16m, 0, 100)

    cesar_data = {'Time': cesar_mtime,
                 'T16': cesarT16m, 'RH16': cesarRH16m,
                 'T24': cesarT24m, 'RH24': cesarRH24m,
                 'T32': cesarT32m, 'RH32': cesarRH32m,
                 'T36': cesarT36m, 'RH36': cesarRH36m,
                 'T46': cesarT46m, 'RH46': cesarRH46m}
    
    return cesar_data
    ec_mtime, ec_latent_heat, ec_latent_quality, ec_sensible_heat, ec_sensible_quality, ec_wind_direction, ec_co2_flux, ec_co2_quality
def ec_cesar(eddyFile):
    '''Takes filename 
    Returns: time, latent heat, latent heat quality, 
             sensible heat, sensible heat quality, wind direction,
             CO2 flux, CO2 flux quality
    Example: T, LE, _, H, _, _, _, _ = ec_cesar(fileName)'''
    print('Importing the eddy covariance file...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates

    with open(eddyFile) as fileobject:
        eddy_file_length = sum(1 for line in fileobject)-3
    
    ec_time  = [0]*eddy_file_length
    ec_mtime = np.empty(eddy_file_length)
    
    ec_latent_heat      = np.empty(eddy_file_length)
    ec_sensible_heat    = np.empty(eddy_file_length)
    
    ec_latent_quality   = np.empty(eddy_file_length)
    ec_sensible_quality = np.empty(eddy_file_length)
    
    ec_wind_direction    = np.empty(eddy_file_length)
    
    ec_co2_flux          = np.empty(eddy_file_length)
    ec_co2_quality       = np.empty(eddy_file_length)
    
    with open(eddyFile) as fileobject:
        file_header_1 = fileobject.readline()
        file_header_2 = fileobject.readline()
        
        for i in range(0,eddy_file_length):
            row        = fileobject.readline().split(';')
            
            time_year   = '20'+row[0]
            time_days   = int(row[1])
            time_hours  = (float(row[2]) - 0.25)
                       
            time_full   = datetime.strptime(time_year,'%Y')
            time_full  += timedelta(days=time_days, hours=time_hours)
            time_full  += timedelta(minutes=60) #Cesar time difference
            
            ec_time[i]  = time_full
            ec_mtime[i] = mdates.date2num(time_full)
            
            ec_sensible_heat[i] = float(row[3])
            ec_latent_heat[i]   = float(row[5])
            
            ec_sensible_quality[i]    = int(float(row[6])) 
            ec_latent_quality[i]      = int(float(row[8]))
            
            ec_wind_direction[i]    = float(row[17])
            
            ec_co2_flux[i]          = float(row[4])
            ec_co2_quality[i]     = float(row[7])
    
    
    return (ec_mtime, ec_latent_heat, ec_latent_quality,
            ec_sensible_heat, ec_sensible_quality, ec_wind_direction, 
            ec_co2_flux, ec_co2_quality)
    
##radiometer
def radiometer(radiometer_file):
    '''Takes: filename
       Returns: time, net radiation, SI, SO, LI, LO'''
    print('Importing the radiometer file...')
       
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates
    
    with open(radiometer_file) as fileobject:
        radiometer_file_length = sum(1 for line in fileobject)-1
        
    radiometer_time  = [0]*radiometer_file_length
    radiometer_mtime = np.empty(radiometer_file_length)
    
    rad_short_in   = np.empty(radiometer_file_length)
    rad_short_out  = np.empty(radiometer_file_length)
    rad_long_in    = np.empty(radiometer_file_length)
    rad_long_out   = np.empty(radiometer_file_length)
    rad_net        = np.empty(radiometer_file_length)
    
    with open(radiometer_file) as fileobject:
        file_header = fileobject.readline()
        
        for i in range(0,radiometer_file_length):
            row          = fileobject.readline().split(';')
            
            time_full    = datetime.strptime(row[0],'%Y-%m-%d %H:%M')
            time_full   += timedelta(minutes=60) #Cesar time difference
            
            radiometer_time[i]  = time_full
            radiometer_mtime[i] = mdates.date2num(time_full)
            
            rad_short_in[i]     = float(row[1])
            rad_short_out[i]    = float(row[2])
            rad_long_in[i]      = float(row[3])
            rad_long_out[i]     = float(row[4])
            rad_net[i]          = float(row[5])
    
    return radiometer_mtime, rad_net, rad_short_in, rad_short_out, rad_long_in, rad_long_out

def hobo_windspeed(wind_file):
    '''Takes: filename
       Returns: time, windspeed, gust speed'''
    print('Importing the radiometer file...')
       
    import numpy as np
    from datetime import datetime
    import matplotlib.dates as mdates
    
    with open(wind_file) as fileobject:
        wind_file_length = sum(1 for line in fileobject)-2
    
    wind_time  = np.empty(wind_file_length)
    wind_speed = np.empty(wind_file_length)
    wind_gust  = np.empty(wind_file_length)
    
    with open(wind_file) as fileobject:
        file_header_wind_1 = fileobject.readline()
        file_header_wind_2 = fileobject.readline()
        
        for i in range(0,wind_file_length):
            row          = fileobject.readline().split(',')
            
            time_stamp    = row[1]
            wind_datetime = datetime.strptime(time_stamp, '%m/%d/%y %I:%M:%S %p')
            
            wind_time[i]  = mdates.date2num(wind_datetime)
            wind_speed[i] = float(row[2])
            wind_gust[i]  = float(row[3])
    
    return wind_time, wind_speed, wind_gust

def cesar_windspeed(wind_file, time_difference):
    '''Takes: filename, time difference with reference 
    Time difference is in minutes, if cesar_wind is behind number is negative
    Returns: time, wind_speed'''
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates
    
    with open(wind_file) as fileobject:
        wind_file_length = sum(1 for line in fileobject)-4
        
    wind_time =  np.empty(wind_file_length)
    wind_speed = np.empty(wind_file_length)
    
    with open(wind_file) as fileobject:
        file_header_wind_1 = fileobject.readline()
        file_header_wind_2 = fileobject.readline()
        file_header_wind_3 = fileobject.readline()
        file_header_wind_4 = fileobject.readline()
        
        for i in range(0,wind_file_length):
            row           = fileobject.readline().split(',')
            
            time_stamp    = row[0][1:-1]
            time_delta    = timedelta(minutes=time_difference)
            wind_datetime = datetime.strptime(time_stamp, '%Y-%m-%d %H:%M:%S')
            
            wind_time[i]  = mdates.date2num(wind_datetime-time_difference)
            wind_speed[i] = float(row[2])
    
    return wind_time, wind_speed

def Cesar_T_RH_2(cesar_file):
    '''Usage: cesarTRHdata = Cesar_T_RH(fileName)
       Takes; A (raw) string
       Returns; Python dictionary with all the data.'''
    print('Importing the temperature, RH file...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates

    #Get file length:
    with open(cesar_file) as fileobject:
        cesar_file_length = sum(1 for line in fileobject)-1
    
    #Initialise arrays:
    cesar_time  = np.empty(cesar_file_length)

    cesarT46m  = np.empty(cesar_file_length)
    cesarRH46m = np.empty(cesar_file_length)
    cesarTW46m = np.empty(cesar_file_length)
    cesarT36m  = np.empty(cesar_file_length)
    cesarRH36m = np.empty(cesar_file_length)
    cesarTW36m = np.empty(cesar_file_length)
    cesarT32m  = np.empty(cesar_file_length)
    cesarRH32m = np.empty(cesar_file_length)
    cesarTW32m = np.empty(cesar_file_length)
    cesarT24m  = np.empty(cesar_file_length)
    cesarRH24m = np.empty(cesar_file_length)
    cesarTW24m = np.empty(cesar_file_length)
    cesarT16m  = np.empty(cesar_file_length)
    cesarRH16m = np.empty(cesar_file_length)
    cesarTW16m = np.empty(cesar_file_length)

    #Load the data from file
    with open(cesar_file) as fileobject:
        file_header_cesar = fileobject.readline()
        
        for i in range(0,cesar_file_length):
            row          = fileobject.readline().split(';')
            
            cesar_time[i]  = float(row[0])
            
            cesarT46m[i]  = float(row[1])
            cesarRH46m[i] = float(row[2])
            cesarTW46m[i] = float(row[3])
        
            cesarT36m[i]  = float(row[4])
            cesarRH36m[i] = float(row[5])
            cesarTW36m[i] = float(row[6])
            
            cesarT32m[i]  = float(row[7])
            cesarRH32m[i] = float(row[8])
            cesarTW32m[i] = float(row[9])
            
            cesarT24m[i]  = float(row[10])
            cesarRH24m[i] = float(row[11])
            cesarTW24m[i] = float(row[12])
            
            cesarT16m[i]  = float(row[13])
            cesarRH16m[i] = float(row[14])
            cesarTW16m[i] = float(row[15])

    cesar_data = {'Time': cesar_time,
                 'T16': cesarT16m, 'RH16': cesarRH16m, 'TW16': cesarTW16m,
                 'T24': cesarT24m, 'RH24': cesarRH24m, 'TW24': cesarTW24m,
                 'T32': cesarT32m, 'RH32': cesarRH32m, 'TW32': cesarTW32m,
                 'T36': cesarT36m, 'RH36': cesarRH36m, 'TW36': cesarTW36m,
                 'T46': cesarT46m, 'RH46': cesarRH46m, 'TW46': cesarTW46m}
    
    return cesar_data
    
def knmi_air_pressure(fileName):
    print('Importing the air pressure data...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates
    
    #Get file length:
    with open(fileName) as fileobject:
        pressure_file_length = sum(1 for line in fileobject)-1
    
    #Initialise arrays:
    pressure_time  = np.empty(pressure_file_length)
    pressure_kpa   = np.empty(pressure_file_length)
    
     #Load the data from file
    with open(fileName) as fileobject:
        file
        file_header_pressure = fileobject.readline()
        
        for i in range(0,pressure_file_length):
            row             = fileobject.readline().split(';')
            
            date            = datetime.strptime(row[0],'%Y%m%d')
            hours           = timedelta(hours=float(row[1]))
            timezone_cor    = timedelta(hours=1)
            
            time            = date+hours+timezone_cor
            
            pressure_time[i] = mdates.date2num(time)
            pressure_kpa[i]  = (10*float(row[2])-860) / 1000 #Pressure in kPa, corrected for height
            
    return pressure_time, pressure_kpa
    
def soil_flux(fileName):
    print('Importing the soil flux data...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates
    
    #Get file length:
    with open(fileName) as fileobject:
        file_length = sum(1 for line in fileobject)-1
    
    #Initialise arrays:
    soilFluxTime   = np.empty(file_length)
    soilHeatFlux   = np.empty(file_length)
    
     #Load the data from file
    with open(fileName) as fileobject:
        fileHeader = fileobject.readline()
        
        for i in range(0,file_length):
            row             = fileobject.readline().split(';')
            
            year            = row[0]
            day             = int(row[1])
            hour            = int(row[4][0:2])
            minutes         = int(row[4][2:4])
            
            date            = datetime.strptime(row[0],'%Y')
            date           += timedelta(days=day)
            date           += timedelta(hours=hour)
            date           += timedelta(minutes=minutes)
            
            soilFluxTime[i] = mdates.date2num(date)
            soilHeatFlux[i] = float(row[3])
            
    return soilFluxTime, soilHeatFlux

def rainfall(fileName):
    print('Importing the rainfall data...')
    
    import numpy as np
    from datetime import datetime
    from datetime import timedelta
    import matplotlib.dates as mdates
    
    #Get file length:
    with open(fileName) as fileobject:
        file_length = sum(1 for line in fileobject)-1
    
    #Initialise arrays:
    rainfallTimeFine = np.empty(file_length)
    rainfallTips     = np.empty(file_length)
    rainfallTime     = np.empty(file_length//15)
    rainfallVolume   = np.empty(file_length//15)
    
     #Load the data from file
    with open(fileName) as fileobject:
        fileHeader = fileobject.readline()
        
        for i in range(0,file_length):
            row             = fileobject.readline().split(';')
            
            date            = datetime.strptime(row[1],'%m/%d/%y %I:%M:%S %p')
            
            rainfallTimeFine[i] = mdates.date2num(date)
            rainfallTips[i]     = float(row[5])
        
        rainfallTips = np.clip(rainfallTips, 0, 1)
        
        for i in range(0,file_length//15):
            tips  = 0
            for j in range(0,15):
                tips += rainfallTips[i*15+j]
                
            rainfallVolume[i] = tips*0.2*4 #Rainfall in mm/hr
            rainfallTime[i]   = rainfallTimeFine[i*15]
        
    return rainfallTimeFine, rainfallTips, rainfallTime, rainfallVolume