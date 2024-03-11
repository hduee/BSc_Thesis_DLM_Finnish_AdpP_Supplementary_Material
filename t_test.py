import argparse
import re
import math

parser = argparse.ArgumentParser()
parser.add_argument('input_file_one', help='input file')
parser.add_argument('input_file_two', help='input file')
args = parser.parse_args()

file_one = args.input_file_one
file_two = args.input_file_two

total_len_one = 0
num_sen_one = 0

current_sen_len_one = 0
current_sen_dep_one = 0
avg_for_words_one = 0

avg_dep_len_of_each_sen_one = []

with open(file_one, 'r', encoding='utf-8') as f:
    for line in f:
        if '# sent_id' in line:
            num_sen_one += 1
        elif '# text' in line:
            continue
        elif line == '\n':
            avg_dep_len_of_each_sen_one.append(current_sen_dep_one / current_sen_len_one)
            avg_for_words_one += current_sen_dep_one / current_sen_len_one
            current_sen_dep_one = 0
            current_sen_len_one = 0
        else:
            current_sen_len_one += 1
            
            if re.search(r'\d \d', line):
                    line = re.sub(r'(\d) (\d)',r'\1\2',line)
                    
            l = line.split()

            if '.' in l[0]:
                l[0] = re.sub(r'(\d).\d',r'\1',l[0])

            if '-' in l[0]:
                l[0] = re.sub(r'(\d)-\d',r'\1',l[0])
                    
            if l[7] != 'root' and l[6] != '_' and l[6] != 'Symb':
                dep = abs(int(l[0]) - int(l[6]))
                current_sen_dep_one += dep
                total_len_one += dep

total_len_two = 0
num_sen_two = 0

current_sen_len_two = 0
current_sen_dep_two = 0
avg_for_words_two = 0

avg_dep_len_of_each_sen_two = []

with open(file_two, 'r', encoding='utf-8') as f:
    for line in f:
        if '# sent_id' in line:
            num_sen_two += 1
        elif '# text' in line:
            continue
        elif line == '\n':
            avg_dep_len_of_each_sen_two.append(current_sen_dep_two / current_sen_len_two)
            avg_for_words_two += current_sen_dep_two / current_sen_len_two
            current_sen_dep_two = 0
            current_sen_len_two = 0
        else:
            current_sen_len_two += 1
            
            if re.search(r'\d \d', line):
                    line = re.sub(r'(\d) (\d)',r'\1\2',line)
                    
            l = line.split()

            if '.' in l[0]:
                l[0] = re.sub(r'(\d).\d',r'\1',l[0])

            if '-' in l[0]:
                l[0] = re.sub(r'(\d)-\d',r'\1',l[0])
                    
            if l[7] != 'root' and l[6] != '_' and l[6] != 'Symb':
                dep = abs(int(l[0]) - int(l[6]))
                current_sen_dep_two += dep
                total_len_two += dep

pairwise_dif = [abs(x-y) for x,y in zip(avg_dep_len_of_each_sen_one, avg_dep_len_of_each_sen_two)]
avg_of_pairwise_dif = sum(pairwise_dif) / num_sen_one

squared_deviations = [(x-avg_of_pairwise_dif)**2 for x in pairwise_dif]

variance = sum(squared_deviations)/ num_sen_one

sd = math.sqrt(variance)

t = (avg_of_pairwise_dif) / (sd / math.sqrt(num_sen_one))

print('length of avg dependency = '+str(avg_for_words_one/num_sen_one)+'\t'+str(avg_for_words_two/num_sen_two))
print(num_sen_one)
print(num_sen_two)
print(t)
