'''
This script is for change the dialog to trainable sample for multi-turn model
'''

import sys
# import codecs

def prepare_dialog_to_multi(in_path, out_path, **kwargs):
    default_settings = {
        'in_enc':'gb18030',
        'out_enc':'gb18030',
        'douban': 0,
    }
    for item in kwargs:
        default_settings[item] = kwargs[item]
    ret = []
    # consider the encoding of 'gb18030'
    with open(in_path, 'r', encoding=default_settings['in_enc'], errors='ignore') as f:
        count = 0
        for line in f:
            count += 1
            if count % 1000 == 0:
                print(count)
            if not default_settings['douban']:
                line_samples = prepare_single_line(line)
            else:
                line_samples = prepare_single_line_douban(line)
            ret += line_samples
    with open(out_path, 'w', encoding=default_settings['out_enc'], errors='ignore') as f:
        f.writelines(ret)

# remove the identifier e.g., p:, d:
def prepare_single_line(line, delimiters='\t'):
    line = line.strip()
    splits = line.split(delimiters)
    # splits = [(item[0], item[2:]) for ]
    roles = [item[0] for item in splits]
    splits = [item[2:].strip() for item in splits]
    ret = []
    for i in range(len(splits)):
        if roles[i] == 'p':
            continue
        elif roles[i] == 'd':
            if i > 0:
                ret.append('\t'.join(splits[:i+1]) + '\n')
        else:
            return ret
    return ret

def prepare_single_line_douban(line, delimiters='\t'):
    ret = []
    line = line.strip()
    splits = line.split(delimiters)
    # splits = [(item[0], item[2:]) for ]
    for i in range(len(splits)):
        ret.append('\t'.join(splits[:i+1]) + '\n')
    return ret

f1 = sys.argv[1]
out_f = sys.argv[2]
kwargs = {}
if len(sys.argv) >= 4:
    kwargs['in_enc']= sys.argv[3]
    kwargs['out_enc'] = sys.argv[4]
if len(sys.argv) >= 6:
    kwargs['douban'] = sys.argv[5]
prepare_dialog_to_multi(f1, out_f, **kwargs)
