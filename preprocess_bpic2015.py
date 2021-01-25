import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as log_converter

# log = xes_importer.apply('../../Downloads/BPIC15_1.xes')
# dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
# dataframe.to_csv('./data/BPIC15_streaming2.csv',index=False)

df = pd.read_csv('./data/BPIC15_1prep.csv')

df = df.loc[:,['Case ID', 'Activity', 'Resource', 'Complete Timestamp']]
df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
df = df.sort_values(by='Complete Timestamp')

groups = df.groupby('Case ID')
lastact =set()
for _,group in groups:
    actlist = list(group['Activity'])
    progresslist = []
    labelchecker = False
    for act in actlist[:-1]:
        if act == 'send confirmation receipt':
            labelchecker =True
        if labelchecker == True and act =='retrieve missing data':
            progresslist.append('end')
            break
        progresslist.append('continue')
    if labelchecker ==False:
        progresslist.append('end')
    if len(actlist) != len(progresslist):
        print(actlist)
        print(progresslist)

            
            
    progresslist.append('end')

    


            

    