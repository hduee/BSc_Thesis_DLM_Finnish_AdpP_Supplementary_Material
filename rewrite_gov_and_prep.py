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
                    ll.append(sen[i]['new_head'])
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
                sen[word_num]['new_head'] = head_num
            
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
                                                    
                            # now change adp to governor

                            detail = sen[i]['rel_detail']
                            detail_without_numbers = re.sub(r'[0-9]', '',detail)

                            head_detail = sen[head]['rel_detail']
                            head_detail_without_numbers = re.sub(r'[0-9]', '', head_detail)

                            v = sen[head]['head_num']

                            sen[i]['new_head'] = v
                            sen[head]['new_head'] = sen[i]['new_number']
             
                            new_detail = v+detail_without_numbers
                            sen[i]['rel_detail'] = new_detail

                            new_head_detail = sen[i]['new_number']+head_detail_without_numbers
                            sen[head]['rel_detail'] = new_head_detail
