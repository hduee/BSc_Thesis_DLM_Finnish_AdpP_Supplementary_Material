from conllu import parse
from conllu import parse_tree

data = """
# sent_id = b204.1
# text = The Garden Collection by H&M
1	The	The	PROPN	N	Case=Nom|Number=Sing	0	root	0:root	_
2	Garden	Garden	PROPN	N	Case=Nom|Number=Sing	1	flat:name	1:flat:name	_
3	Collection	Collection	PROPN	N	Case=Nom|Number=Sing	1	flat:name	1:flat:name	_
4	by	by	PROPN	N	Case=Nom|Number=Sing	1	flat:name	1:flat:name	_
5	H&M	H&M	PROPN	N	Abbr=Yes|Case=Nom|Number=Sing	1	flat:name	1:flat:name	_

# sent_id = b204.2
# text = Viikonlopun pyöritys alkoi H&M:n järjestämällä bloggaajabrunssilla Helsingissä.
1	Viikonlopun	viikon#loppu	NOUN	N	Case=Gen|Derivation=U|Number=Sing	2	nmod:poss	2:nmod:poss	_
2	pyöritys	pyöritys	NOUN	N	Case=Nom|Number=Sing	3	nsubj	3:nsubj	_
3	alkoi	alkaa	VERB	V	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin|Voice=Act	0	root	0:root	_
4	H&M:n	H&M	PROPN	N	Abbr=Yes|Case=Gen|Number=Sing	5	nsubj	5:nsubj	_
5	järjestämällä	järjestää	VERB	V	Case=Ade|Number=Sing|PartForm=Agt|VerbForm=Part|Voice=Act	6	acl	6:acl	_
6	bloggaajabrunssilla	bloggaaja#brunssi	NOUN	N	Case=Ade|Number=Sing	3	obl	3:obl	_
7	Helsingissä	Helsinki	PROPN	N	Case=Ine|Number=Sing	3	obl	3:obl	SpaceAfter=No
8	.	.	PUNCT	Punct	_	3	punct	3:punct	_
"""

ud_data = [
"UD_data/fi_ftb-ud-dev.conllu",
"UD_data/fi_ftb-ud-test.conllu",
"UD_data/fi_ftb-ud-train.conllu",
"UD_data/fi_ood-ud-test.conllu",
"UD_data/fi_pud-ud-test.conllu",
"UD_data/fi_tdt-ud-dev.conllu",
"UD_data/fi_tdt-ud-test.conllu",
"UD_data/fi_tdt-ud-train.conllu"
]

adp_file = ""

# klappt soweit

def read_file(file):
    global adp_file
    with open(file, encoding='utf-8') as f:
        current_sentence = ""
        for line in f:
            if "# sent_id" in current_sentence and "# sent_id" in line:
                if "ADP" in current_sentence:
                    adp_file = adp_file + current_sentence
                current_sentence = line
            else:
                current_sentence = current_sentence + line

# for ud_file in ud_data:
#    read_file(ud_file)
    
# print(adp_file)

# WIP

def calculate_dep_len(sentence:str):
    total_dep_len = 0
    avg_dep_len = 0
    l = []
    for line in sentence:
        if "#" not in line and "PUNCT" not in line:
            l.append(line.split("\t"))
    for word in l:
        if word[6] != 0:
            total_dep_len += abs(word[0]-word[6])
    total_dep_len = avg_dep_len / (len(l)-1)
    return total_dep_len, avg_dep_len


# WIP

# zu Präp ändern:
# for word in stc:
# if ADP
# if head < id
# find smallest id for which head = head of ADP # or head, if nothing comes before the head
# id of ADP = that smallest id
# every id after it += 1
# iterate over stc again

glo_stc = []

def change_to_prep(stc):
    global glo_stc
    glo_stc = stc
    for item in stc[2:]:
        if item[3] == "ADP":
            item_id = item[0]
            item_index = stc.index(item)
            head_id = item[6]
            if item_id > head_id:
                for word in glo_stc[2:]:
                    if word[0] == head_id or word[6] == head_id:
                        word_index = stc.index(word)
                        glo_stc[item_index], glo_stc[word_index] = glo_stc[word_index], glo_stc[item_index]
                        print(glo_stc)
                        break

test_d = [
['ntn'], ['fews'],
['1', 'Sarkian', 'sarkia', 'PROPN', 'N,Prop,Sg,Gen', 'Case=Gen|Number=Sing', '2', 'nmod', '_', '_\n'],
['2', 'loppusoinnut', 'loppusointu', 'NOUN', 'N,Pl,Nom', 'Case=Nom|Number=Plur', '7', 'nsubj:cop', '_', '_\n'],
['3', 'ovat', 'olla', 'AUX', 'V,Act,Ind,Pres,Pl3', 'Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act', '7', 'cop', '_', '_\n'],
['4', 'yleensä', 'yleensä', 'ADV', 'Adv', '_', '7', 'advmod', '_', '_\n'],
['5', 'briljeeraukseen', 'briljeeraus', 'NOUN', 'N,Sg,Ill', 'Case=Ill|Number=Sing', '7', 'nmod', '_', '_\n'],
['6', 'asti', 'asti', 'ADP', 'Adp', '_', '5', 'case', '_', '_\n'],
]

#item_id = 6
#item_index = 7
#head_id = 5

print(change_to_prep(test_d))


# WIP

# Sätze als Liste von Listen
# Sätze umstellen
# wieder in Datei schreiben

with open("ud_data/five_sentence_test_file.txt", encoding='utf-8') as f:
    l = []
    for line in f:
        if line != "\n":
            l.append(line.split("\t"))   
        else:
            with open("ud_data/test_output.txt", 'a', encoding='utf-8') as append_f:
                for item in l:
                    if type(item) == 'str':
                        append_f.write(item)
                    else:
                        for subelement in item:
                            append_f.write(subelement+"\t")
                            
            with open("ud_data/prep_test.txt", 'a', encoding='utf-8') as prep_f:
                test_prep = change_to_prep(l)
                print(test_prep)
                for item in test_prep:
                    if type(item) == 'str':
                        prep_f.write(item)
                    else:
                        for subelement in item:
                            prep_f.write(subelement+"\t")
            l = []
        



     
        

# zu Post ändern:
# for word in stc:
# if ADP
# if head > id
# find largest id for which head = head of ADP
# id of ADP = that largest id
# every id before it -= 1
# iterate over stc again
