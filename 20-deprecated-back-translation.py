import pandas as pd
from torch import nn
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tools import start_debugger_on_exception
from text_utils import split_by_fullstop
import threading
start_debugger_on_exception()
torch_device = 'cpu'
import glob
from pathlib import Path

zh2en = 'Helsinki-NLP/opus-mt-zh-en'
import glob
en2zh = 'Helsinki-NLP/opus-mt-en-zh'
'''
tokenizer_zh2en = AutoTokenizer.from_pretrained(zh2en)
tokenizer_en2zh = AutoTokenizer.from_pretrained(en2zh)

model_zh2en = AutoModelForSeq2SeqLM.from_pretrained(zh2en)

model_en2zh = AutoModelForSeq2SeqLM.from_pretrained(en2zh)

for model in [model_zh2en,model_en2zh]:

    model.to(torch_device)
'''
'''
def en_len(x):
    return tokenizer_en2zh.encode(x, return_tensors="pt").size(1)
def cut_string_en(input,max_len):
    return  cut_string(input,max_len,len_func = en_len)
def cut_string_zh(input,max_len):
    return  cut_string(input,max_len,len_func = len)
    
def cut_string(input,max_len,len_func):
    if len_func(input)<= max_len:
        return [input]
    else:
        s = split_by_fullstop(input)
        output = ['']
        for sen in s:
            if len_func(output[-1]+sen)>max_len:
                output.append('')
            else:
                output[-1] = output[-1]+sen
        return output
'''
def back_translation_batch(inputs,\
    tokenizer_zh2en,\
    tokenizer_en2zh,\
    model_en2zh,\
    model_zh2en, \
    torch_device='cuda:1',verbose = True,):
    # tokenizer_zh2en = AutoTokenizer.from_pretrained(zh2en)
    # tokenizer_en2zh = AutoTokenizer.from_pretrained(en2zh)
    # model_zh2en = AutoModelForSeq2SeqLM.from_pretrained(zh2en)
    # model_en2zh = AutoModelForSeq2SeqLM.from_pretrained(en2zh)
    # for model in [model_zh2en,model_en2zh]:

    #     model.to(torch_device)
    # import pdb;pdb.set_trace()
    import time
    
    try:
        
        #inputs= sum([cut_string_zh(input,512) for input in inputs], [])
        input_ids_zh = tokenizer_zh2en(inputs,return_tensors="pt",padding=True).to(torch_device)
        en = model_zh2en.generate(**input_ids_zh)
        decoded_en = [tokenizer_zh2en.decode(e, skip_special_tokens=True) for e in en]
        #decoded_en = sum([cut_string_en(x,512) for x in decoded_en], [])
        input_ids_en = tokenizer_en2zh(decoded_en,return_tensors="pt",padding=True).to(torch_device)#.prepare_seq2seq_batch(decoded_en)
        zh = model_en2zh.generate(**input_ids_en)
        decoded_zh = [tokenizer_en2zh.decode(z, skip_special_tokens=True) for z in zh]
        #import pdb;pdb.set_trace()
        return decoded_zh
    except:
        return [back_translation(input= input, \
        tokenizer_en2zh=tokenizer_en2zh,\
        tokenizer_zh2en = tokenizer_zh2en,\
        model_en2zh = model_en2zh,\
        model_zh2en = model_zh2en,\
        torch_device = torch_device) for input in inputs]
def back_translation(input,\
    tokenizer_zh2en,\
    tokenizer_en2zh,\
    model_en2zh,\
    model_zh2en, \
    torch_device='cuda:1'):
    #import pdb;pdb.set_trace()
    print('to single',torch_device)
    try:
        
        input_ids_zh = tokenizer_zh2en.encode(input, return_tensors="pt") 
        en = model_zh2en.generate(input_ids_zh.to(torch_device))
        decoded_en = tokenizer_zh2en.decode(en[0], skip_special_tokens=True)
        input_ids_en = tokenizer_en2zh.encode(decoded_en, return_tensors="pt")
        zh = model_en2zh.generate(input_ids_en.to(torch_device))
        decoded_zh = tokenizer_en2zh.decode(zh[0], skip_special_tokens=True) 
        return decoded_zh
    except:
        print('failed:',input)
        return ''
'''print(back_translation_batch(['有一回，鹿和马为了一块草地争吵得不可开交，各人都想将这块草地占为己有。最后鹿仗着自己那对厉害的角，终于战胜了马。',\
    '家庭是社会的细胞。有了健全的细胞，才会有一个健全的社会乃至一个健全强盛的国家。家庭首先由夫妻两个人组成。夫妻关系是人际关系中最密切最长久的一种。',\
    '我这一辈子，经过几个朝代，也已经过了八十几个\"年\"了！时代在前进，这过年的方式，也有很大的不同和进步。从我四五岁记事起到十一岁（那是在前清时代）过的是小家庭生活。'],\
    tokenizer_en2zh=tokenizer_en2zh,\
    tokenizer_zh2en = tokenizer_zh2en,\
    model_en2zh = model_en2zh,\
    model_zh2en = model_zh2en,verbose = False) )
print([back_translation(input=input,\
    tokenizer_en2zh=tokenizer_en2zh,\
    tokenizer_zh2en = tokenizer_zh2en,\
    model_en2zh = model_en2zh,\
    model_zh2en = model_zh2en) for input in ['有一回，鹿和马为了一块草地争吵得不可开交，各人都想将这块草地占为己有。最后鹿仗着自己那对厉害的角，终于战胜了马。',\
    '家庭是社会的细胞。有了健全的细胞，才会有一个健全的社会乃至一个健全强盛的国家。家庭首先由夫妻两个人组成。夫妻关系是人际关系中最密切最长久的一种。',\
    '我这一辈子，经过几个朝代，也已经过了八十几个\"年\"了！时代在前进，这过年的方式，也有很大的不同和进步。从我四五岁记事起到十一岁（那是在前清时代）过的是小家庭生活。']])
import pdb;pdb.set_trace()'''


def dataset_adaptive(batch_size, data):
    start = 0
    while start<len(data):
        lstart = len(data[min(start+10,len(data)-1)][1])
        bsize = int(batch_size/lstart)
        
        end = min(len(data),start+bsize)
        print('    lineno:',end)
        yield data[start:end]
        start = end

    # for i in range(int(len(data)/batch_size)):
    #     end = min(len(data),batch_size*(i+1))
    #     yield data[i*batch_size:end]

def dataset(batch_size, data):
    i = 0
    for i in range(int(len(data)/batch_size)):
        end = min(len(data),batch_size*(i+1))
        print('    lineno:',end)
        yield data[i*batch_size:end]
class  myThread (threading.Thread):
   def __init__(self, torch_device, batch,\
   tokenizer_zh2en,\
   tokenizer_en2zh,\
   model_en2zh,\
   model_zh2en, ):
      threading.Thread.__init__(self)
      self.torch_device = torch_device
      self.batch = batch
      self.tokenizer_en2zh=tokenizer_en2zh
      self.tokenizer_zh2en = tokenizer_zh2en
      self.model_en2zh = model_en2zh
      self.model_zh2en = model_zh2en
   def run(self):
       st = time.time()
       print ("Starting " + self.torch_device)
       process_data(batch = self.batch, torch_device = self.torch_device,\
       tokenizer_en2zh=self.tokenizer_en2zh,\
       tokenizer_zh2en = self.tokenizer_zh2en,\
       model_en2zh = self.model_en2zh,\
       model_zh2en = self.model_zh2en,)
       ed = time.time()
       print ("Exiting " + self.torch_device, 'time:',ed-st)

def process_data(batch, torch_device,\
    tokenizer_zh2en,\
    tokenizer_en2zh,\
    model_en2zh,\
    model_zh2en, ):
    inputs = [x[1] for x in batch]
    index = [x[0] for x in batch]
    t = back_translation_batch(inputs = inputs,\
    tokenizer_en2zh=tokenizer_en2zh,\
    tokenizer_zh2en = tokenizer_zh2en,\
    model_en2zh = model_en2zh,\
    model_zh2en = model_zh2en,\
    torch_device = torch_device,verbose = False)
    results[torch_device] = list(zip(index,t))

authors = [f.split('/')[-1].split('.')[0] for f in glob.glob('10-construct-csv-per-author/*.csv')]
devices = ['cuda:'+str(i) for i in [1,2,3,4,5,6,7]]
models_zh2en = {torch_device:AutoModelForSeq2SeqLM.from_pretrained(zh2en).to(torch_device) for torch_device in devices}
models_en2zh = {torch_device:AutoModelForSeq2SeqLM.from_pretrained(en2zh).to(torch_device) for torch_device in devices}

tokenizer_zh2en = AutoTokenizer.from_pretrained(zh2en)
tokenizer_en2zh = AutoTokenizer.from_pretrained(en2zh) 
results = {x:None for x in devices}
authors = ['jinyong','luxun','sanmao']
for author in authors:
    batch_size = 6*300
    df = pd.read_csv('10-construct-csv-per-author/'+author+'.csv')
    data = list(enumerate(df['text'].tolist() ))
    ds = dataset_adaptive(batch_size, data)
    
    translate = []
    for torch_device in devices:
        try:
            batch = next(ds)
        except:
            break
        thread = myThread(torch_device, batch, 
            tokenizer_zh2en,\
            tokenizer_en2zh,\
            models_en2zh[torch_device],\
            models_zh2en[torch_device], )
        # process_data(batch = batch, torch_device =torch_device,\
        #     tokenizer_en2zh=tokenizer_en2zh,\
        #     tokenizer_zh2en = tokenizer_zh2en,\
        #     model_en2zh = models_en2zh[torch_device],\
        #     model_zh2en = models_zh2en[torch_device],)
        results[torch_device] = 'running'
        thread.start()
    finish = False
    while not finish:
        time.sleep(0.1)
        run = False
        for torch_device in results.keys():
            if results[torch_device] is not None and results[torch_device]!='running':
                translate+=results[torch_device]
                results[torch_device]=None
                
                try:
                    batch = next(ds)
                    run = True
                except:
                    continue
                thread = myThread(torch_device, batch, 
                    tokenizer_zh2en,\
                    tokenizer_en2zh,\
                    models_en2zh[torch_device],\
                    models_zh2en[torch_device], )
                thread.start()
                results[torch_device] = 'running'
                
            
            elif results[torch_device] == 'running':
                run = True
        if run == False:
            finish = True
    # import pdb;pdb.set_trace()
    translate_sort = sorted(translate,key = lambda x: x[0])
    df['back_translation'] = pd.DataFrame({'translation':[x[1] for x in translate_sort]})
    path = '20-back-translation/'
    Path(path).mkdir(parents=True, exist_ok=True)
    df.to_csv(path+author+'.csv')
    # import pdb;pdb.set_trace()
# import pdb;pdb.set_trace() 
