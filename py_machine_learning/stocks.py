import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style

style.use('dark_background')

path = 'intraQuarter';


gather=["Total Debt/Equity",
                      'Trailing P/E',
                      'Price/Sales',
                      'Price/Book',
                      'Profit Margin',
                      'Operating Margin',
                      'Return on Assets',
                      'Return on Equity',
                      'Revenue Per Share',
                      'Market Cap',
                        'Enterprise Value',
                        'Forward P/E',
                        'PEG Ratio',
                        'Enterprise Value/Revenue',
                        'Enterprise Value/EBITDA',
                        'Revenue',
                        'Gross Profit',
                        'EBITDA',
                        'Net Income Avl to Common ',
                        'Diluted EPS',
                        'Earnings Growth',
                        'Revenue Growth',
                        'Total Cash',
                        'Total Cash Per Share',
                        'Total Debt',
                        'Current Ratio',
                        'Book Value Per Share',
                        'Cash Flow',
                        'Beta',
                        'Held by Insiders',
                        'Held by Institutions',
                        'Shares Short (as of',
                        'Short Ratio',
                        'Short % of Float',
                        'Shares Short (prior '];

def Key_stats(gather):
    key_stats_path = path + '/_KeyStats';
    dir = [x[0] for x in os.walk(key_stats_path)];
    
    df = pd.DataFrame(columns = ['Date','Unix','Ticker', 'Price','Price_Pctchng','SP500', 'SP500_Pctchng','Difference', 'Status']);

    sp500_df = pd.read_csv('YAHOO-INDEX_GSPC.csv', index_col='Date')
    ticker_list = []
    for each_dir in dir[1:2]:
        files = os.listdir(each_dir);
        ticker = each_dir.split('\\')[1]

        old_stock_price_value = False
        old_SP500_value = False
        
        ticker_list.append(ticker);

        for file in files:
            date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html');
            unix_time = time.mktime(date_stamp.timetuple())
    
            try:
                source = ''
                print each_dir + '/' + file
                with open(each_dir + '/' + file, 'r') as f:
                    source = f.read();
                    source = source.replace('\n', '').replace('\r', '')

                feature_map = dict()
                try:
                    #value = float(source.split('Total Debt/Equity (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]);
                    dfs = pd.read_html(each_dir + '/' + file);
                    df_stats = pd.DataFrame();
                    for d in dfs:
                        try:
                            if(str(d[0][0]).startswith('Key')):
                                df_stats  = d[[0,1]]
                                for index, row in df_stats.iterrows():
                                    try:
                                        key = str(row[0])
                                        if key.endswith(':'):
                                            for feature in gather:    
                                                if key.startswith(feature):
                                                    val = str(row[1])
                                                    feature_map[feature] = val
                                                    break;
                                    except :
                                        pass
                                break;
                        except:
                                pass;
                except Exception as e:
                    pass

                try:
                    sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                    row = sp500_df[(sp500_df.index == sp500_date)]
                    sp500_value = float(row['Adjusted Close'])
                except  :
                    sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                    row = sp500_df[(sp500_df.index == sp500_date)]
                    sp500_value = float(row['Adjusted Close'])
                    pass

                try:
                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0]);
                except :
                    try:
                        stock_price_line = source.split('</small><big><b>')[1].split('</b></big>')[0];
                        stock_price = float(stock_price_line.split('>')[1].split('<')[0]);
                    except :
                        try:
                            stock_price = float(source.split('<span id="yfs_l84_'+ticker+'">')[1].split('</span>')[0]);
                        except Exception as e:
                            #print 'stock_price:' + str(e) + ' in ' + ticker + ' '+  file ;
                            pass
                if not old_stock_price_value:
                    old_stock_price_value = stock_price;
                if not old_SP500_value:
                    old_SP500_value = sp500_value;

                price_pctchng = ((stock_price - old_stock_price_value)/old_stock_price_value) * 100
                SP500_pctchng = ((sp500_value - old_SP500_value)/old_SP500_value) * 100
                diff = price_pctchng - SP500_pctchng;

                if diff > 0:
                    status =1
                else:
                    status =-1

                feature_map.update({'Date': date_stamp,
                                'Unix':unix_time,
                                'Ticker':ticker,
                                'Price' : stock_price,
                                'SP500' : sp500_value,
                                'Price_Pctchng' : price_pctchng,
                                'SP500_Pctchng':SP500_pctchng,
                                'Difference' : price_pctchng - SP500_pctchng,
                                'Status' : status
                                });
                df = df.append(feature_map, ignore_index=True);
            except Exception as e:
                #print str(e) + ' in ' + ticker + ' '+  file ;
                pass


    for ticker in ticker_list:
        plot_df = df[(df['Ticker'] == ticker)];
        plot_df.set_index('Date', inplace = True)

        if plot_df['Status'][-1] == 1 :
            color = 'g'
        else:
            color = 'r'

        plot_df['Difference'].plot(label = ticker, color = color);
        plt.legend();

    
    df.to_csv('out.csv');
    plt.show();

Key_stats(gather);
print 'Done'

