import json
import sys
import pdb
import codecs
from collections import defaultdict

def import_to_dataset(inf, dataset_file):
    ret = []
    with codecs.open(inf, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # for ix in range(len(lines)):
        # lines[ix] = lines[ix].encode('utf-8', errors='ignore')
    ix = 1
    ret = defaultdict(list)
    order = ['inputs:', 'decodes:', 'targets:']
    while ix < len(lines):
        line = lines[ix]
        if line.strip().isdigit():
            # tmp = []
            ix += 1
            continue
        if not line.strip():
            ix += 1
            continue
        tt = []
        for i in range(4):
            line = lines[ix]
            ix += 1
            if i == 3:
                continue
            # strip some weird chars
            splits = line.strip().split('\t')
            if line.startswith('targets') and not (splits[-1].isdigit() and splits[-2].isdigit()):
                splits.append('2')
            if len(splits) > 1:
                line_text = "".join(splits[:-2])
                try:
                    score = int(splits[-2])
                    valid_for_test = int(splits[-1])
                except:
                    pdb.set_trace()
            elif len(splits) == 1:
                line_text = splits[0]
            # replace all spaces
            line_text = line_text[len(order[i]):].strip().replace(' ','')
            tt.append(line_text)
            if i == 2:
                score = int(splits[-2])
                valid_for_test = int(splits[2])

        ret['\t'.join(tt[:2])]= (score, valid_for_test)
    print("finish reading files.")
    with open(dataset_file, 'r') as f:
        tmp = json.load(f)
    tmp.update(ret)

    with open(dataset_file, 'w') as f:
        json.dump(ret, f)


f1 = sys.argv[1]
out_f = sys.argv[2]
import_to_dataset(f1, out_f)
