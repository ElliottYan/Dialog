import sys
import pdb
import codecs

def clean_medical(in_file, out_file, in_encoding='utf-8', out_encoding='utf-8'):
    with open(in_file, 'rb') as in_f:
        lines = in_f.readlines()
    # decode makes the binary to unicode encoding
    lines = [line.decode(encoding=in_encoding, errors='ignore') for line in lines]
    ret = []
    ret_roles = []
    count = 0
    errors = []
    for ix, line in enumerate(lines):
        # remove some unuseful infos
        line_text = line.strip()
        splits = line_text.split('\t')[2:]
        tmp = []
        previous = ''
        roles = []
        break_flag = 0
        for j, split in enumerate(splits):
            role = split[:4]
            if role[0] not in {'p', 'd'}:
                # pdb.set_trace()
                count += 1
                break_flag = 1
                break
            split_text = split[4:].strip()
            if previous == role:
                tmp[-1] += " " + split_text
            else:
                previous = role
                # remove space
                split_text = split_text.replace(' ','') + '\n'
                split_text = split_text.encode(out_encoding, errors='ignore')
                if split_text.strip():
                    tmp.append(split_text)
                    roles.append("{}\t{}\n".format(role[0], str(ix)))
                else:
                    break_flag = 1
                    break
        if not ix % 10000:
            print('Processed {} lines!'.format(str(ix)))
        if not break_flag:
            ret += tmp
            ret_roles += roles
        else:
            errors.append(line + '\n')
    print("Skip {} lines".format(str(count)))

    # this format is for tokenization.
    assert len(ret) == len(ret_roles)

    with codecs.open(out_file, 'wb') as out_f:
        with codecs.open(out_file + '.roles', 'wb') as out_f2:
            for ix in range(len(ret)):
                # line = ret[ix].encode(out_encoding, errors='ignore')
                line = ret[ix]
                ret_role = ret_roles[ix]
                out_f.write(line)
                out_f2.write(ret_role)

    with codecs.open(out_file + '.errors', 'wb', encoding=in_encoding, errors='ignore') as out_f:
        for line in errors:
            out_f.write(line)


if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    in_encoding = sys.argv[3]
    out_encoding = sys.argv[4]
    clean_medical(in_file, out_file, in_encoding=in_encoding, out_encoding=out_encoding)
