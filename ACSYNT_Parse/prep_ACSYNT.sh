#!/usr/bin/env bash

# Abdel @LINAGORA - DONE

corpus=$1
# CD1 CD2 CD3 are directories which contain Data
ACSYNT_CD1=$corpus/ACSYNT_CD1/ACSYNT_CD1
ACSYNT_CD2=$corpus/ACSYNT_CD2/ACSYNT_CD2
ACSYNT_CD3=$corpus/ACSYNT_CD3/ACSYNT_CD3

# separate Readed speech , prepared speech and meetings
# 4 letters : 3 for ID and latest: E: for meeting, P: for prepared speech and T: for readed speech

out=$2
out_prepared=$out/prepared_speech
out_meeting=$out/meeting
out_story=$out/story
mkdir -p $out
mkdir -p $out_prepared
mkdir -p $out_story
mkdir -p $out_meeting

for type_speech in $(find $ACSYNT_CD1 $ACSYNT_CD2 $ACSYNT_CD3 -mindepth 1 -maxdepth 1 -type d);do
type=$(basename $type_speech)
_Bool_meeting=`echo $type | grep "Entretien"`
_Bool_prepared=`echo $type | grep "Presentation"`
_Bool_text=`echo $type | grep "Text"`
if [ ! -z "$_Bool_meeting" ]; then
# This file is a meeting
for dir_meeting in $(find $type_speech -mindepth 1 -maxdepth 1 -type d);do
cp -r $dir_meeting/ $out_meeting
dir_name=$(basename $dir_meeting)
_Bool_Uppercase=`ls $out_meeting/$dir_name | grep ".TEXTGRID"`
for filewithuppercase in $(echo $_Bool_Uppercase); do
fileingoodformat=`echo $filewithuppercase | sed "s/TEXTGRID/TextGrid/"`
mv $out_meeting/$dir_name/$filewithuppercase $out_meeting/$dir_name/$fileingoodformat
done
done
fi
if [ ! -z "$_Bool_prepared" ]; then
# This file is a prepared speech
for dir_prepared in $(find $type_speech -mindepth 1 -maxdepth 1 -type d);do
cp -r $dir_prepared/ $out_prepared
dir_name=$(basename $dir_prepared)
_Bool_Uppercase=`ls $out_prepared/$dir_name | grep ".TEXTGRID"`
for filewithuppercase in $(echo $_Bool_Uppercase); do
fileingoodformat=`echo $filewithuppercase | sed "s/TEXTGRID/TextGrid/"`
mv $out_prepared/$dir_name/$filewithuppercase $out_prepared/$dir_name/$fileingoodformat
done
done
fi
if [ ! -z "$_Bool_text" ]; then
# This file is a story readed
for file_story in $(find $type_speech -mindepth 1 -maxdepth 1 | grep wav);do
wav_file=$(basename $file_story)
dir_name=$(dirname $file_story)
file_name=`echo $wav_file | sed 's/\.wav//g'`
mkdir -p $out_story/$file_name
cp $dir_name/$file_name* $out_story/$file_name
#cp `echo $file_story | sed 's/wav/TextGrid/g'` $out_story/$dir_out
# change all textgrid extension to TEXTGRID
_Bool_Uppercase=`ls $out_story/$file_name | grep ".TEXTGRID"`
if [ ! -z  "$_Bool_Uppercase" ]; then
mv $out_story/$file_name/$file_name.TEXTGRID $out_story/$file_name/$file_name.TextGrid
fi
done
echo "Text..."
fi
done