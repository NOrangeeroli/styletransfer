import json,glob

authors = ['laoshe','luxun','xiaohong','zhanghenshui','xuzhimo','zhuziqing']
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
            chaps +=1
            paras += len(c['content'])
            leng += sum([len(x) for x in c['content']])
            output[title]+=c['content']
    print('author:',author)
    print('    ','docs:',docs)
    print('    ','chaps:',chaps)
    print('    ','length:',leng)
    with open('00-grabdata/'+author+'/data.json','w') as f:
        json.dump(output,f,ensure_ascii=False,indent=4)
for author in authors:    
    write_data_title_paragraph(author=author)



            

