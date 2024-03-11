# BSc_Thesis_DLM_Finnish_AdpP_Supplementary_Material

This repository contains material supplementary to my unpublished bachelor's thesis "Potential Dependency Length Minimization Effects in Finnish Adpositional Phrases", handed in on March 11th, 2024 at Universität des Saarlandes.

The files do the following:

calculate_shannon_entropy.py calculates the Shannon entopry for two inputs and prints the output. I needed to know the entropy for two specific values several times and used this script to calculate it.

calculate_total_dependency_length.py reads a conllu file and prints the total dependency length of all the dependencies within, the number of sentences, the average dependency length of a sentence, and the average length of an individual dependency relation.

extract_all_sentences_containing_adp_from_file.py reads a conllu file and creates a new conllu file that contains only those sentences that contain adpositions.

t_test.py performs a paired difference t-test given two files and prints the t value. I used this on the tdt corpus (with adpositions turned into governors) and the counterfactual corpus (where all postpositions are turned into prepositions) to test whether the change in dependency length is significant. Important: I extracted only those sentences containing adpositions beforehand.

turn_adp_into_governor.py takes a conllu file and turns all adpositions into governors.

turn_all_PostP_into_PreP.py takes a conllu file and turns all postpositions into prepositions.

turn_all_PostP_into_PreP_with_adp_as_governor.py takes a conllu file and turns all postpositions into prepositions. It also turns all adpositions into governors.

ud-wordorder.py was not written by me, but provided by one of my supervisors, Dr. Luigi Talamo. It takes a conllu file, a part of speech, and a dependency relation as input and outputs a csv file with information on dependency length. I always put in "ADP case". The resulting files show the dependency length between any ADP token that has a case relation and the word it has that relation with. The results can be found in the "stats" folder.

The "stats" folder contains information on the distance between ADP tokens with a case relation and the word they have a case relation with for all ADPs in a given conllu file:

report-all_to_prep.csv uses the file as input where all postpositions are turned into prepositions.
report-gov.csv uses the file as input where adpositions are turned into governors.
report-gov_and_prep.csv uses the file as input where all postpositions are turned into prepositions and adpositions are turned into governors.
report-tdt_all.csv uses the original TDT data as input.
