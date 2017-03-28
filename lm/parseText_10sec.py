#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from unicodedata import normalize
from sys import argv
from num2words import num2words
from unidecode import unidecode
import re
import os.path
import sys
# ( in text
# ) in text
def transformation_text(text):
    bool=True
    if "###" in text or len(re.findall(r"\[.+\]", text)) > 0 or \
                    len(re.findall(r"\p{L}+-[^\p{L}]|\p{L}+-$",text)) > 0 \
            or len(re.findall("[^\p{L}]-\p{L}+|^-\p{L}+", text)) > 0:
        #print text
        #print "Ligne Supprime"
        bool=False
    else:
        # 4x4
        # Remove noise sound (BIP) over Name of places and person
        #text = re.sub(r"¤[^ ]+|[^ ]+¤|¤", "", text.strip())
        if len(re.findall(r"\dx\d",text))>0:
            text=re.sub(r"x","  ",text)
        if len(re.findall("\d+h\d+",text))>0:
            heures=re.findall("\d+h\d+",text)
            for h in heures:
                split_h=h.split('h')
                text_rep=split_h[0]+' heure '+split_h[1]
                text=text.replace(h, text_rep)
        text=re.sub(r',',' ',text)
        # remove silence character : OK
        #text=re.sub(r"(/.+/","remplacer par la 1er",text)
        # Liaison non standard remarquable
        text=re.sub(r'=','',text)
        # Comment Transcriber
        text=re.sub(r'\{.+\}','',text)
        text=re.sub(r'\(.+\}','',text)
        #print "detecter (///|/|<|>)"
        # Remove undecidable variant heared like on (n') en:
        text=re.sub(r"\(.+\)","",text)
        #text = re.sub(r"(\+|[*]+|///|/|<|>)", "", text.strip())
        #text=re.sub(r"-|_|\."," ",text.strip())
        text=re.sub(r'(O.K.)','ok',text)
        text = re.sub(r'(O.K)', 'ok', text)
        # Replace . with ' '
        text=re.sub(r'\.',' ',text)
        #text=re.sub(r"{[^{]+}"," ",text.strip())
        # Remove ? ! < > : OK
        #<[^\p{L}]|[^\p{L}]>|#+|<\p{L}+[ ]|<\p{L}+$
        text=re.sub(r":|\?|/|\!|<|>|#+","",text)
        # replace silence character with <sil> : OK
        #text=re.sub(r"(\+)", "<sil>", text)
        text=re.sub(r"(\+)", "", text)
        text=re.sub(r"(///)", "", text)
        #text=re.sub(r"(///)", "<long-sil>", text)
        if len(re.findall(r"/.+/", text)) > 0:
            #print "AVANT***********"+text
            for unchoosen_text in re.findall(r"/.+/", text):
                # choose first undecideble word
                unchoosen_word=unchoosen_text.split(',')
                for choosen_word in unchoosen_word:
                    # isn't incomprehensible word
                    if len(re.findall(r"\*+|\d+", choosen_word))==0:
                        choosen_word = choosen_word.replace('/', '')
                        text = text.replace(unchoosen_text, choosen_word)
                        #print "Apres************"+text
                        # Remove noise sound (BIP) over Name of places and person
        text=re.sub(r"(¤.+¤)",'',text)
        # replace unkown syllable
        text=re.sub(r"\*+","",text)
        # cut of recording : OK
        text=re.sub(r"\$+","",text)
        # remove " character: OK
        text = re.sub(r"\"+", "", text)
        # t 'avais
        text = re.sub(r"[ ]\'", " ", text)
        text = re.sub(r"\'", "\' ", text)
        # convert number if exist : OK
        num_list = re.findall(" \d+| \d+$", text)
        if len(num_list) > 0:
            #print text
            #print "********************************* NUM2WORD"
            for num in num_list:
                num_in_word = num2words(int(num), lang='fr')
                #num_in_word=normalize('NFKD', num_in_word).encode('ascii', 'ignore')
                text = text.replace(str(num), " " + str(num_in_word) + " ")
                #print text
                # replace n succesive spaces with one space. : OK
        text=re.sub(r"\s{2,}"," ",text)
        text = re.sub("^ ", '', text)
    # change bounding | to < and > : OK
    #balise=set(re.findall(r"\|\w+_?\w+\|",text))
    #if len(balise)>0:
        #print(balise)
    #    for b in balise:
    #        new_balise='<'+b[1:len(b)-1]+'>'
    #        text=text.replace(b,new_balise)
            #print(text)
    # c'est l'essaim ....
    text=text.lower()
    return bool,text
if __name__=="__main__":
    duration=5
    # Inputs
    file_trs=argv[1]
    #print(file_trs)
    #print file_trs
    # Read Trans File
    tree_trs = ET.parse(file_trs)
    trsdoc= tree_trs.getroot()
    text=""
    Turn_count=0
    count=0
    has_attrib_speaker=False
    seg_duration=0
    start_utt=0
    end_utt=0
    # set for uniq add
    for Element in trsdoc.iter():
        if Element.tag=="Turn" and Element.get('speaker') is None:
            has_attrib_speaker=False
        elif Element.tag=="Turn":
            # If the latest Utterance of previous Speaker is the latest one of his Turn speech
            if Turn_count>0:
                count = 0
                bool, text = transformation_text(text)
                # File wav.scp
                # File utt2spk
                # File text
                # File speaker_gender
                seg_duration=seg_duration+(float(endTime)-float(start_utt))
                if bool and text!="" and seg_duration>duration:
                    print(text)
                    start_utt=endTime
                    seg_duration=0
                    text=""
                    #for spk_tuple in speaker_gender:
                    #    if spk_tuple[0]==spkr:
                    #        print >> spk2gender,'%s %s' % (seg_id, spk_tuple[1])
                    #        break
            has_attrib_speaker=True
            # count sync for computing start and end utterance
            startTime = Element.get('startTime')
            # Get EndSegment
            endTime = Element.get('endTime')
            Turn_count = Turn_count+1
        elif Element.tag=="Sync" and has_attrib_speaker:
            Time_start_current_sync=Element.get('time')
            if count>0:
                bool, text = transformation_text(text)
                end_utt=Time_start_current_sync
                seg_duration=seg_duration+(float(end_utt)-float(start_utt))
                if bool and text!="" and seg_duration>duration:
                    print(text)
                    start_utt=Time_start_current_sync
                    seg_duration=0
                    text=""
            text=text+Element.tail.replace('\n', '')
            count=count+1
        elif Element.tag=="Comment" and has_attrib_speaker and not Element.tail is None:
            text=text+" "+Element.tail.replace('\n', '')
        elif Element.tag=="Event" and has_attrib_speaker and not Element.tail is None :
            text=text+" "+Element.tail.replace('\n', '')
        elif Element.tag=="Who" and has_attrib_speaker and not Element.tail is None:
            text=text+" "+Element.tail.replace('\n', '')
    if count > 0 and has_attrib_speaker and not Element.tail is None and seg_duration>duration:
        bool, text = transformation_text(text)
        if bool and text != "":
            print(text)