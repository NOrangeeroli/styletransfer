import json,glob
from tools import start_debugger_on_exception
from pathlib import Path
import re
from text_utils import chinese_ratio
start_debugger_on_exception()
def split_para(x):
    if '|' in x:
        return x.split('|')
    elif '\n' in x:
        return x.split('\n')
    #elif '    ' in x:
    #    return x.split('    ')
    #elif '\\' in x and ('"'  in x or '“' not in x and '”' not in x:
    #    import pdb;pdb.set_trace()
    else:
        return [x]
def len_ch_check(x):
    if x != '':
        if  len(x)<=10:
            x = ''
        elif chinese_ratio(x)<0.6:
            x = ''
    return x
def clean_data(x):
    head_no = u'?？。，,”")）》'
    tail_no = u'"“《（('
    r_second_modify = re.compile(u'[^'+head_no+u'].*[^'+tail_no+u']',re.UNICODE)
    start = u'[^\u4E00-\u9FA5]{,30}'
    end = u'[^\u4E00-\u9FA5]{,30}'
    list_rep = [re.compile(start + u'小[^\u4E00-\u9FA5]{,20}说[^\u4E00-\u9FA5]{,20}天[^\u4E00-\u9FA5]{,20}堂'+end, re.UNICODE),\
                re.compile(start+u'[wWＷ][^\u4E00-\u9FA5]{,20}[wWＷ][^\u4E00-\u9FA5]{,20}[wWＷ][^\u4E00-\u9FA5]{,30}$', re.UNICODE),
                re.compile(start +u'[ＣcC][^\u4E00-\u9FA5]{,20}[oO][^\u4E00-\u9FA5]{,20}[mMＭ]'+end, re.UNICODE),
                re.compile(start +u'[tT][^\u4E00-\u9FA5]{,20}[xX][^\u4E00-\u9FA5]{,20}[tT][^\u4E00-\u9FA5]{,20}天[^\u4E00-\u9FA5]{,20}堂'+end, re.UNICODE),
                re.compile(start+u'xiaoshuotxt'+end,re.UNICODE),
                re.compile(u'mpanel(1);',re.UNICODE)
                ]
    list_del = [re.compile(u'读后感', re.UNICODE )]
    for rs in list_rep:
        ms = re.findall(rs,x)
        for m in ms:
            mm = re.search(r_second_modify,m).group()
           
            x = x.replace(mm,'')
    for rs in list_del:
        if re.search(rs,x) is not None:
            x = ''
    if x != '':
        if  len(x)<=10:
            x = ''
        elif chinese_ratio(x)<0.6:
            x = ''
    if "\\" in x and '"' not in x and '“' not in x and '”' not in x:
        #import pdb;pdb.set_trace()
        x= x.replace('\\','"')
    x = x.replace('“','"').replace('”','"')
    x = x.replace('    ','')
    return x
authors = [f.split('/')[-1].split('.')[0] for f in glob.glob('00-grabdata/*.json')]
def write_data_title_paragraph(author):
    f = '00-grabdata/'+author+'.json'
    data = json.load(open(f,'r'))
    output = {}
    leng = 0
    paras = 0
    docs = 0
    chaps = 0
    for title in data.keys():
        docs += 1
        output[title] = []
        chapter = data[title]
        for c in chapter:
            if 'content' in c.keys():
                content_str = 'content'
            elif 'text' in c.keys():
                content_str = 'text'
            c[content_str] = clean_data(c[content_str]) if isinstance(c[content_str],str) else [clean_data(x) for x in c[content_str]]
            if  isinstance(c[content_str],str):
                c['content'] = split_para(c[content_str])
            elif isinstance(c[content_str],list):
                c['content'] = c[content_str]
            else:
                assert False
            chaps +=1
            paras += len(c['content'])
            leng += sum([len(x) for x in c['content']])
            output[title]+=[x.strip() for x in c['content'] if len(x.strip())>1  and len_ch_check(x.strip()) != '']
    print('author:',author)
    print('    ','docs:',docs)
    print('    ','chaps:',chaps)
    print('    ','length:',leng)
    path = '00-grabdata/'+author
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(path+'/data.json','w') as f:
        json.dump(output,f,ensure_ascii=False,indent=4)
for author in authors:    
    write_data_title_paragraph(author=author)



            

