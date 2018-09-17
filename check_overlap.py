from prepare_to_attention_all_you_need_format import remove_delimiter_one_sentence
import sys

def check_overlap(f1_path, f2_path):
	with open(f1_path, 'r', encoding='gb18030') as f:
		lines = f.readlines()
	for ix, line in enumerate(lines):
		lines[ix] = (line.strip().split('\t'))

	overlap_set = set()
	for en, zh in lines:
		en = remove_delimiter_one_sentence(en)
		zh = remove_delimiter_one_sentence(zh)
		overlap_set.add((en,zh))

	with open(f2_path, 'r', encoding='utf-8') as f:
		lines = f.readlines()

	for ix, line in enumerate(lines):
		lines[ix] = (line.strip().split('\t'))

	count = 0
	for en, zh in lines:
		if (en, zh) in overlap_set:
			count += 1

	return count

if __name__ == '__main__':
	f1_path = sys.argv[1]
	f2_path = sys.argv[2]
	check_overlap(f1_path, f2_path)
