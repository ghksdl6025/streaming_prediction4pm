import pandas as pd
from collections import Counter
pd.set_option('display.max_columns', 500)
df = pd.read_csv('./data/bac.csv')
print(df.head)
print(df.columns.values)

# df = df.sort_values(by='Complete Timestamp')
groups= df.groupby('REQUEST_ID')
trueminlen = {}
concating = []
for _, group in groups:
    group = group.reset_index(drop=True)
    actlist = list(group['ACTIVITY'])
    # 'Back-Office Adjustment Requested'
    # 'Pending Request for acquittance of heirs'
    outcomelist = []
    outcome=None
    for act in actlist[:-1]:
        if act =='Pending Request for acquittance of heirs':
            outcome=True
        outcomelist.append(outcome)
    if actlist[-1] != 'Pending Request for acquittance of heirs' and outcome ==None:
        outcomelist.append(False)
    elif actlist[-1] == 'Pending Request for acquittance of heirs':
        outcomelist.append(True)
    elif outcome == True:
        outcomelist.append(True)
    group['outcome'] = outcomelist

    # concating.append(group)
    if True in outcomelist:
        if outcomelist.index(True) not in trueminlen.keys():
            trueminlen[outcomelist.index(True)] =1
        else:
            trueminlen[outcomelist.index(True)] +=1
        
print(trueminlen)
sortedkey = sorted(trueminlen.keys())
for t in sortedkey:
    print(t,':',trueminlen[t])
# dfn = pd.concat(concating)
# dfn.to_csv('./data/bac_online.csv',index=False)