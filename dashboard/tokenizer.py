import pandas as pd
import re
import spacy
import json
import string
from spacy.lang.en.stop_words import STOP_WORDS




with open('cont_en.json') as file:
    contEn = json.load(file)
    
c_re = re.compile('(%s)' % '|'.join(contEn.keys()))

def expandContractions(text, c_re=c_re):         # expanding contractiion into full form word. ex: won't -> will not
    def replace(match):
        return contEn[match.group(0)]
    return c_re.sub(replace, text.lower())

def stars(text):
    if '*' in text:
        word = text.replace('*',' stars') # replacing * symbol with "star"
    else:
        word = text
    return word

def num2word(text):                        #convert number to string
    if len(text) == 1 and text in '12345':
        if text == '1':
            word = 'one'
        elif text == '2':
            word = 'two'
        elif text == '3':
            word = 'three'
        elif text == '4':
            word = 'four'
        elif text == '5':
            word = 'five'
        else:
            word = text
    else:
        word = text
    return word

def lemma(word):
    lemma_doc = nlp(" ".join(word)) 
    lemma_text = [token.text if '_' in token.text else token.lemma_ for token in lemma_doc]
    return lemma_text

nlp = spacy.load("en_core_web_sm")

nlp.Defaults.stop_words -= {"one", "two","three","four","five"} #removing these word from stop_word
stopword = list(STOP_WORDS)

stopword2 = stopword
stopword2.extend(['good'])

def clean_text(text):
    text = stars(text)
    text = expandContractions(text)
    text = re.split(r'\W+',text)
    text = [num2word(x) for x in text]
    text = [x for x in text if x not in string.punctuation]
    text = ["have" if x == "ve" else x for x in text]
    text = ["game" if x == "games" else x for x in text]
    text = ["phone" if x == "mobile" else x for x in text]
    text = ' '.join(text).replace('one one','1.1').split()
    text = [x for x in text if x not in stopword2 and len(x) > 1 and len(x) <= 45]
    return text

def tokenizer(bow):
    text = clean_text(bow)
    text = lemma(text) #,allowed_postags=['NOUN','VERB']
    return text