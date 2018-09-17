import sys
import pdb
import codecs

def clean_medical(in_file, out_file, in_encoding='utf-8', out_encoding='utf-8'):
    with open(in_file, 'rb') as in_f:
        lines = in_f.readlines()
    # decode makes the binary to unicode encoding
    lines = [line.decode(encoding=in_encoding, errors='ignore') for line in lines]
    ret = []
    for line in lines:
        # remove some unuseful infos
        line_text = line.strip()
        splits = line_text.split('\t')[2:]
        tmp = []
        previous = ''
        roles = []
        for ix, split in enumerate(splits):
            role = split[:4]
            split_text = split[4:].strip()
            if previous == role:
                tmp[-1] += " " + split_text
            else:
                previous = role
                tmp.append(split_text)
                roles.append(role[0])
        ret.append(("\t".join(tmp)+'\n').encode(out_encoding, errors='ignore'))

    with codecs.open(out_file, 'wb') as out_f:
        out_f.writelines(ret)

if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    in_encoding = sys.argv[3]
    out_encoding = sys.argv[4]
    clean_medical(in_file, out_file, in_encoding=in_encoding, out_encoding=out_encoding)
