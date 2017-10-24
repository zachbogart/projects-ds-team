
# coding: utf-8

# In[148]:



################# READ ME ##################################
# usage:

### In new python notebook, import the function then run "parse_data" with parameters:

#   from fetchWeather import parse_data
#   parse_data(start_year,end_year,"stationID")

# Station ID lookup can be found here: ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-history.txt
# 725030-14732 = LGA

###########################################################


# get all weather points from specific URL. 

def fetch_weather_data(url):
    import urllib2
    import StringIO
    import gzip
    import pandas as pd

    # baseURL = "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/"
    # filename = "725030-14732-2016.gz"

    parse = [(0, 4),(4,7),(7,10),(10,13),(13,20),(20,25),(38,43),(44,49),(50,55),(56,61)]

    response = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO()
    compressedFile.write(response.read())

    compressedFile.seek(0)

    decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

    weather_hist = pd.read_fwf(filepath_or_buffer=decompressedFile, colspecs=parse, header=None)
    return weather_hist


# Get all weather data for specified station and years and parse into DataFrame. Returns one DF with all datapoints
    
def parse_data(start_year, end_year, stationID):
    import pandas as pd
    baseURL = "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/"

    col_names = ['year', 'month', 'day', 'hour', 'airtemp(C)', 'dewpoint(C)', 'windspeed(m/s)', 'skycoverage(code)', '1h-prec(mm)', '6h-prec(mm)']
    full_hist = pd.DataFrame()


    for year in range(start_year,end_year+1):
#         print baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz"
        try:
            year_hist = fetch_weather_data(baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz")
            full_hist = full_hist.append(year_hist)
        except:
            print "following URL was invalid: " + baseURL + str(year) + "/" + str(stationID) + "-" + str(year) + ".gz"
            print "make sure to enclose the stationID in quotes"

    full_hist.columns = col_names
    full_hist.to_csv(str(stationID)+"_"+str(start_year)+"-"+str(end_year)+"_data.csv")
