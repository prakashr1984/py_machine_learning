import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import matplotlib.style as style

style.use('ggplot')

def get_stock(stock):
    stock_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=10y/csv'

    source_code = urllib.urlopen(stock_url).read().decode()
    source_split = source_code.split('\n')

    source_data = []
    i = 18
    while i < len(source_split):
        if source_split[i]:
            source_data.append(source_split[i])
        i+=1

    strconverter = mdates.strpdate2num('%Y%m%d');
    date, closep, highp, lowp, openp, volume = np.loadtxt(source_data
                                                          , unpack = True
                                                          , delimiter = ','
                                                          , converters = {0 : lambda x : strconverter(x)});

    fig = plt.Figure()
    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=1, colspan=1)
    plt.title('Stock Prices for ' + stock)
    plt.ylabel('high/low')
    ax2 = plt.subplot2grid((6,1),(1,0), rowspan=4, colspan=1, sharex = ax1)
    plt.ylabel('Close price')
    ax2v = ax2.twinx()

    ax3 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex = ax1)
    plt.ylabel('close/open')

    ax1.plot_date(date,list(map(lambda x,y : x - y, highp,lowp)), '-', label = 'high - low', color='b')
    ax2.plot_date(date,closep, '-', label = 'closep', color = 'g', alpha=0.3)
    ax2.fill_between(date,closep[0],closep, where = (closep > closep[0]) , facecolor='g', alpha=0.3)
    ax2.fill_between(date,closep[0],closep, where = (closep < closep[0]) , facecolor='r', alpha=0.3)
    ax2v.fill_between(date,0,volume, facecolor='b', alpha=0.3)
    ax2v.yaxis.set_ticklabels([]);
    ax2v.set_ylim(0,3*max(volume));
    ax3.plot_date(date,list(map(lambda x,y : x - y, closep,openp)), '-', label = 'close - open')

    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45);

    ax2.grid(True)

    

    
    
    plt.legend()
    plt.show()

data = get_stock('EBAY')