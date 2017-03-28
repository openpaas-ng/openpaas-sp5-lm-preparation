#!/bin/bash

# Copyright 2016 Linagora (author: Abdel HEBA) | DONE
# see research.linagora.com OpenPaas Project and https://hubl.in for meetings
# GPL

source path.sh

#LANG=en_US.ISO-8859-15

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <src-dir> <dst-dir>"
    echo "e.g: $0 /baie/corpus/ESTER/DGA/Phase1/data data/Phase1"
    #exit 1
fi

 src=$1
 dst=$2

# all utterances are Wav compressed, we use sox for reading signal in binary format
if ! which sox >&/dev/null; then
    echo "Please install 'sox' on All worker nodes"
    echo "apt-get install sox"
    #exit 1
fi


#Reflechir partie Split...?

#echo "=== Starting initial Tcof Data preparation ..."

#echo "--- Making test/train data split ..."

mkdir -p $dst #|| exit 1;

[ ! -d $src ] && echo "$0: no such directory $src" #&& exit  1;

wav_scp=$dst/wav.scp; [[ -f "$wav_scp" ]] && rm $wav_scp
trans=$dst/text; [[ -f "$trans" ]] && rm $trans
utt2spk=$dst/utt2spk; [[ -f "$utt2spk" ]] && rm $utt2spk
spk2gender=$dst/spk2gender; [[ -f $spk2gender ]] && rm $spk2gender
utt2dur=$dst/utt2dur; [[ -f "$utt2dur" ]] && rm $utt2dur
segments=$dst/segments; [[ -f "$segments" ]] && rm $segments

# For each session
for trs_file in $(find $src -type f -name "*.trs" | sort); do
    wav_file=$(echo $meeting_dir | sed "s/.trs/.wav/g")
    [ ! -f $trs_file ] && [ ! -f $wav_file ] && echo " Missing $meeting.trs or $meeting.wav file " #&& exit 1
    # Generate Kaldi input file
    #echo $meeting_dir
    #echo $dst
    #python3 local/parse_AudioDB.py --data-prep --input-dir $meeting_dir --output-dir $dst >> log.txt 2>&1
    echo "python3 local/parseTcofSync.py $trs_file $dst >> log.txt 2>&1"
done

# Sort all files
# text
#export LC_ALL=C
cat $trans | sort -k1 > $trans.txt
rm $trans
mv $trans.txt $trans
#segments
cat $segments | sort -k1 > $segments.txt
rm $segments
mv $segments.txt $segments
# wav
cat $wav_scp | sort -k1 > $wav_scp.txt
rm $wav_scp
mv $wav_scp.txt $wav_scp
# spk2gender
cat $spk2gender | sort -k1 > $spk2gender.txt
rm $spk2gender
mv $spk2gender.txt $spk2gender
# utt2spk
cat $utt2spk |sort -k1 > $utt2spk.txt
rm $utt2spk
mv $utt2spk.txt $utt2spk

# convert utt2spk to spk2utt
spk2utt=$dst/spk2utt
utils/utt2spk_to_spk2utt.pl <$utt2spk >$spk2utt #|| exit 1

# Sort spk2utt
cat $spk2utt | sort -k1 > $spk2utt.txt
rm $spk2utt
mv $spk2utt.txt $spk2utt
# Check trannscripts and utterances
 ntrans=$(wc -l <$trans)
 nutt2spk=$(wc -l <$utt2spk)
 ! [ "$ntrans" -eq "$nutt2spk" ] && \
    echo "Inconsistent #transcripts($ntrans) and # utt2spk($nutt2spk)" #&& exit 1;

# compute segment's duration
 utils/data/get_utt2dur.sh $dst 1>&2 #|| exit 1
# Validate Kladi Inputs
 utils/validate_data_dir.sh --no-feats $dst #|| exit 1;

 echo "Successfully prepared data in $dst.."

#exit 0
