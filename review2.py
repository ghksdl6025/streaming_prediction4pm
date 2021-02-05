import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 500)
df =pd.read_csv('./data/bac_online.csv')
small_caseid = np.random.choice(list(set(df['REQUEST_ID'])),5000)
df_small = df[df['REQUEST_ID'].isin(small_caseid)]
df_small['START_DATE'] = pd.to_datetime(df_small['START_DATE'])
df_small = df_small.sort_values(by='START_DATE')
print(df_small.shape)
df_small.to_csv('./data/bac_online_small.csv',index=False)

dfn = pd.read_csv('./data/bac_offline.csv')
dfn_small = dfn[dfn['REQUEST_ID'].isin(small_caseid)]
print(dfn_small.shape)
dfn_small.to_csv('./data/bac_offline_small.csv',index=False)

# df = df[df['REQUEST_ID']==20176000338]
# df['START_DATE'] = pd.to_datetime(df['START_DATE'])
# df = df.rename(columns={'REQUEST_ID':'caseid','ACTIVITY':'activity','START_DATE':'ts','CE_UO':'resource'})
# df = df.loc[:,['caseid','activity','ts','resource','outcome']]

def filter_by_prefix(df,prefix):
    '''
    Filter case by prefix length
    
    Parameters
    ----------
    df : pandas dataframe
        Assigned dataframe to slice by prefix length
    
    prefix : int
        Prefix length to slice to cases in fixed length
    
    Returns
    ----------
    Return dataframe with sliced cases
    '''
    df['ts'] = pd.to_datetime(df['ts'])
    groups = df.groupby('caseid')
    encoded_df=[]
    for case,group in groups: 
        group = group.reset_index(drop=True)
        if len(group)>prefix:
            group = group.loc[:prefix-1,:]
            encoded_df.append(group)
    return pd.concat(encoded_df)

# groups = df.groupby('caseid')
# concating = []
# for _, group in groups:
#     outcomelist = list(group['outcome'])
#     outcome = outcomelist[-1]
#     group = group.reset_index(drop=True)
#     if True in outcomelist:
#         group = group.loc[:outcomelist.index(True),:]
#     group['outcome'] = outcome
#     concating.append(group)

# df = pd.concat(concating)

# t = filter_by_prefix(group,10)
# print(t)
# print(set(t['outcome']))
