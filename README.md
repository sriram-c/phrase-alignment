# Phrase-alignment

Tool to align the phrases/gropus in English and Hindi NMT translated sentences.



## Prerequisties:

##### NMT translation of English sentences:
English sentences need to be translated to Hindi using various NMT models. 
NMT translations of each English sentence has to be kept in the folder 'uniq-hnd-translation'
For the format please see the sample files kept inside the folder.

##### NMT translations of English groups/chunks:

English sentences need to be break down to groups/chunks and should be given the NMT for translation to Hindi.
These group/chunks translation should be kept inside folder 'eng-hnd-grp-translations'.
For the format please see the sample files kept inside the folder.

##### Root dictionary for Hindi words:

The file 'hnd_root_list' contains the root dictionary of each Hindi word present in the translated output.
To get the root list the tool will be shared separately.

## To Run

`sh run-all.sh selected-list`

selected-list contains the sentence numbers you want to run.

## output:

Raw output is stored on 'output' file and the html version in 'output.html'



