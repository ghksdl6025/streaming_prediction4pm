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
trainset_prefix ={}
for x,y in dataset:
    # Event stream change dictionary keys
    x = utils.dictkey_chg(x, key_pair)

    # Event timestamp slice decimals
    x['ts'] = x['ts'][:-4]

    # Check label possible
    x = utils.set_label(x)

    # Initialize case by prefix length
    caseid = x['caseid']
    x.pop('caseid')
    case_bin = prefix_bin(caseid, x)

    # Allocate event stream to prefix bin class
    if 'True label' not in x.keys():
        if caseid not in list(case_dict.keys()):
            case_bin.set_prefix_length(1)    
            case_dict[caseid] = []
        else:
            case_bin.set_prefix_length(len(case_dict[caseid])+1)
            case_bin.set_prev_enc(case_dict[caseid][-1])
        case_bin.update_encoded()
        case_dict[caseid].append(case_bin)
            
    else:
        print('----------')
        for prefix in range(1,len(case_dict[caseid])):
            casebyprefix = case_dict[caseid][prefix]
            print(casebyprefix.prefix_length, casebyprefix.encoded)

    
        