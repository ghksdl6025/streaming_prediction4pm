import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

# log = xes_importer.apply('../../Downloads/BPIC15_1.xes')
# dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
# dataframe.to_csv('./data/BPIC15_streaming2.csv',index=False)

df = pd.read_csv('./data/BPIC15_1prep.csv')

df = df.loc[:,['Case ID', 'Activity', 'Resource', 'Complete Timestamp']]
df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
df = df.sort_values(by='Complete Timestamp')

groups = df.groupby('Case ID')
concatlist = []
for _,group in groups:
    group = group.reset_index(drop=True)
    actlist = list(group['Activity'])
    progresslist = []
    outcomelist = []
    labelchecker = False
    eventtag = 'continue'
    outcome = None
    for act in range(len(actlist)):
        
        if 'send confirmation receipt' in actlist[:act] and actlist[act] =='retrieve missing data':
            outcome = True
        progresslist.append(eventtag)
        outcomelist.append(outcome)
    progresslist[-1]='end'
    # print(outcomelist)
    group['Outcome'] = outcomelist
    group['Progress'] = progresslist
    concatlist.append(group)

dfn = pd.concat(concatlist)            
print(dfn.head)
dfn.to_csv('./data/bpic15_streaming.csv',index=False)