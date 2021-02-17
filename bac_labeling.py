import pandas as pd
from tqdm import tqdm
pd.set_option('display.max_columns', 500)
df = pd.read_csv('./data/bac.csv')
df['START_DATE'] = pd.to_datetime(df['START_DATE'])
df = df.sort_values(by='START_DATE')
actvivity_occurance = ['Authorization Requested', 'Pending Request for acquittance of heirs', 'Back-Office Adjustment Requested']

groups = df.groupby('REQUEST_ID')
counting = 0
concating = []
concating2 = []
actlocationset = {}
for _,group in tqdm(groups):
    group = group.reset_index(drop=True)
    actlist = list(group['ACTIVITY'])
    outcome =False
    if 'Authorization Requested' in actlist:
        outcome=True
        act_location = actlist.index('Authorization Requested')
        if act_location not in list(actlocationset.keys()):
            actlocationset[act_location] = 1
        else:
            actlocationset[act_location] += 1
    else:
        group.loc[len(group)-1,'outcome'] = outcome

print(actlocationset)



'''
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
    outcome = 'None'
    for act in range(len(actlist)):
        
        if 'send confirmation receipt' in actlist[:act] and actlist[act] =='retrieve missing data':
            outcome = True
        progresslist.append(eventtag)
        outcomelist.append(outcome)
    progresslist[-1]='end'
    # print(outcomelist)
    if outcomelist[-1] =='None':
        outcomelist[-1] =False
    group['Outcome'] = outcomelist
    group['Progress'] = progresslist
    concatlist.append(group)

dfn = pd.concat(concatlist).sort_values(by='Complete Timestamp')
print(dfn.head)
dfn.to_csv('./data/bpic15_streaming.csv',index=False)
'''