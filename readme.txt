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

## Steps to align English Hindi sentence

1. Download and setup the path:

	Download the phrase_alignment repository into any path in your system.
	Unzip the folder . For e.g in /home/sriram/phrase_alignment
	set up the path in bashrc . For e.g. as below.
        export HOME_phrase_alignment=/home/sriram/phrase_alignment
    
2. To align a single English sentence to its Hindi NMT translation

  For e.g. English sentence is
  
  `Chapter 1 Introduction Inventors have long dreamed of creating machines that think.`
  
  and its Hindi translation from different NMT models:
  
  
NMT:  अध्याय 1 परिचय निवेशकों लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय निवेशकों लंबे समय से सोच मशीनों बनाने के सपने देखा है .
NMT:  अध्याय 1 परिचय निवेशकों को लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय अन्वेषकों लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय निवेशकों ने लंबे समय से ऐसी मशीनों के निर्माण का सपना देखा है जो सोचती हैं ।
NMT:  अध्याय 1 परिचय निवेशकों ने लंबे समय से ऐसी मशीनें बनाने का सपना देखा है जो सोचती हैं ।
NMT: 
  
  Put it in a single file ' English-Hindi-Translations' as below.
  
  
  English -->    Chapter 1 Introduction Inventors have long dreamed of creating machines that think.
NMT:  अध्याय 1 परिचय निवेशकों लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय निवेशकों लंबे समय से सोच मशीनों बनाने के सपने देखा है .
NMT:  अध्याय 1 परिचय निवेशकों को लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय अन्वेषकों लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
NMT:  अध्याय 1 परिचय निवेशकों ने लंबे समय से ऐसी मशीनों के निर्माण का सपना देखा है जो सोचती हैं ।
NMT:  अध्याय 1 परिचय निवेशकों ने लंबे समय से ऐसी मशीनें बनाने का सपना देखा है जो सोचती हैं ।
NMT: 


Several example sentences are given in the directory 'uniq-hnd-translation'


3. For the english sentence get the chunks(groups) from constituent parse and translate it using NMT.

for e.g. for the english sentence


the chunks and its hindi translation as as follows.

------------	------------
NP2	Chapter 1 Introduction Inventors	aXyAya 1 paricaya AviRkAraka
NML3	Chapter 1	aXyAya 1
NNP6	Introduction	paricaya
NNP7	Inventors	nirmAwAoM
VP8_LWG	have long dreamed	laMbe samaya se sapane xeKa cuke hEM
ADVP10	long	laMbe samaya waka
PP14	of creating machines that think	maSInoM kA nirmANa karanA jo socawe hEM
VP17_LWG	creating	banA rahA hE racanA
NP19	machines that think	maSIneM jo socawI hEM
NP20	machines	maSIneM
WHNP23	that	vaha
VP26_LWG	think	socie
  
 
put it in a file 'Grp-translation'.

4. Get root words of all the Hindi words and put it in a file called 'hnd_root_list'. One sample file named 'hnd_root_list' is provided. 

5. To run the alignment program.

sh run-alignment.sh English-Hindi-Translations Grp-translation 




## output:

Raw output is stored on 'output' file 

sample output be like as follow.

Chapter 1 Introduction Inventors have long dreamed of creating machines that think.
अध्याय 1 परिचय निवेशकों लंबे समय से मशीनों है कि लगता है बनाने का सपना देखा है .
	 Chapter 1 Introduction Inventors	have long dreamed	of	creating	machines that think
	 अध्याय 1 परिचय आविष्कारक/1	/लंबे समय से सपने देख चुके हैं	/	/	/मशीनें जो सोचती हैं
प्रोचेस्सेड्




