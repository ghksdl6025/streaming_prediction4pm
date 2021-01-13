from river import stream
import utils
import datetime
from encoding import prefix_bin


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

case_dict ={}
for x,y in dataset:
    # Event stream change dictionary keys
    x = utils.dictkey_chg(x, key_pair)

    # Event timestamp slice decimals
    x['ts'] = x['ts'][:-4]

    # Check label possible
    x = utils.set_label(x)

    # Allocate event stream to prefix bin class
    if 'True label' not in x.keys():
        caseid = x['caseid']
        x.pop('caseid')
        case_bin = prefix_bin()
        case_bin.set_caseid(caseid)

        if caseid not in list(case_dict.keys()):
            case_bin.set_start_ts(x['ts'])
            case_dict[caseid] = [case_bin]
        else:
            start_ts = case_dict[caseid][0].start_ts
            case_bin.set_start_ts(start_ts)
            case_dict[caseid].append(case_bin)
            
    # else:

print(case_dict['Offer_1064426652'][0].start_ts,case_dict['Offer_1064426652'][1].start_ts,case_dict['Offer_1064426652'][3].start_ts)
        

    
        