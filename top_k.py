import math
import sys
import codecs
import os
import json
import pdb
from collections import defaultdict

def read_in_prelabeled_data(labeled_data):
    with open(labeled_data, 'r') as f:
        pre_labeled_sents = json.load(f)
    return pre_labeled_sents

# have to make sure only oen set of decoding results in this directory
def read_in_decoder_output(decoder_output_dir):
    files = os.listdir(decoder_output_dir)
    tmp_dict = defaultdict(list)
    # all this files should have same size
    for file_path in files:
        key = file_path.split('.')[-1]
        with codecs.open(os.path.join(decoder_output_dir, file_path), 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            tmp_dict[key].append(line.strip())

    # need a standard to define a response.
    decoder_output = list(zip(tmp_dict['input'], tmp_dict['decode'], tmp_dict['target']))
    return decoder_output

def read_in_decoder_output_v2(decoder_output_file, beam_size=4):
    with codecs.open(decoder_output_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # for ix in range(len(lines)):
        # lines[ix] = lines[ix].encode('utf-8', errors='ignore')
    ix = 1
    ret = []
    order = ['inputs:', 'decodes:', 'targets:']
    # ix is the global index
    while ix < len(lines):
        # print(ix)
        beam_result = []
        j = 0
        # j is the index inside a beam
        while j < beam_size and ix < len(lines):
            # pdb.set_trace()
            line = lines[ix]
            if line.strip().isdigit():
                ix += 1
                continue
            if not line.strip():
                ix += 1
                continue
            tt = []
            for i in range(3):
                try:
                    line = lines[ix]
                except:
                    pdb.set_trace()
                ix += 1
                if i == 3:
                    continue
                # strip some weird chars
                line_text = line.strip()
                if not line_text.startswith(order[i]):
                    pdb.set_trace()
                line_text = line_text[len(order[i]):].strip().replace(' ','')
                tt.append(line_text)
            j += 1

            beam_result.append('\t'.join(tt[:2]))
        ret.append(beam_result)
    return ret

def top_k(pre_defined_sents, decoder_output, beam_size, k=1):
    """
        Inputs: pre_defined_sents, dict
                decoder_output, list
                beam_size, int
        Return: Average NDCG, float
    """
    ret = []
    rels = []
    accs = []
    # for item in decoder_output:
    ix = 0
    count = 0
    while ix < len(decoder_output):
        # item = decoder_output[ix]
        DCG = 0
        query = decoder_output[ix][0].strip().replace(' ', '')
        # list of beam_size
        outputs = decoder_output[ix][1].replace(' ','').split('\t')
        break_flag = 0
        scores = []
        valids = []
        for j in range(beam_size):
            # output = item[j][1].strip().replace(' ', '')
            try:
                key = '\t'.join([query, outputs[j].strip()])
            except:
                pdb.set_trace()
            if key in pre_defined_sents:
                count += 1
                score = pre_defined_sents[key][0]
                # make sure the result divisor is bigger than 0
                # score starts from 0.
                is_valid_medical = pre_defined_sents[key][1]
                scores.append(score)
                if is_valid_medical != 2:
                    valids.append(is_valid_medical)
            else:
                ret.append(key)
                break_flag=1
        # max_DCG = gains.sort()
        if not break_flag:
            ave_relevance = float(sum(scores[:k])) / k
            rels.append(ave_relevance)
            if valids:
                med_acc = float(sum(valids[:k])) / k
                accs.append(med_acc)
        ix += 1

    return sum(rels) / len(rels), sum(accs) / len(accs), ret


def main(args):
    labeled_file = sys.argv[1]
    decoder_output_dir = sys.argv[2]
    k = sys.argv[3]
    beam_size = 4
    pre_labeled_sents = read_in_prelabeled_data(labeled_file)
    # decoder_output = read_in_decoder_output_v2(decoder_output_file, beam_size=beam_size)
    decoder_output = read_in_decoder_output(decoder_output_dir)
    ave_relevance, medicial_accuracy, need_to_label_sents = top_k(pre_labeled_sents, decoder_output, beam_size, k=int(k))
    print(ave_relevance)
    print(medicial_accuracy)
    print(need_to_label_sents)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
