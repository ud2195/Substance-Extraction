# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:11:31 2019

@author: udayk
"""

import pandas as pd
import numpy as np
import spacy
import re

trainingdata=[]
def findindex(file,word,substance):
    for m in re.finditer(word, file):
         trainingdata.append((file,dict(entities=[tuple(( m.start(), m.end(),substance))])))

DIR='D:\\DownloadFiles_MetaDataDetialstext\\'

data=pd.read_excel(r'D:\DownloadFiles_MetaDataDetials\DownloadFiles_MetaDataDetials\FilesData.xlsx')

data.columns

data=data.dropna(axis=0,subset=['SubstanceManufacturer'])

substancemanufacturer=list(data['SubstanceManufacturer'])
filelist=list(data['File'])


for x,y in zip(filelist[0:2000],substancemanufacturer[0:2000]):
    try:
        file=open(DIR+x+'.txt',encoding='utf-8')
        file=file.read().lower()
        y=str(y)
        y=y.lower()
        findindex(file,y,'ORG')
    except Exception as e:
        print(e)
        pass
    

nlp2 = spacy.blank('en')

import random
ner = nlp2.create_pipe('ner')
nlp2.add_pipe(ner)
# Add a new label
ner.add_label('ORG')


nlp2.begin_training()
for i in range(10):
    # Shuffle the training data
    random.shuffle(trainingdata)
    # Create batches and iterate over them
    for batch in spacy.util.minibatch(trainingdata):
        # Split the batch in texts and annotations
        texts = [text for text, annotation in batch]
        annotations = [annotation for text, annotation in batch]
        # Update the model
        nlp2.update(texts, annotations)    
    
    
    
for x in filelist[2001:2524]:
        try:
            file=open(DIR+x+'.txt',encoding='utf-8')
            file=file.read()
            doc=nlp2(file)
            for ent in doc.ents:
                print(ent.text, ent.label_)
        except Exception as e:
            print(e)
            pass
                
c=[]   
for x in substancemanufacturer:
    if x not in substancemanufacturer[0:2000]:
        c.append(x)
        
        
substancemanufacturer[0:2000].index('jost chemical')        

nlp2.to_disk(r'D:\manufacturerner')

file=open(DIR+'manufacturer_9789fd49-9259-4cc2-862b-38fb5ccf21a9.pdf'+'.txt',encoding='utf-8')
file=file.read()
doc=nlp2(file)
for ent in doc.ents:
    print(ent.text, ent.label_)
    
SubstanceManufacturer=c    
df = pd.DataFrame({'col':SubstanceManufacturer})
print (df)    
df.columns = ['SubstanceManufacturer']

result = pd.merge(df,data[['File', 'SubstanceManufacturer']],on='SubstanceManufacturer')




for x in result['File']:
    #x=x.astype(str)
    try:
        file=open(DIR+x+'.txt',encoding='utf-8')
        file=file.read()
        doc=nlp2(file)
        for ent in doc.ents:
            result['prediction']=ent.text
    except Exception as e:
        print(e)
        pass
       
            

    
    
