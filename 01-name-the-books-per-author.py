import json

import glob
output = json.load(open('01-name-the-books-per-author.json','r'))
for f in glob.glob('00-grabdata/*.json'):
    author = f.split('/')[-1].split('.')[0]
    data = json.load(open(f,'r'))
    output.update({author:list(data.keys())})
with open('01-name-the-books-per-author.json','w') as f:
    json.dump(output,f,ensure_ascii=False,indent=4)


