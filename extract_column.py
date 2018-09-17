import codecs
import sys

def retrieve_column(k, f_path, out_f_path):
    ret = []
    k = int(k)
    with codecs.open(f_path, 'r', encoding='gb18030', errors='ignore') as f:
        for line in f:
            ret.append(line.strip().split('\t')[k] + '\n')
    with codecs.open(out_f_path, 'w', encoding='gb18030', errors='ignore') as f:
        f.writelines(ret)

k = sys.argv[1]
in_f = sys.argv[2]
out_f = sys.argv[3]
retrieve_column(k, in_f, out_f)
