import json,glob
import pandas as pd



def gen_dataset():
    files= glob.glob('00-grabdata/*/data.json')
    output = pd.DataFrame()
    for f in files:
        author = f.split('/')[-2]
        with open(f,'r') as fi:
            data=json.load(fi)
            for title in data.keys():
                entries = [{'title':title,'text': x }for x in data[title]]
                temp = pd.DataFrame(entries)
                temp['author'] = author
                vor = len(output)
                output = output.append(temp)
                nach = len(output)
                assert nach-vor == len(temp)
    output.to_csv('10-construct-dataset.csv')
    import pdb;pdb.set_trace()

gen_dataset()