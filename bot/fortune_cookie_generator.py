# -*- coding: utf-8 -*-
"""
Created on Fri May  5 16:15:34 2023

@author: frenc
"""

# minimal load

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


gmodeldir = '.\model_save5'
bmodeldir = '.\model_save1'

device = torch.device("cpu")


gtokenizer = GPT2Tokenizer.from_pretrained(gmodeldir)
gmodel = GPT2LMHeadModel.from_pretrained(gmodeldir)

btokenizer = GPT2Tokenizer.from_pretrained(bmodeldir)
bmodel = GPT2LMHeadModel.from_pretrained(bmodeldir)


def good_fortune_gen():

    
    gmodel.eval()
    
    prompt = "<|startoftext|>"
    
    generated = torch.tensor(gtokenizer.encode(prompt)).unsqueeze(0)
    generated = generated.to(device)
    
    model_output = gmodel.generate(generated, 
                                  do_sample=True,   
                                  top_k=1000, 
                                  max_length = 40,
                                  top_p=0.99, 
                                  num_return_sequences=1
                                  )
    
    fortune = str(gtokenizer.decode(model_output[0], skip_special_tokens=True))
    return fortune

def bad_fortune_gen():

    
    bmodel.eval()
    
    prompt = "<|startoftext|>"
    
    generated = torch.tensor(btokenizer.encode(prompt)).unsqueeze(0)
    generated = generated.to(device)
    
    model_output = bmodel.generate(generated, 
                                  do_sample=True,   
                                  top_k=1000, 
                                  max_length = 40,
                                  top_p=0.99, 
                                  num_return_sequences=1
                                  )
    
    fortune = str(btokenizer.decode(model_output[0], skip_special_tokens=True))
    return fortune

#%%

fort = good_fortune_gen()
print('good fortune')
print(fort)

fort = bad_fortune_gen()
print('bad fortune')
print(fort)
