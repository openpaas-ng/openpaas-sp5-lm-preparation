#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom
from unicodedata import normalize
from sys import argv
from num2words import num2words
import re
import os.path

def transformation_text(text):
    bool=True
    #print text
    #or "(" in text
    # Remove Line when : ### | $$$ | Particular Pronunciation | Amorse | BIP | Sylable incompréhensible
    #len(re.findall(r"\w+-[^\w+]|\w+-$",text))
    if "###" in text or len(re.findall(r"\[.+\]",text))>0 or len(re.findall(r"\w+-[^\w+]|\w+-$",text))>0 or len(re.findall(" -\w+",text))>0 or len(re.findall(r"\¤",text))>0 or len(re.findall(r"/.+/",text))>0:
        #print text
        #print "Ligne Supprimé"
        bool=False
    else:
    # 4x4
        text=re.sub(r"4x4","quatre fois quatre",text)
    #convert number if exist : OK
        num_list=re.findall(" \d+ ",text)
        if len(num_list)>0:
            for num in num_list:
                num_in_word=num2words(int(num), lang='fr')
                text=normalize('NFKD', text.replace(num,num_in_word)).encode('utf-8', 'ignore')
    # replace silence character with <sil> : OK
        #text=re.sub(r"(\+)", "<sil>", text)
        #text=re.sub(r"(///)", "<sil>", text)
    # remove silence character : OK
        text=re.sub(r"(\+|///)", "", text.strip())
        #text=re.sub(r"(/.+/","remplacer par la 1er",text)
    # Liaison non standard remarquable
        text=re.sub(r'=\w+=','',text)
    # Comment Transcriber
        text=re.sub(r'\{.+\}','',text)
        #print "detecter (///|/|<|>)"
    # Remove noise sound (BIP) over Name of places and person
        text=re.sub(r"(¤\.+¤)",'<noise>',text)
    # Remove undecidable variant heared like on (n') en:
        text=re.sub(r"\(.+\)","",text)
        #print text
        #text=re.sub(r"(\+)", "<sil>", text)
        #text = re.sub(r"(\+|[*]+|///|/|<|>)", "", text.strip())
        #text=re.sub(r"-|_|\."," ",text.strip())
        text=re.sub(r'(O.K.)','ok',text)
        # Replace . with ' '
        #text=re.sub(r'\.',' ',text)
#text=re.sub(r"{[^{]+}"," ",text.strip())
        # BIP: OK
        text=re.sub(r"¤[^ ]+|[^ ]+¤|¤","",text.strip())
        # Remove ? ! < > : OK
        text=re.sub(r"\?|\!|<|>","",text)
    # cut of recording : OK
        text=re.sub(r"\${3}","",text)
    # Syllable incompréhensible
        text=re.sub(r"[*]+","",text)
    # replace n succesive spaces with one space. : OK
        text=re.sub(r"\s{2,}"," ",text)

    #print bool
    #print text
    return bool,text

if __name__=="__main__":
    file_trs=argv[1]
    # Read Trans File
    trsdoc= minidom.parse(file_trs)
    Turnlist= trsdoc.getElementsByTagName('Turn')
    a=""
    count=1
    for Turn in Turnlist:
        # Get Text
        field_text="".join(t.nodeValue for t in Turn.childNodes if t.nodeType == t.TEXT_NODE)
        _text=field_text.encode('utf-8','ignore').split()
        text=""
        for x in _text:
            text=text+' '+x
        # Function Transformation à faire
        bool,text=transformation_text(text)
        if bool and text!="":
            print text
