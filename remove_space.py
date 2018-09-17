import sys
import codecs

def remove_space(file_path, out_file_path, encoding):
    lines = []
    with codecs.open(file_path, 'r', encoding=encoding):
        for line in f:
            line = line.replace(' ', '')
            lines.append(line)
    with codecs.open(out_file_path, 'w', encoding=encoding):
        f.writelines(lines)

if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    encoding = sys.argv[3]
    remove_space(in_file, out_file, encoding)
