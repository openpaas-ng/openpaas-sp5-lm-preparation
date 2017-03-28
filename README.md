# Text Preparation

 The process of building a language model consists of the following steps:
 
- Data collection
- Data cleanup
- Model training
- Testing

In this project we focus on the two first steps. To build a Statistical Language Model first of all we need to prepare a large collection of clean texts. You can collect text transcription from project like librivox, transcribed podcasts, setup web data collection, by transcribing existing recordings, or generating it artificially with scripts. You can also try to contribute to Voxforge. The most valuable data is a real-life data anyway. 
Our project's context concerns French conversational speech during meetings. Therefore we tried to collect corpora adapted to our context that we share here with you including their preparation.

# Data collection

We have grouped the following corpora by specifying their license and their respective characteristics.
Movie subtitles are also good source for spoken language. 

| Corpora |  Constructed at  | Licence  | Hours/words | Speakers | Database Type |
| ------ | ------ | ------ | ------ | ------ | ------ |
| ASCYNT  | Université Jean Jaures - Toulouse  | Creative Commons | 9 H /124 000 words | 2 Males - 21 Females | - The oral conference of text (17,858 words), monologue presentations (19,575 words) and guided interviews (86,584). - Audio files and PRAAT transcriptions (textgrid format)|
| TCOF: Traitement de Corpus Oraux en Français | ATILF Analyse et Traitement Informatique de la Langue Française - Nancy | Creative Commons, Freely available for non-commercial use  | 124 H | 1365 Speakers | Spontaneous Speech. Transcriber et WAV |
| CFPP2000: COllections de COrpus Oraux Numériques | Université Paris 3 Sarbonne nouvelle  | Creative Commons,Freely available for non-commercial use  | 49 H  | Unknown  | Interviews |
| ESLO | Laboratoire Ligérien de Linguistique de l'université d'Orléans en partenariat avec le CNRS et le Ministère de la Culture et la Région Centre | Creative Commons| 800 H / around 5 Million of words | Unknown | calls, interview, visit, meeting, diner |
| Movie Subtitles | https://www.sous-titres.eu/ | Free for use | A lot | Plenty | Movie subtitles |

## Download corpora!
Links to download the corpora are in the following table.

| Corpora Name | Download Link |
| ------ | ------ |
| ASCYNT | https://www.ortolang.fr/market/corpora/sldr000832 |
| TCOF | https://www.ortolang.fr/market/corpora/tcof |
| CFPP2000 | http://cfpp2000.univ-paris3.fr/Corpus.html |
| ESLO | http://ct3.ortolang.fr/data2/eslo/ |
| Movie Subtitles | https://www.sous-titres.eu/ |

For movie subtitles, you can download the .zip files and then extract them. 

## Different formats

The corpora that we have gathered use different formats of transcripts. We have the following formats:
- [Transcriber format][transcriber] (TCOF, CFPP2000) 
- [PRAAT (textgrid format)][TextGrid] (ASCYNT)
- [SubRip][srt] and [SubStation Alpha subtitle text file format][ass] (Movie Subtitles)

When downloading Eslo corpus, you have a "raw" version of transcription. You can synchronize the transcriptions to the sound using transcriber software, which allows segmentation at several levels: sections, speakers, speaking slots. In this [website][EsloTranscription] you're going to find more details about Eslo's transcription format.

# Data cleanup

In this folder you're going to find all the scripts that we used to generate the kaldi files and to cleanup these different corpora ; to expand abbreviations, convert numbers to words, clean non-word items, replace silence character with <sil>, replace n succesive spaces with one space...

## Files/Script Includes With This Project

> `runPrepare.sh` that is called by the main script of the project to run the right preparation according to the corpus passed as a parameter (parameters order: corpus name, path to the corpus, path for the Directory output)
> `dataPrepare.sh` prepares segment, utt2spk, text, wav.scp files and calls the Parse script to clean up the text.

The following scripts cleanup the text of the transcription according to the transcription format (so to the corpus)
> `parseTcofSync.py`
> `parseAscynt.py`
> `parseCfppSync.py`
> `parseEsloSync.py`
> `parseSubtitles.py`

## Libraries
List of libraries you should install to be able to run our scripts:
- xml.etree.ElementTree [The ElementTree XML API][ElementTree]
- sys [System-specific parameters and functions][sys] 
- num2words [Convert numbers to words in multiple languages][num2words] 
- unidecode [ASCII transliterations of Unicode text][unicode] 
- re [Regular expression operations][re] 
- os.path [Common pathname manipulations][os.path] 

We used Python 3.5.2. If you are using an older version of Python you may experience encoding problems especially with the French language (accents).

# Authors
Original Author and Development Lead

- Abdelwahab HEBA (aheba@linagora.com)
- Sonia BADENE (soniabadene@gmail.com)
- Tom JORQUERA (tjorquera@linagora.com)

# Development
Want to contribute? Great! Share your work with us in the following link:


License
----
GNU AFFERO GENERAL PUBLIC LICENSE v3


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)



   [transcriber]: <http://trans.sourceforge.net/en/usermanUS.php>
   [TextGrid]: <http://www.fon.hum.uva.nl/praat/manual/TextGrid.html>
   [EsloTranscription]: <http://eslo.huma-num.fr/index.php/pagemethodologie/20-eslo>
   [srt]: <https://en.wikipedia.org/wiki/SubRip>
   [ass]: <https://en.wikipedia.org/wiki/SubStation_Alpha>
   [ElementTree]: <https://docs.python.org/2/library/xml.etree.elementtree.html>
   [sys]: <https://docs.python.org/3/library/sys.html>
   [num2words]: <https://pypi.python.org/pypi/num2words>
   [unicode]: <https://pypi.python.org/pypi/Unidecode>
   [re]: <https://docs.python.org/2/library/re.html>
   [os.path]: <https://docs.python.org/2/library/os.path.html>
   

