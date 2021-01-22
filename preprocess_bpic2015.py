import pandas as pd

df = pd.read_csv('./data/BPIC15_1prep.csv')

df = df.loc[:,['Case ID', 'Activity', 'Resource', 'Complete Timestamp']]
df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
df = df.sort_values(by='Complete Timestamp')

groups = df.groupby('Case ID')
lastact =set()
for _,group in groups:
    actlist = list(group['Activity'])
    if 'send confirmation receipt' in list(group['Activity']) and 'retrieve missing data' in list(group['Activity']):
        if actlist.index('send confirmation receipt') <  actlist.index('retrieve missing data'):
            print(actlist.index('retrieve missing data')-actlist.index('send confirmation receipt'))

    