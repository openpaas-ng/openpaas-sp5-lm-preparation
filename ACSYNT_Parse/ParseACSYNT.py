#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Abdel Linagora@March17


from textgrid import TextGrid
from sys import argv
import re
import os.path


def transform_text(text):
    if len(re.findall(r"\<.+\>", text)) > 0:
        text=re.sub(r"\<.{2}"," ",text)
        text=re.sub(r"\>"," ",text)
    text=re.sub(r"\[\w+\]","<noise>",text)
    text=re.sub(r"\[.+\]","<noise>",text)
    text=re.sub(r"\.","",text)
    text=re.sub(r"\\+","",text)
    text=re.sub(r"e\^","ê",text)
    text=re.sub(r"c\,","ç",text)
    text=re.sub(r"o\^","ô",text)
    text=re.sub(r"u\`","ù",text)
    text=re.sub(r"i\^","î",text)
    text=re.sub(r"\?","",text)
    # delete space in the end of utterance
    text=re.sub(r"[\s]+$","",text)
    # replace n succesive spaces with one space. : OK
    text=re.sub(r"\s{2,}"," ",text)
    # split word j'y j' y
    if len(re.findall(r"\w+-\w+\'\w+", text)) > 0:
        a=
    else:
        text = re.sub("\'","\' ",text)
    text=text.lower()
    return text
if __name__=="__main__":
    # Input : file.TEXTGRID and we assume that file.wav are in the same directory
    TEXTGRID_file=argv[1]
    dirname=os.path.dirname(TEXTGRID_file)
    basename=os.path.basename(TEXTGRID_file.split('.')[0])
    WAV_file=dirname+'/'+basename+'.wav'
    # Output directory
    outdir=argv[2]
    # Output File needed for kaldi input
    segments_file = open(outdir + '/segments', 'a')
    utt2spk_file = open(outdir + '/utt2spk', 'a')
    text_file = open(outdir + '/text', 'a')
    wav_scp = open(outdir + '/wav.scp', 'a')

    # Parse TEXTGRID FILE
    TEXTGRID_io=open(TEXTGRID_file,'r')
    TEXTGRID_obj=TextGrid(TEXTGRID_io.read())
    # Get only first Imte
    Tier=TEXTGRID_obj.tiers[0]
    count=0
    Spk_that_contribute_to_meeting=[]
    spkr_id=1
    for deb_seg,end_seg,text in Tier.simple_transcript:
        seg_id=str(basename) + '_spk-%03d_seg-%05d' % (int(count), int(count))
        text=transform_text(text)
        split_spkr_text=text.split(':')
        if len(split_spkr_text)>1:
            if not split_spkr_text[0] in Spk_that_contribute_to_meeting:
                Spk_that_contribute_to_meeting.append(split_spkr_text[0])
            spkr=Spk_that_contribute_to_meeting.index(split_spkr_text[0])+1
            spkr_id=str(basename)+'_spk-%03d' % int(spkr)
            text=split_spkr_text[1]
        text = re.sub("^ ", "", text)
        #print(split_spkr_text)
        segments_file.write(seg_id+" "+basename+" "+str(round(float(deb_seg),3))+" "+str(round(float(end_seg),3))+"\n")
        text_file.write(seg_id+" "+text+"\n")
        utt2spk_file.write(seg_id+" "+str(spkr_id)+"\n")
        count=count+1
    wav_scp.write(basename+" sox "+WAV_file+" -t wav -r 16000 -c 1 - |\n")
    segments_file.close()
    utt2spk_file.close()
    text_file.close()
    wav_scp.close()