# coding=gbk
import json,glob
import pinyin
from tools import start_debugger_on_exception
from nltk.translate import bleu_score as bleu
start_debugger_on_exception()
author_list = ['³Ѹ','������','����','��־Ħ','����','�ź�ˮ',\
'�Ű���','��ë','����','�ͽ�','������','����','���ݱ���','�ϸ���','������','����','������','����','ϯĽ��','������','��С�','Ǯ����','Ī��']#'����','�����'
author_male = ['³Ѹ','������','����','��־Ħ','�ź�ˮ','�ͽ�','������','����','������','Ǯ����','Ī��','�໪']
author_female = ['����','�Ű���','��ë','����','���ݱ���','�ϸ���','������','����','����','ϯĽ��','������','��С�']
luxun_zawen= ['������ѧ','���Ǽ�','����Ϧʰ','�ҽ�ͤ����','��ǻ������','��','���м�','α������','�ȷ�','���Ѽ�','׼����̸','���ļ�']
luxun_novel = ['�ź�','�����ռ�','�����±�','����']
xiaohong_novel = ['������','ţ����','�����������','���й�','����','����ɩ����','��Ұ�ĺ���','С������','�����Ӵ�','���н�','�����ƪС˵��','����']
xiaohong_zawen = ['����ɢ��']
zhuziqing_zawen = ['��','����','ŷ���Ӽ�','�ټ�','��Ӱ','�׶��Ӽ�']
laoshe_novel = ['è�Ǽ�','ƶѪ��','�Ĳ�ʿ','����','��������',\
    'С�µ�����','Ů��Ա','��','����','����ͬ��','����Ի',\
    '���ŵ���ѧ','���弯','�������ֵ�','���','����','�����ߵ�������',\
        '��������','Сľͷ�˶�','ţ��ʹ�','����һ����','ӣ����','΢��',\
            '������','�ϼ�']
laoshe_zawen=['�����Ĵ���','���ڳ���']
xuzhimo_novel=['����С˵��']
xuzhimo_zawen=['�������צ','�����ļ�','��üС��','��Ҷ']
zhanghenshui_novel = ['��������','���˶�','��ʮһ��','��ɽ����ףӢ̨','��˪��','ˮ��´�',\
    '���ӵǿ�','�����','�󽭶�ȥ','�ػ�����','������ʷ','��ϼ����','��ɽҹ��','�������',\
        'ֽ�����','��Ѫ֮��','��������','������','�����Ϸ�']
zhanghenshui_zawen = ['ɽ��СƷ']
def get_json_dejian_minzuo(author):
    files = glob.glob('/home/liuziqi/chinesestory/dejian_minzuo/book/*.json')
    luxun = {}
    for f in files:
        data = json.load(open(f,'r'))
        assert 'author' in data.keys()
        if data['author'] == author:
            print(data['title'])
            
            if author == '³Ѹ':
                filter = luxun_zawen+luxun_novel
            elif author == '����':
                filter = xiaohong_zawen+xiaohong_novel
            elif author == '������':
                filter = zhuziqing_zawen
            elif author == '����':
                filter = laoshe_novel+laoshe_zawen
            elif author == '��־Ħ':
                filter = xuzhimo_novel+xuzhimo_zawen
            elif author == '�ź�ˮ':
                filter = zhanghenshui_zawen+zhanghenshui_novel
            else :
                filter = []
            skip = False
            if filter != []:
                skip = True
                for name in filter:
                    if name in data['title']:
                        skip = False
            if skip:
                continue
            if data['title'] in luxun.keys():

                for c in data['chapter']:
                    if c['title']  in [x['title'] for x in luxun[data['title']]]:
                        assert False
                        continue
                    else:
                        luxun[data['title']].append(c)
                    print('    ',c['title'])
            else:
                luxun[data['title']] = []
                for c in data['chapter']:
                    luxun[data['title']].append(c)

    name = pinyin.get(author, format="strip", delimiter="")
    with open('00-grabdata/'+name+'.json','w') as f:
        json.dump(luxun,f,ensure_ascii=False,indent=4)




def get_json_auto(author):
    dic = json.load(open('00-author-files.json','r'))
    files = list(set(dic[author]))
    # files = glob.glob('/home/liuziqi/chinesestory/dejian_minzuo/book/*.json')
    luxun = {}
    text_temp = []
    for f in files:
        print(f)
        data = json.load(open(f,'r'))
        if 'books' in data.keys():
            continue
            
        if True:
            if 'С˵��' in data['title']:
                continue
            if ('�ļ�' in data['title'] or 'ȫ��' in data['title'] or '��Ʒ��' in data['title'] or 'ʫ�輯' in data['title']) and not (':' in data['title']  or '��' in data['title']):
                continue
            if 'chapter' in data.keys():
                str_chapter = 'chapter'
            elif 'chpater' in data.keys():
                str_chapter = 'chpater'
            else:
                assert False
                
            text = ''.join([x['text'] for x in data[str_chapter]])
            skip = False
            for t in text_temp:
                if bleu.sentence_bleu([list(t)],list(text))>0.8:
                    # print(f)
                    # assert False
                    skip = True

            if skip:
                continue
            text_temp.append(text)
            if data['title'] in luxun.keys():

                for c in data[str_chapter]:
                    if c['title']  in [x['title'] for x in luxun[data['title']]]:
                        # assert False
                        continue
                    else:
                        luxun[data['title']].append(c)
                    print('    ',c['title'])
            else:
                print(data['title'])
                luxun[data['title']] = []
                for c in data[str_chapter]:
                    print('    ',c['title'])
                    luxun[data['title']].append(c)

    name = pinyin.get(author, format="strip", delimiter="")
    
    with open('00-grabdata/'+name+'.json','w') as f:
        json.dump(luxun,f,ensure_ascii=False,indent=4)

'''
files = glob.glob('/home/liuziqi/chinesestory/**/*.json',recursive=True)
author_files = {}
author = []
for f in files:
    try:
        data = json.load(open(f,'r'))
    except:
        continue
    try:
        if True:
            try:
                author_files[data['author']].append(f)
            except:
                author_files[data['author']] = []
                author_files[data['author']].append(f)
            
            print(f)
        # print(data['author'])
        if data['author'] not in author:
            author.append(data['author'])
    except:
        continue
with open('00-author-files.json','w') as at:
    json.dump(author_files,at, ensure_ascii=False,indent=4)
'''
# dic_new = {}
'''
for author in ['³Ѹ','������','����','��־Ħ','����','�ź�ˮ']:
    get_json_dejian_minzuo(author)
for author in ['�Ű���','��ë','����','�ͽ�','������','����','���ݱ���','�ϸ���','������','����','������','����','ϯĽ��','������','��С�','Ǯ����','Ī��']:
    print(author)
    dic = json.load(open('00-author-files.json','r'))
    
    # dic_new[author] = sorted(dic[author])
    get_json_auto(author)
'''
for author in ['����','��ӹ','���ݱ���']:
    print(author)
    dic = json.load(open('00-author-files.json','r'))
    
    # dic_new[author] = sorted(dic[author])
    get_json_auto(author)    
# json.dump(dic_new,open('temp.json','w'), ensure_ascii=False,indent=4)
import pdb;pdb.set_trace()


