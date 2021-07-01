import json,glob
import pandas as pd
from pathlib import Path
from tools import start_debugger_on_exception
from utils import sentence_split_zh,cut_string_zh,soft_cut_string_zh
start_debugger_on_exception()

def gen_dataset(author = None):
    files= glob.glob('00-grabdata/'+author+'/data.json')
    output = pd.DataFrame()
    for f in files:
        with open(f,'r') as fi:
            data=json.load(fi)
            for title in data.keys():
                entries = [{'title':title,'text': x }for x in sum([cut_string_zh(x,300) for x in data[title]],[])]
                print(title,len(entries))
                temp = pd.DataFrame(entries)
                temp['author'] = author
                vor = len(output)
                output = output.append(temp)
                nach = len(output)
                assert nach-vor == len(temp)
    if len(output) == 0:
        return
    output['len'] = output['text'].apply(len)
    output = output[output['len']>20]
    output = output.sort_values(by = 'len')[['title','text','author']]
    #output = output.sample(frac=1).reset_index(drop=True)
    output = output[output.text.apply(lambda x: x[-1] in list('。？！.?!……"”'))]
    path = '10-construct-csv-per-author/'
    Path(path).mkdir(parents=True, exist_ok=True)
    output.to_csv(path+author+'.csv')
    #import pdb;pdb.set_trace()
authors = [f.split('/')[-2] for f in glob.glob('00-grabdata/*/data.json')]
# authors = ['zhangailing']
for author in authors:
    gen_dataset(author)
