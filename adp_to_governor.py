import argparse
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import TweetTokenizer
tokenizer = TweetTokenizer()

if __name__ == '__main__':

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
                    ll = [sen[i]['number']] 
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

                sen[word_num]['new_head'] = head_num
                #sen[word_num]['new_rel_detail'] = rel_detail
            
            if current_text_split != [] and line != '\n' and line.split()[1] == current_text_split[-1]: # erst auf Adp pruefen, wenn der ganze Satz eingelesen ist
                
                for i in sen.keys():
                    
                    if sen[i]['POS'] == 'ADP' and sen[i]['deprel'] == 'case':
                        
                        head = sen[i]['head_num']
                        pos_head = sen[head]['POS']

                        detail = sen[i]['rel_detail']
                        detail_without_numbers = re.sub(r'[0-9]', '',detail)

                        head_detail = sen[head]['rel_detail']
                        head_detail_without_numbers = re.sub(r'[0-9]', '', head_detail)

                        if pos_head in ['NOUN','PRON','PROPN','NUM']:
                            # we have found an adposition

                            v = sen[head]['head_num']

                            sen[i]['new_head'] = v
                            sen[head]['new_head'] = sen[i]['number']
             
                            new_detail = v+detail_without_numbers
                            sen[i]['rel_detail'] = new_detail

                            new_head_detail = sen[i]['number']+head_detail_without_numbers
                            sen[head]['rel_detail'] = new_head_detail
