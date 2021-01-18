'''
Utility functions used in training and pre-processing stage.
'''
import graphviz 

def save_graph_as_png(dot_string, output_file):
    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    if '/' in output_file:
        dir_add = output_file.split('/')[1]
        output_file = output_file.split('/')[2]
    g.format = 'png'
    g.filename = output_file
    g.directory = './img/' +dir_add
    g.render(view=False,cleanup=True)

    return g

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

def succ_aggr_enc(event,catattrs,prefix_length,prev_enc=None):
    '''
    Succeding aggregation encoding
    Aggregation encoding method along previously encoded case information in aggregation method

    Parameters
    ----------
    event: dictionary
        Nelwy added event
    
    catattrs: list
        List of categorical attributes

    prefi_length: int
        Current case prefix length

    prev_enc: class
        Previously streamed event case


    Returns
    ----------
    One hot encoded dictionary in aggregation based 
    '''
    if prev_enc == None:
        ohedict ={}
    else:
        
        ohedict = {x:prev_enc.encoded[x] for x in prev_enc.encoded.keys()}

    # Event duration average
    if 'duration_avg' not in list(ohedict.keys()):
        ohedict['duration_avg'] = 0
    else:
        # Current event duration
        duration = (event['ts'] - prev_enc.event['ts']).total_seconds()

        # Calculate average event duration | ((prev_avg)*(prefixlength -1) + duration)/prefixlength
        ohedict['duration_avg'] = (ohedict['duration_avg']*(prefix_length-1) + duration)/prefix_length

    # categorical attributes one hot encoding and counting
    for cat in catattrs:
        oheitem = cat+' '+event[cat]
        if oheitem not in list(ohedict.keys()):
            ohedict[oheitem] = 1
        else:
            ohedict[oheitem] +=1
        
    return ohedict

def invoke_cases_by_prefix(case_dict):
    '''
    Invoke encoded cases by given prefix length and return 

    Parameters
    ----------
    case_dict: Dictionary
        Dictionary with cases contains 'bin' class 
    
    prefix: int
        Prefix length to gather
    
    Return
    ----------
    Gathered encoded cases in dictionary
    '''
    for caseid in list(case_dict.keys()):
        for prefix in range(1,len(case_dict[caseid])):
            casebyprefix = case_dict[caseid][prefix]
            print(casebyprefix.prefix_length, casebyprefix.encoded)

def readjustment_training(dataset, feature_matrix):
    '''
    Readjustment on encoded dataset and extract feature matrix

    Parameters
    ----------
    training: list
        List of preprocessed 'bin' class

    Return
    ----------
    Training 
    '''
    # print(dataset)
    for feature in feature_matrix:
        if feature not in list(dataset.keys()):
            dataset[feature] = 0
    return dataset



if __name__== "__main__":
    test_event1 = {'activity': 'O_Accepted', 'resource': 'User_115', 'ts': '2016-01-29 21:33:14'}
    test_event2 = {'activity': 'O_Create Offer', 'resource': 'User_34', 'ts': '2016-01-29 21:41:06'}
    test_event3 = {'activity': 'O_Accepted', 'resource': 'User_115', 'ts': '2016-01-29 21:04:32'}

    catattrs = ['activity','resource']
    samp1 = succ_aggr_enc(test_event1,catattrs=catattrs,prefix_length=1)
    samp2 = succ_aggr_enc(test_event2,catattrs=catattrs,prefix_length=2,prev_enc= samp1)
    samp3 = succ_aggr_enc(test_event3,catattrs=catattrs,prefix_length=3,prev_enc= samp2)
    # print(samp1)
    # print(samp2)
    print(samp3)



