import pandas as pd
import os
import time
from datetime import datetime


path = 'intraQuarter';

def Key_stats():
    key_stats_path = path + '/_KeyStats';
    dir = [x[0] for x in os.walk(key_stats_path)];
    
    df = pd.DataFrame(columns = ['Date','Unix','Ticker','DE Ratio']);

    for each_dir in dir[1:5]:
        files = os.listdir(each_dir);
        ticker = each_dir.split('\\')[1]
        for file in files:
            date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html');
            unix_time = time.mktime(date_stamp.timetuple())

            #dfs = pd.read_html(each_dir + '/' + file);
            #balence_sheet = pd.DataFrame();
            #for df in dfs:
            #    if(df[0][0] == 'Balance Sheet' and df[0][4].startswith('Total Debt/Equity')):
            #        balence_sheet = df;
            #        break;
            #if balence_sheet.empty:
            #    print 'Error : ' + each_dir + '/' + file;
            
            try:
                with open(each_dir + '/' + file, 'r') as f:
                    source = f.read();
                    value = float(source.split('Total Debt/Equity (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]);
                    df = df.append({'Date': date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value}, ignore_index=True);
            except  :
                pass

    df.to_csv('out.csv');

Key_stats();
print 'Done'

