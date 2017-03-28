#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET
from sys import argv
from num2words import num2words
from unidecode import unidecode
import re
import os.path

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
        text=re.sub(r"(\+)", "!SIL", text)
        text=re.sub(r"(///)", "!SIL", text)
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
        text=re.sub(r"(¤.+¤)",'<NOISE>',text)
    # replace unkown syllable
        text=re.sub(r"\*+","<SPOKEN_NOISE>",text)
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
    balise=set(re.findall(r"\|\w+_?\w+\|",text))
    if len(balise)>0:
        #print(balise)
        for b in balise:
            new_balise='<'+b[1:len(b)-1]+'>'
            text=text.replace(b,new_balise)
        #print(text)
    # c'est l'essaim ....
    text=text.lower()
    return bool,text
if __name__=="__main__":
    # Inputs
    file_trs=argv[1]
    #print(file_trs)
    #print file_trs
    outdir=argv[2]
    basename=os.path.basename(file_trs.split('.')[0])
    # MetaData File
    file_meta = file_trs.split('.')[0] + '.xml'
    #print file_trs.split('.')[0]
    # Output File needed for kaldi input
    segments_file = open(outdir + '/segments', 'a')
    utt2spk_file = open(outdir + '/utt2spk', 'a')
    text_file = open(outdir + '/text', 'a')
    wav_scp = open(outdir + '/wav.scp', 'a')
    spk2gender= open(outdir + '/spk2gender', 'a')
    # Read Trans File
    tree_trs = ET.parse(file_trs)
    trsdoc= tree_trs.getroot()
    #Read MetaData Of speaker ( ID and Name)
    speaker_id=[]
    namespk=[]
    for spk in trsdoc.iter('Speaker'):
        id_spk=spk.get('id')
        name_spk=unidecode(spk.get('name'))
        #if isinstance(name_spk,str):
        #print(type(name_spk))
        #name_spk=normalize('NFKD', name_spk).encode('ascii', 'ignore')
        speaker_id.append(id_spk.replace(" ",""))
        namespk.append(name_spk.lower().replace(" ",""))
    #Read MetaData To get Gender of Speaker (Gender and Name)
    tree_meta = ET.parse(file_meta)
    metadoc= tree_meta.getroot()
    speaker_gender=[]
    #print namespk
    #print speaker_id
    for loc in metadoc.iter('locuteur'):
        if loc.attrib!=dict({}):
            name_loc=loc.get('identifiant')
            name_loc = unidecode(name_loc)
            name_loc=name_loc.replace(" ","")
            #print name_loc
            #print name_loc
            #If the gender of speaker doesn't mentioned
            #print loc.findall('sexe')
            if loc.findall('sexe')==[]:
                speaker_gender.append([speaker_id[namespk.index(name_loc.lower())],'m'])
            else:
                # case 1 represent gender informat
                gender_loc=loc.find('sexe').text
                if gender_loc==None:
                    speaker_gender.append([speaker_id[namespk.index(name_loc.lower())], 'm'])
                else:
                    #print namespk
                    #print namespk.index(name_loc.lower())
                    speaker_gender.append([speaker_id[namespk.index(name_loc.lower())],gender_loc.lower()])
    #Turnlist= trsdoc.getElementsByTagName('Turn')
    #Synclist= trsdoc.getElementsByTagName('Sync')
    #print len(Turnlist)
    #print len(Synclist)
    #list_time_sync=[]Q
    #for sync in Synclist:
    #    list_time_sync.append(float(sync.attributes['time'].value))
    #a=""
    #count=1
    #print "#id_utt\tid_Seg\tid_Spkr\tstartTime\tendTime\tText"
    text=""
    Turn_count=0
    count=0
    has_attrib_speaker=False
    # set for uniq add
    Spk_that_contribute_to_meeting=set([])
    start_utt=0
    end_utt=0
    sourceEncoding = "iso-8859-1"
    targetEncoding = "utf-8"
    for Element in trsdoc.iter():
        if Element.tag=="Turn" and Element.get('speaker') is None:
            has_attrib_speaker=False
        elif Element.tag=="Turn":
            # If the latest Utterance of previous Speaker is the latest one of his Turn speech
            if Turn_count>0:
                count = 0
                #print text
                ### Save Files For Kaldi ###
                seg_id = str(basename) + '_spk-%03d_Turn-%03d_seg-%07d' % (int(spkr.split('spk')[1]), int(Turn_count), int(count))
                spkr_id=str(basename)+'_spk-%03d' % int(spkr.split('spk')[1])
                bool, text = transformation_text(text)
                # File wav.scp
                # File utt2spk
                # File text
                # File speaker_gender
                if bool and text!="":
                    segments_file.write(seg_id+" "+basename+" "+str(start_utt)+" "+str(endTime)+"\n")
                    start_utt=endTime
                    utt2spk_file.write(seg_id+" "+spkr_id+"\n")
                    text_file.write(seg_id+" "+text+"\n")
                    #for spk_tuple in speaker_gender:
                    #    if spk_tuple[0]==spkr:
                    #        print >> spk2gender,'%s %s' % (seg_id, spk_tuple[1])
                    #        break
            has_attrib_speaker=True
            # Get id_spkr
            spkr = Element.get('speaker')
            #print file_trs
            spkr=spkr.split()[0]
            Spk_that_contribute_to_meeting.add(spkr)
            #print spkr
            # Get StartSegment
            startTime = Element.get('startTime')
            # Get EndSegment
            endTime = Element.get('endTime')
            # count sync for computing start and end utterance
            Turn_count = Turn_count+1
        elif Element.tag=="Sync" and has_attrib_speaker:
            Time_start_current_sync=Element.get('time')
            if count>0:
                #print text
                ### Save Files For Kaldi ###
                seg_id = str(basename) + '_spk-%03d_Turn-%03d_seg-%07d' % (int(spkr.split('spk')[1]), int(Turn_count) , int(count))
                spkr_id=str(basename)+'_spk-%03d' % int(spkr.split('spk')[1])
                bool, text = transformation_text(text)
                end_utt=Time_start_current_sync
                if bool and text!="":
                    segments_file.write(seg_id+" "+basename+" "+str(start_utt)+" "+str(end_utt)+"\n")
                    start_utt=Time_start_current_sync
                    utt2spk_file.write(seg_id+" "+spkr_id+"\n")
                    text_file.write(seg_id+" "+text+"\n")
            text=Element.tail.replace('\n', '')
            count=count+1
        elif Element.tag=="Comment" and has_attrib_speaker and not Element.tail is None:
            text=text+" "+Element.tail.replace('\n', '')
        elif Element.tag=="Event" and has_attrib_speaker and not Element.tail is None :
            if Element.get('type')=='noise':
                if Element.get('desc')=='rire':
                    text=text+" |LAUGH| "+Element.tail.replace('\n', '')
                else:
                    text=text+" |NOISE| "+Element.tail.replace('\n', '')
            elif Element.get('type')=='pronounce':
                text=text+" |SPOKEN_NOISE| "+Element.tail.replace('\n', '')
            else:
                text=text+" |NOISE| "+Element.tail.replace('\n', '')
        elif Element.tag=="Who" and has_attrib_speaker and not Element.tail is None:
            text=text+" "+Element.tail.replace('\n', '')
        #else:
        #    print Element.attrib,Element.tag
        #    text=str(Element.tail)
        #    print "*********warning********"+text
            # Les phrases appartenant � un tour de parole
    # The last Turn, check if count >0 and add latest utterance
    #print count
    #print has_attrib_speaker
    #print Element.tail
    if count > 0 and has_attrib_speaker and not Element.tail is None:
        #print text
        ### Save Files For Kaldi ###
        seg_id = str(basename) + '_spk-%03d_Turn-%03d_seg-%07d' % (
        int(spkr.split('spk')[1]), int(Turn_count), int(count))
        spkr_id = str(basename) + '_spk-%03d' % int(spkr.split('spk')[1])
        bool, text = transformation_text(text)
        if bool and text != "":
            segments_file.write(seg_id+" "+basename+" "+str(start_utt)+" "+str(endTime)+"\n")
            utt2spk_file.write(seg_id+" "+spkr_id+"\n")
            text_file.write(seg_id+" "+text+"\n")
    for spk in speaker_gender:
        if spk[0] in Spk_that_contribute_to_meeting:
            spk_id = str(basename)+'_spk-%03d' % int(spk[0].split('spk')[1])
            spk2gender.write(spk_id+" "+spk[1]+"\n")
    wav_scp.write(basename+" sox "+os.path.dirname(file_trs) + '/' + basename + '.wav'+" -t wav -r 16000 -c 1 - |\n")
    segments_file.close()
    utt2spk_file.close()
    text_file.close()
    wav_scp.close()
