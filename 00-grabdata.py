import json,glob
from tools import start_debugger_on_exception
start_debugger_on_exception()
author_list = ['鲁迅','朱自清','老舍','徐志摩','萧红','张恨水']#'胡适','瞿秋白'
luxun_zawen= ['花边文学','华盖集','朝花夕拾','且介亭杂文','南腔北调集','坟','三闲集','伪自由书','热风','而已集','准风月谈','二心集']
luxun_novel = ['呐喊','狂人日记','故事新编','彷徨']
xiaohong_novel = ['生死场','牛车上','家族以外的人','北中国','弃儿','王阿嫂的死','旷野的呼喊','小城三月','呼兰河传','商市街','萧红短篇小说集','马伯乐']
xiaohong_zawen = ['萧红散文']
zhuziqing_zawen = ['春','你我','欧游杂记','踪迹','背影','伦敦杂记']
laoshe_novel = ['猫城记','贫血集','文博士','集外','骆驼祥子',\
    '小坡的生日','女店员','蜕','火葬','四世同堂','赵子曰',\
    '老张的哲学','蛤藻集','秦氏三兄弟','离婚','二马','无名高地有了名',\
        '正红旗下','小木头人儿','牛天赐传','我这一辈子','樱海集','微神集',\
            '月牙集','赶集']
laoshe_zawen=['北京的春节','出口成章']
xuzhimo_novel=['轮盘小说集']
xuzhimo_zawen=['巴黎的鳞爪','自剖文集','爱眉小札','落叶']
zhanghenshui_novel = ['魍魉世界','美人恩','八十一梦','梁山伯与祝英台','傲霜花','水浒新传',\
    '五子登科','蜀道难','大江东去','秦淮世家','春明外史','落霞孤鹜','巴山夜雨','金粉世家',\
        '纸醉金迷','热血之花','虎贲万岁','满江红','北雁南飞']
zhanghenshui_zawen = ['山窗小品']
def get_json_dejian_minzuo(author):
    files = glob.glob('/home/liuziqi/chinesestory/dejian_minzuo/book/*.json')
    luxun = {}
    for f in files:
        data = json.load(open(f,'r'))
        assert 'author' in data.keys()
        if data['author'] == author:
            print(data['title'])
            
            if author == '鲁迅':
                filter = luxun_zawen+luxun_novel
            elif author == '萧红':
                filter = xiaohong_zawen+xiaohong_novel
            elif author == '朱自清':
                filter = zhuziqing_zawen
            elif author == '老舍':
                filter = laoshe_novel+laoshe_zawen
            elif author == '徐志摩':
                filter = xuzhimo_novel+xuzhimo_zawen
            elif author == '张恨水':
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

    if author == '鲁迅':
        name = 'luxun'  
    elif author == '萧红':
        name = 'xiaohong'
    elif author == '朱自清':
        name = 'zhuziqing'
    elif author == '老舍':
        name = 'laoshe'
    elif author == '徐志摩':
        name = 'xuzhimo'
    elif author =='张恨水':
        name = 'zhanghenshui'
    else:
        name = 'temp'
    with open('00-grabdata/'+name+'.json','w') as f:
        json.dump(luxun,f,ensure_ascii=False,indent=4)
    

files = glob.glob('/home/liuziqi/chinesestory/**/*.json',recursive=True)

author = []
for f in files:
    data = json.load(open(f,'r'))
    try:
        if data['author'] in ['金庸','jinyong','JINYONG','Jinyong',\
            '古龙','gulong','GULONG','Gulong',\
                '冰心','bingxin','BINGXIN','Bingxin',\
                    '三毛','sanmao','SANMAO','Sanmao',\
                        '郭敬明','guojingming','GUOJINGMING','Guojingming',\
                            '韩寒','hanhan','Hanhan','HANHAN',\
                                '安妮宝贝','annibaobei','ANNIBAOBEI','Annibaobei']:
            print(f)
        # print(data['author'])
        if data['author'] not in author:
            author.append(data['author'])
    except:
        continue
import pdb;pdb.set_trace()

