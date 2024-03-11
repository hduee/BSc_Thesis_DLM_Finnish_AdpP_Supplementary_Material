import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='input file')
args = parser.parse_args()

file = args.input_file

total_len = 0
num_sen = 0

current_sen_len = 0
current_sen_dep = 0
avg_for_words = 0

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        if '# sent_id' in line:
            num_sen += 1
        elif '# text' in line:
            continue
        elif line == '\n':
            avg_for_words += current_sen_dep / current_sen_len
            current_sen_dep = 0
            current_sen_len = 0
        else:
            current_sen_len += 1
            
            if re.search(r'\d \d', line):
                    line = re.sub(r'(\d) (\d)',r'\1\2',line)
                    
            l = line.split()

            if '.' in l[0]:
                l[0] = re.sub(r'(\d).\d',r'\1',l[0])

            if '-' in l[0]:
                l[0] = re.sub(r'(\d)-\d',r'\1',l[0])
                    
            if l[7] != 'root' and l[6] != '_' and l[6] != 'Symb':
                dep = abs(int(l[0]) - int(l[6]))
                current_sen_dep += dep
                total_len += dep

avg = total_len / num_sen

print('total dep len = '+str(total_len))
print('number of sentences = '+str(num_sen))
print('avg dependency length of a sentence = '+str(avg))
print('length of avg dependency = '+str(avg_for_words/num_sen))



###

# problem:
# 2	tulee	tulla	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin|Voice=Act	_	_	0:root	_
#bei Satz:
#Myöhemmin sitten se näyttö tai ehkä jopa jo nyt, sillä saatan [...]
# also _ durch 0 ersetzen

# auch:
#3.1	lisää	lisätä	VERB	_	Mood=Imp|Number=Sing|Person=2|VerbForm=Fin|Voice=Act	_	_	1:conj	_
#in
# Lisä mausteet ja halutessasi hieman...
# der Satz ist generell falsch annotiert???

#auch falsch annotiert?:
# Mörinä vain kuuluu suljetun oven lävitse tai joskus karjahdus...

#auch falsch:
#Punanen kenttä tonne päätyyn. tulee

#auch falsch:
# "eläinlääkintäalaa koskevalla lainsäädännöllä": direktiivin 89/662/ETY...

#auch falsch:
# "todistuksia myöntävillä viranomaisilla": virkaeläinlääkäriä tai, mikäli...
