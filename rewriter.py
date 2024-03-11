import argparse
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()

if __name__ == '__main__':

    condition = 'make_prep'

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file')
    parser.add_argument('output_file', help='output file')
    args = parser.parse_args()

    file = args.input_file
    output = args.output_file
    
    with open(file, 'r', encoding='utf-8') as f:
        current_id = ""
        current_text = ""
        current_text_split = []
        sen = {}
        for line in f:
            if "# sent_id" in line:
                # write to file
                # new dict
                current_id = line
            elif "# text" in line:
                current_text = line
                #current_text_split = nltk.word_tokenize(current_text)
                current_text_split = tokenizer.tokenize(current_text)
            elif line == "\n":
                l = []
                for i in sen.keys():
                    ll = [sen[i]['new_number']] 
                    ll.append(sen[i]['word'])
                    ll.append(sen[i]['lemma'])
                    ll.append(sen[i]['POS'])
                    ll.append(sen[i]['pos'])
                    ll.append(sen[i]['agr'])
                    ll.append(sen[i]['head_num'])
                    ll.append(sen[i]['deprel'])
                    ll.append(sen[i]['rel_detail'])
                    ll.append(sen[i]['final'])

                    l.append(ll)
                l.sort(key=lambda x: float(x[0]))
                    
                with open(output,'a',encoding='utf-8') as a:
                    a.write(current_id)
                    a.write(current_text)
                    for s in l:
                        for w in s:
                            a.write(w+'\t')
                        a.write('\n')
                    a.write('\n')

                # reset dict for next sentence
                
                sen = {}
            else:

                if re.search(r'\d \d', line):
                    line = re.sub(r'(\d) (\d)',r'\1\2',line)
                
                columns = line.split()

                if '.' in columns[0]:
                    word_num = re.sub(r'(\d).\d',r'\1',columns[0])

                elif '-' in columns[0]:
                    word_num = re.sub(r'(\d)-\d',r'\1',columns[0])

                else:
                    word_num = columns[0]
                    
                word = columns[1]
                lemma = columns[2]
                POS = columns[3]
                pos = columns[4]
                agr = columns[5]
                head_num = columns[6]
                deprel = columns[7]
                rel_detail = columns[8]
                final = columns[9]
                sen[word_num] = {}
                sen[word_num]['number'] = word_num
                sen[word_num]['word'] = word
                sen[word_num]['lemma'] = lemma
                sen[word_num]['POS'] = POS
                sen[word_num]['pos'] = pos
                sen[word_num]['agr'] = agr
                sen[word_num]['head_num'] = head_num
                sen[word_num]['deprel'] = deprel
                sen[word_num]['rel_detail'] = rel_detail
                sen[word_num]['final'] = final
                sen[word_num]['new_number'] = word_num
            
            if current_text_split != [] and line != '\n' and line.split()[1] == current_text_split[-1]: # erst auf PostP pruefen, wenn der ganze Satz eingelesen ist
                
                if condition == 'make_prep':
                    for i in sen.keys():
                        found_earliest = False
                        if sen[i]['POS'] == 'ADP' and sen[i]['deprel'] == 'case':
                        
                            head = sen[i]['head_num']
                            pos_head = sen[head]['POS']
                        
                            int_head = int(sen[i]['head_num'])
                            int_dep = int(sen[i]['number'])

                            if pos_head in ['NOUN','PRON','PROPN','NUM'] and int_head < int_dep:
                                # we have found a postposition
                                # now find earliest word that depends on the noun

                                for potential_np in sen.keys(): # sucht nach Kopf-Nomen 
                                    # it either is the noun itself or depends on the noun
                                
                                    if sen[potential_np]['number'] == head:
                                                    
                                        int_new_head_number = int_head+1
                                        new_head_number = str(int_new_head_number)
                                        sen[head]['new_number'] = new_head_number

                                        new_dep_number = head
                                        sen[i]['new_number'] = new_dep_number

                                        # Adp muss an richtige Position des Kopfes verweisen, siebte Stelle des Worteintrags
                                        sen[i]['head_num'] = new_head_number 
                                        detail = sen[i]['rel_detail']
                                        detail_without_numbers = re.sub(r'[0-9]', '',detail)
                                        new_detail = new_head_number+detail_without_numbers
                                        sen[i]['rel_detail'] = new_detail

                                        for k in sen.keys():
                                            position = sen[k]['number']
                                            int_position = int(position)
                                            if int_position > int_head and int_position < int_dep:
                                                sen[k]['new_number'] = str(int_position+1)

                                for potential_np in sen.keys(): # sucht nach potentiellen Dependenten in der NP
                                    
                                    if sen[potential_np]['head_num'] == head:
                                        int_new_head_number = int_head+1
                                        new_head_number = str(int_new_head_number)
                                        sen[potential_np]['head_num'] = new_head_number
                                        detail = sen[potential_np]['rel_detail']
                                        detail_without_numbers = re.sub(r'[0-9]', '',detail)
                                        new_detail = new_head_number+detail_without_numbers
                                        sen[potential_np]['rel_detail'] = new_detail

                                        int_potential_np = int(sen[potential_np]['number'])
                                        
                                        if found_earliest == False and sen[potential_np]['number'] != head and int_new_head_number > int_potential_np:
                                            
                                            found_earliest = True

                                            sen[i]['new_number'] = sen[potential_np]['number']
                                            sen[potential_np]['new_number'] = str(int_potential_np+1)

                                            for other_np_parts in sen.keys():
                                                int_other_np_parts = int(sen[other_np_parts]['number'])
                                                if sen[other_np_parts]['number'] != sen[i]['number'] and sen[other_np_parts]['number'] != sen[head]['number'] and sen[other_np_parts]['number'] != sen[potential_np]['number'] and int_other_np_parts > int_potential_np and int_head > int_other_np_parts:
                                                    int_new_other_part_number = int(sen[other_np_parts]['number'])+1
                                                    sen[other_np_parts]['new_number'] = str(int_new_other_part_number)
                                            
                            
                            
                            
                            
        #print(sen)
        #print(len(sen))
            
                
### es gibt Zeilen wie:
### 2-3	ettei	_	_	_	_	_	_	_	_
### auch probelmatisch:
#5	oven	ovi	NOUN	N	Case=Gen|Number=Sing	3	obl	3:obl|8.1:obl	_
#6	lävitse	lävitse	ADP	Adp	AdpType=Post	5	case	5:case	_
#7	tai	tai	CCONJ	C	_	9	cc	8.1:cc|9:cc	_
#8	joskus	joskus	ADV	Adv	_	9	orphan	8.1:advmod	_
#8.1	kuuluu	kuulua	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	_	_	3:conj	_

# sent_id = e1039.14
# text = Uudelle Saksalle annettiin 110 000 tonnin kiintiö.
#1	Uudelle	uusi	ADJ	A	Case=All|Degree=Pos|Number=Sing	2	amod	2:amod	_	
#2	Saksalle	Saksa	PROPN	N	Case=All|Number=Sing	3	obl	3:obl	_	
#3	annettiin	antaa	VERB	V	Mood=Ind|Tense=Past|VerbForm=Fin|Voice=Pass	0	root	0:root	_	
#4	110	000	110	000	NUM	Num	NumType=Card	5	nummod	
#5	tonnin	tonni	NOUN	N	Case=Gen|Number=Sing	6	nmod:poss	6:nmod:poss	_	
#6	kiintiö	kiintiö	NOUN	N	Case=Nom|Number=Sing	3	obj	3:obj	SpaceAfter=No	
#7	.	.	PUNCT	Punct	_	3	punct	3:punct	_

# # text = Itse asiassa odotan, että valvontajakson päättyessä pääsen siivouksen ja leipomisen pariin. :)
# text = Olen kyllä edelleen sitä mieltä, että pieni pakkanen lumen kera on pitkässä juoksussa lämpimämpää kuin lumeton pimeys ja ainainen kosteus…

# 1	Tasanteella	tasanne	NOUN	N	Case=Ade|Number=Sing	0	root	0:root|1.1:obl	_
# 1.1	mennään	mennä	VERB	_	Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Pass	_	_	0:root	_
# 2	ohi	ohi	ADP	Adp	AdpType=Prep	4	case	4:case	_

# x.1 nur bei Verben -> kann wohl weg
# x-x immer Satzeinleiter, unterbrechen also keine NPs und können weg

# sent_id = t023.1
# text = Espanjan lainakorko lähellä "pelastusrajaa"
#1	Espanjan	Espanja	PROPN	N	Case=Gen|Number=Sing	2	nmod:poss	2:nmod:poss	_
#2	lainakorko	laina#korko	NOUN	N	Case=Nom|Number=Sing	5	nsubj:cop	5:nsubj:cop	_
#3	lähellä	lähellä	ADP	Adp	AdpType=Prep	5	case	5:case	_
#4	"	"	PUNCT	Punct	_	5	punct	5:punct	SpaceAfter=No
#5	pelastusrajaa	pelastus#raja	NOUN	N	Case=Par|Number=Sing	0	root	0:root	SpaceAfter=No
#6	"	"	PUNCT	Punct	_	5	punct	5:punct	_

#workaround -> zweites " durch . ersetzt

# der ging aber: # text = “Mä painan, mä painan!”

# der fliegt aus tdt_all_to_prep_target.conllu, weil das ud-wordlength Programm da keinen Satz bilden kann:
# sent_id = b306.1
# text = ONNELLISTA JOULUA : )
#1	ONNELLISTA	onnellinen	ADJ	A	Case=Par|Degree=Pos|Derivation=Llinen|Number=Sing	2	amod	2:amod	_	
#2	JOULUA	joulu	NOUN	N	Case=Par|Number=Sing	0	root	0:root	_	
#3	:	)	:	)	SYM	Symb	_	2	discourse

#der auch:
# sent_id = b301.1
# text = SIIVOUKSELLISTA SIELUNHOITOA : )
#1	SIIVOUKSELLISTA	siivouksellinen	ADJ	A	Case=Par|Derivation=Llinen|Number=Sing	2	amod	2:amod	_	
#2	SIELUNHOITOA	sielun#hoito	NOUN	N	Case=Par|Number=Sing	0	root	0:root	_	
#3	:	)	:	)	SYM	Symb	_	2	discourse

# und der (hat ADP!!!!!!!!!!!!!!!!):
# sent_id = b301.20
# text = Samalla voisi laatikon päälle kirjoittaa: ”Tämän lapseni heittävät roskiin purkaessaan jäämistöäni vuonna XXXX…” : D
#1	Samalla	samalla	ADV	Adv	_	5	advmod	5:advmod	_	
#2	voisi	voida	AUX	V	Mood=Cnd|Number=Sing|Person=0|VerbForm=Fin|Voice=Act	5	aux	5:aux	_	
#3	laatikon	laatikko	NOUN	N	Case=Gen|Number=Sing	5	obl	5:obl	_	
#4	päälle	päälle	ADP	Adp	AdpType=Post	3	case	3:case	_	
#5	kirjoittaa	kirjoittaa	VERB	V	InfForm=1|Number=Sing|VerbForm=Inf|Voice=Act	0	root	0:root	SpaceAfter=No	
#6	:	:	PUNCT	Punct	_	10	punct	10:punct	_	
#7	”	”	PUNCT	Punct	_	10	punct	10:punct	SpaceAfter=No	
#8	Tämän	tämä	PRON	Pron	Case=Gen|Number=Sing|PronType=Dem	10	obj	10:obj	_	
#9	lapseni	lapsi	NOUN	N	Case=Nom|Number=Plur|Number[psor]=Sing|Person[psor]=1	10	nsubj	10:nsubj	_	
#10	heittävät	heittää	VERB	V	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	5	parataxis	5:parataxis	_	
#11	roskiin	roska	NOUN	N	Case=Ill|Number=Plur	10	obl	10:obl	_	
#12	purkaessaan	purkaa	VERB	V	Case=Ine|InfForm=2|Number=Sing|Person[psor]=3|VerbForm=Inf|Voice=Act	10	advcl	10:advcl	_	
#13	jäämistöäni	jäämistö	NOUN	N	Case=Par|Number=Sing|Number[psor]=Sing|Person[psor]=1	12	obj	12:obj	_	
#14	vuonna	vuosi	NOUN	N	Case=Ess|Number=Sing	12	obl	12:obl	_	
#15	XXXX	XXXX	SYM	Symb	_	14	nmod	14:nmod	SpaceAfter=No	
#16	…	…	PUNCT	Punct	_	10	punct	10:punct	SpaceAfter=No	
#17	”	”	PUNCT	Punct	_	10	punct	10:punct	_	
#18	:	D	:	D	SYM	Symb	_	5	discourse

# und der (hat ADP!!!!!!!!!!!!!!!!!!):
# sent_id = b301.25
# text = Itse asiassa sen jälkeen löytyy aivan uusi energia sille tekemiselle, jonka tavaranpaljous on aiemmin tukahduttanut! : )
#1	Itse	itse	ADV	Adv	_	5	advmod	5:advmod	_	
#2	asiassa	asiassa	ADV	Adv	_	1	fixed	1:fixed	_	
#3	sen	se	PRON	Pron	Case=Gen|Number=Sing|PronType=Dem	5	obl	5:obl	_	
#4	jälkeen	jälkeen	ADP	Adp	AdpType=Post	3	case	3:case	_	
#5	löytyy	löytyä	VERB	V	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	0:root	_	
#6	aivan	aivan	ADV	Adv	_	7	advmod	7:advmod	_	
#7	uusi	uusi	ADJ	A	Case=Nom|Degree=Pos|Number=Sing	8	amod	8:amod	_	
#8	energia	energia	NOUN	N	Case=Nom|Number=Sing	5	nsubj	5:nsubj	_	
#9	sille	se	PRON	Pron	Case=All|Number=Sing|PronType=Dem	10	det	10:det	_	
#10	tekemiselle	tekeminen	NOUN	N	Case=All|Derivation=Minen|Number=Sing	8	nmod	8:nmod	SpaceAfter=No	
#11	,	,	PUNCT	Punct	_	16	punct	16:punct	_	
#12	jonka	joka	PRON	Pron	Case=Gen|Number=Sing|PronType=Rel	16	obj	16:obj	_	
#13	tavaranpaljous	tavara#paljous	NOUN	N	Case=Nom|Derivation=Vs|Number=Sing	16	nsubj	16:nsubj	_	
#14	on	olla	AUX	V	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	16	aux	16:aux	_	
#15	aiemmin	aiemmin	ADV	Adv	_	16	advmod	16:advmod	_	
#16	tukahduttanut	tukahduttaa	VERB	V	Case=Nom|Number=Sing|PartForm=Past|VerbForm=Part|Voice=Act	10	acl:relcl	10:acl:relcl	SpaceAfter=No	
#17	!	!	PUNCT	Punct	_	5	punct	5:punct	_	
#18	:	)	:	)	SYM	Symb	_	5	discourse

# und der:
# sent_id = b301.26
# text = Antoisaa viikonloppua! : )
#1	Antoisaa	antoisa	ADJ	A	Case=Par|Degree=Pos|Number=Sing	2	amod	2:amod	_	
#2	viikonloppua	viikon#loppu	NOUN	N	Case=Par|Derivation=U|Number=Sing	0	root	0:root	SpaceAfter=No	
#3	!	!	PUNCT	Punct	_	2	punct	2:punct	_	
#4	:	)	:	)	SYM	Symb	_	2	discourse

# und der (hat ADP!!!!!!!!!!!!!!!!):
# sent_id = b304.1
# text = ARKIPUUHIEN PARIIN : )
#1	ARKIPUUHIEN	arki#puuha	NOUN	N	Case=Gen|Number=Plur	0	root	0:root	_	
#2	PARIIN	pariin	ADP	Adp	AdpType=Post	1	case	1:case	_	
#3	:	)	:	)	SYM	Symb	_	1	discourse

# und der:
# sent_id = b309.1
# text = ILO UUDESTA TUOKSUSTA : )
#1	ILO	ilo	NOUN	N	Case=Nom|Number=Sing	0	root	0:root	_	
#2	UUDESTA	uusi	ADJ	A	Case=Ela|Degree=Pos|Number=Sing	3	amod	3:amod	_	
#3	TUOKSUSTA	tuoksu	NOUN	N	Case=Ela|Derivation=U|Number=Sing	1	nmod	1:nmod	_	
#4	:	)	:	)	SYM	Symb	_	1	discourse

# Problem, weil Kopf von valtavan paksun ist:

# sent_id = fC01.6
# text = Nousin vaunuuni ja ahtauduin valtavan paksun miehen viereen käytäväpaikalle.
#1	Nousin	nousta	VERB	V	Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act	0	root	0:root	_
#2	vaunuuni	vaunu	NOUN	N	Case=Ill|Number=Sing|Number[psor]=Sing|Person[psor]=1	1	obl	1:obl	_
#3	ja	ja	CCONJ	C	_	4	cc	4:cc	_
#4	ahtauduin	ahtautua	VERB	V	Mood=Ind|Number=Sing|Person=1|Tense=Past|VerbForm=Fin|Voice=Act	1	conj	1:conj	_
#5	valtavan	valtava	ADJ	A	Case=Gen|Degree=Pos|Number=Sing	6	amod	6:amod	_
#6	paksun	paksu	ADJ	A	Case=Gen|Degree=Pos|Number=Sing	7	amod	7:amod	_
#7	miehen	mies	NOUN	N	Case=Gen|Number=Sing	4	obl	4:obl	_
#8	viereen	viereen	ADP	Adp	AdpType=Post	7	case	7:case	_
#9	käytäväpaikalle	käytävä#paikka	NOUN	N	Case=All|Number=Sing	4	obl	4:obl	SpaceAfter=No
#10	.	.	PUNCT	Punct	_	1	punct	1:punct	_
