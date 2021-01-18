from river import stream,tree,metrics
import utils
import datetime
from encoding import prefix_bin
import csv

dataset = stream.iter_csv(
            './data/bpic2017.csv',
            drop=['(case) Accepted', '(case) ApplicationID', '(case) CreditScore', '(case) FirstWithdrawalAmount',
            '(case) MonthlyCost', '(case) NumberOfTerms', '(case) OfferedAmount', '(case) Selected',
            'Action', 'EventID', 'EventOrigin', 'OfferID', 'lifecycle:transition']
            )
totallength = len(list(dataset))


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
feature_matrix ={}
casecount = 0
rowcounter = 0
resultdict ={}
# Feature matrix extraction with grace period

for x,y in dataset:
    if rowcounter%1000 == 0:
        print(rowcounter*100/totallength ,'%', 'Case finished: %s'%(casecount))
    rowcounter +=1
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

    # Adding newly finished case to training set.    
    else:
        casecount +=1

        # Grace period to collect feature matrix
        if casecount <200:
            case_length = len(case_dict[caseid])
            for prefix in range(1, case_length):
                if 'prefix_%s'%(prefix+1) not in list(feature_matrix.keys()):
                    feature_matrix['prefix_%s'%(prefix+1)]=set()
                    # Initialize classifier and performance matrix and updating count
                    trainset_prefix['prefix_%s'%(prefix+1)] = [tree.HoeffdingTreeClassifier(max_depth=5),metrics.Accuracy(), 0]
                feature_list = list(case_dict[caseid][prefix].encoded.keys())
                for x in feature_list: feature_matrix['prefix_%s'%(prefix+1)].add(x) 
            case_dict.pop(caseid)               

        # Real training start
        else:
            # Modify encoded attributes of cases with feature matrix
            case_length = len(case_dict[caseid])
            y = x['True label']
            for prefix in range(1, case_length):
                if case_dict[caseid][prefix].grace_updated == False:
                    case_dict[caseid][prefix].encoded = utils.readjustment_training(case_dict[caseid][prefix].encoded, feature_matrix['prefix_%s'%(prefix+1)])
                    case_dict[caseid][prefix].update_grace_status(True)
                x = case_dict[caseid][prefix].encoded
                model = trainset_prefix['prefix_%s'%(prefix+1)][0]
                model.learn_one(x,y)
                trainset_prefix['prefix_%s'%(prefix+1)][2] +=1

                for cases in list(case_dict.keys()):
                    if len(case_dict[cases]) >prefix:
                        if case_dict[cases][prefix].grace_updated ==False:
                            case_dict[cases][prefix].encoded = utils.readjustment_training(case_dict[cases][prefix].encoded, feature_matrix['prefix_%s'%(prefix+1)])
                            case_dict[cases][prefix].update_grace_status(True)
                        x_test = case_dict[cases][prefix].encoded
                        y_pred = model.predict_one(x_test)
                        case_dict[cases][prefix].update_prediction((trainset_prefix['prefix_%s'%(prefix+1)][2], y_pred))
            resultdict[caseid] = case_dict.pop(caseid)

    if casecount > 200 and rowcounter%1000 == 0:
        for prefix in trainset_prefix.keys():
            model = trainset_prefix[prefix][0]
            outputfile = './%s/%s.png'%(prefix, round(rowcounter*100/totallength,2))
            utils.save_graph_as_png(model.draw(),outputfile)

            #   case_dict[cases][prefix].encoded = utils.readjustment_training(case_dict[cases][prefix].encoded, feature_matrix['prefix_%s'%(prefix+1)])