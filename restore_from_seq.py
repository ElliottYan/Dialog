import codecs
import sys
from collections import defaultdict

def restore(f1, f2, out_f):
    with codecs.open(f1, 'r', encoding='gb18030', errors='ignore') as f:
        lines1 = f.readlines()

    with codecs.open(f2, 'r', encoding='gb18030', errors='ignore') as f:
        lines2 = f.readlines()

    ret_dict = defaultdict(list)
    count = 0
    for ix in range(len(lines1)):
        role, id = lines2[ix].strip().split('\t')
        id = int(id)
        if not ret_dict[id]:
            if role != 'p':
                count += 1
        ret_dict[id].append(role+':'+lines1[ix].strip())
    print("There are {} sessions don't start with p!".format(count))

    with codecs.open(out_f, 'w', encoding='gb18030', errors='ignore') as f:
        count = 0
        for _, val in ret_dict.items():
            count += 1
            if count % 1000000 == 0:
                print('Processed {} lines.'.format(count))
            f.write("\t".join(val) + '\n')

f1 = sys.argv[1]
f2 = sys.argv[2]
out_f = sys.argv[3]

restore(f1, f2, out_f)
