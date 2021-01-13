from river import stream
import utils

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


if __name__ == "__main__":
    case_dict ={}
    dataset = stream.iter_csv(
                './data/bpic2017.csv',
                drop=['(case) Accepted', '(case) ApplicationID', '(case) CreditScore', '(case) FirstWithdrawalAmount',
                '(case) MonthlyCost', '(case) NumberOfTerms', '(case) OfferedAmount', '(case) Selected',
                'Action', 'EventID', 'EventOrigin', 'OfferID', 'lifecycle:transition']
                )
    # ['Case ID', 'Activity', 'Resource', 'Complete Timestamp',  'activity', 'True label']
    key_pair = {
        'Case ID' : 'caseid',
        'Activity' : 'activity',
        'Resource' : 'resource',
        'Complete Timestamp' : 'ts'
    }
    for x,y in dataset:
        x = utils.dictkey_chg(x, key_pair)
        x = set_label(x)
        if 'True label' not in x.keys():
            caseid = x['caseid']
            x.pop('caseid')
            if caseid not in list(case_dict.keys()):
                case_dict[caseid] = [x]
            else:
                case_dict[caseid].append(x)
        # else:

    print(case_dict)
            

        
            