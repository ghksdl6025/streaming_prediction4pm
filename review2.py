import pandas as pd
import numpy as np
import math
pd.set_option('display.max_columns', 500)
df =pd.read_csv('./data/bac_online_back.csv')

groups = df.groupby('REQUEST_ID')
print(len(set(df['REQUEST_ID'])))
print(df.shape)
# dft =pd.read_csv('./data/bac_offline.csv')
small_caseid = np.random.choice(list(set(df['REQUEST_ID'])),10000,replace=False)
df_small = df[df['REQUEST_ID'].isin(small_caseid)]
groups = df_small.groupby('REQUEST_ID')

print(len(set(df_small['REQUEST_ID'])))
print(df_small.shape)
df_small.to_csv('./data/bac_online_back_small.csv',index=False)
# dft_small = dft[dft['REQUEST_ID'].isin(small_caseid)]

# df_small['START_DATE'] = pd.to_datetime(df_small['START_DATE'])
# df_small = df_small.sort_values(by='START_DATE')

# dft_small['START_DATE'] = pd.to_datetime(dft_small['START_DATE'])
# dft_small = dft_small.sort_values(by='START_DATE')

# # print(len(set(df['REQUEST_ID'])))
# print(df_small.shape)

# # print(len(set(dft['REQUEST_ID'])))
# print(dft_small.shape)

# df_small.to_csv('./data/bac_online_small.csv',index=False)
# dft_small.to_csv('./data/bac_offline_small.csv',index=False)


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


# groups = df.groupby('REQUEST_ID')

# outcome_number = {}
# for _, group in groups:
#     outcomelist= list(group['outcome'])
#     for o in outcomelist:
#         if type(o) ==  bool:
#             outcome =o
    
#     outcome_available = outcomelist.index(outcome)
#     if outcome_available not in list(outcome_number.keys()):
#         outcome_number[outcome_available] = {True:0,False:0}
#     outcome_number[outcome_available][outcome] +=1
# for t in sorted(list(outcome_number.keys())):
#     print(t,outcome_number[t][True], outcome_number[t][False])
# # print(outcome_number)
