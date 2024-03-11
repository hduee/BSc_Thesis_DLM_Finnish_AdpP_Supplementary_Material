import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('output_file')
args = parser.parse_args()

with open(args.input_file, 'r', encoding='utf-8') as f:
    current_sen = ''
    for line in f:
        if line != '\n':
            current_sen = current_sen + line
        else:
            if 'ADP' in current_sen:
                with open(args.output_file, 'a', encoding='utf-8') as w:
                    w.write(current_sen+'\n')
            current_sen = ''
