import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tools import start_debugger_on_exception
from utils import split_by_fullstop
start_debugger_on_exception()
df = pd.read_csv('10-construct-dataset.csv')
zh2en = 'Helsinki-NLP/opus-mt-zh-en'
en2zh = 'Helsinki-NLP/opus-mt-en-zh'
tokenizer_zh2en = AutoTokenizer.from_pretrained(zh2en)
tokenizer_en2zh = AutoTokenizer.from_pretrained(en2zh)

model_zh2en = AutoModelForSeq2SeqLM.from_pretrained(zh2en)
model_en2zh = AutoModelForSeq2SeqLM.from_pretrained(en2zh)
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
def back_translation(input,verbose = True):
    #import pdb;pdb.set_trace()
    if verbose:
        print(input.index)
    input = input['text']
    
    import time
    st = time.time()
    input = cut_string_zh(input,512)
    input_ids_zh = [tokenizer_zh2en.encode(i, return_tensors="pt") for i in input]
    en = [model_zh2en.generate(i) for i in input_ids_zh]
    #decoded_en = [tokenizer_zh2en.decode(e[0], skip_special_tokens=True) for e in en]
    #decoded_en = sum([cut_string_en(x,512) for x in decoded_en], [])
    input_ids_en = en#  [tokenizer_en2zh.encode(i, return_tensors="pt") for i in decoded_en]
    zh = [model_en2zh.generate(i) for i in input_ids_en]
    decoded_zh = [tokenizer_en2zh.decode(i[0], skip_special_tokens=True) for i in zh]
    ed = time.time()
    print(ed-st)
    return ''.join(decoded_zh)

#print(back_translation({'text':'有一回，鹿和马为了一块草地争吵得不可开交，各人都想将这块草地占为己有。最后鹿仗着自己那对厉害的角，终于战胜了马。','index':0},verbose = False) )

df['back_translation'] = df.apply(back_translation,axis = 1)
df.to_csv('20-back-translation.csv')
import pdb;pdb.set_trace() 
