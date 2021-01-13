'''
Utility functions used in training and pre-processing stage.
'''
def dictkey_chg(dictionary, key_pair):
    '''
    Change dictionary key from old to new according to key_pair

    Parameters
    ----------
    dictionary : Dictionary
        dictionary to modify

    key_pair : Dictionary
        key pair with old (key) and new (value)

    Return
    ----------
    Modified dictionary
    '''
    for old_key in list(key_pair.keys()):
        dictionary[key_pair[old_key]] = dictionary.pop(old_key)
    return dictionary

def set_label(data):
    '''
    From given data, set case label if condition satisfied.
    Return data with case label y.

    Parameters
    ----------
    data : dictionary
    Streaming data

    Return
    ----------
    data : updated dictionary
    '''
    y = ''
    if 'Cancelled' in data['activity']:
        y = 'Cancelled'
    elif 'Accepted' in data['activity']:
        y = 'Accepted'
    elif 'Refused' in data['activity']:
        y = 'Refused'

    if len(y) >=1:
        data['True label'] =y
    return data

def aggregation_encoding(df):
    '''
    Aggregation encoding
    
    Parameters
    ----------
    df : pandas dataframe
        Assigned dataframe to encode for outcome prediction
    
    prefix : int
        Prefix length to slice to cases in fixed length
    
    Returns
    ----------
    Return dataframe encoded in aggregation method
    '''
    df['ts'] = pd.to_datetime(df['ts'])
    groups = df.groupby('caseid')
    encoded_df=[]
    for case,group in groups: 
        group = group.reset_index(drop=True)
        outcome = set(group['outcome']).pop()
        cumdurationlist = [(x - list(group['ts'])[0]).total_seconds() for x in list(group['ts'])]
        case_time_outcome = {'caseid':case, 'ts':np.mean(cumdurationlist),'outcome':outcome}
        activity_count = {x: list(group['activity']).count(x) for x in set(group['activity'])}
        resource_count = {x: list(group['resource']).count(x) for x in set(group['resource'])}

        case_time_outcome.update(activity_count)
        case_time_outcome.update(resource_count)
        dfk = pd.DataFrame.from_dict([case_time_outcome])
        encoded_df.append(dfk)
    concated_df = pd.concat(encoded_df)
    concated_df = concated_df.fillna(0)
    return concated_df