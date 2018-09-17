import sys
import os
from os.path import join
import random

def remove_delimiter_one_sentence(sen):
    delimiters = "[《》<>\"':：\、\|“”‘’]{}（）{}【】()｛｝（）：、~——+％%`:“”＂\'‘/\\_——".replace(" ", "")
    new_sen = sen
    while True:
        sen_len = len(new_sen)
        for c in delimiters:
            d_str = c
            new_sen = new_sen.replace(d_str, "").replace("  ", " ")
        if len(new_sen) == sen_len:
            return new_sen
    return ""


def convert(in_file,out_file_train_cxt, out_file_train_en, out_file_train_zh, out_file_dev_cxt, out_file_dev_en, out_file_dev_zh, remove_delimiter, remove_space, p, limit=800000):
    random.seed()
    line_count = 0
    line_count_train = 0
    line_count_dev = 0
    with open(in_file, encoding = "utf-8") as in_f:
        list_train = []
        list_dev = []
        for line in in_f:
            line_count += 1
            if line_count % 1000 == 0:
                print(str(line_count))
            x = random.random()
            line = line.rstrip()
            # [en, zh, count] = line.split("\t")
            splits = line.split('\t')

            if remove_delimiter:
                splits = map(remove_delimiter_one_sentence, splits)
            if remove_space:
                splits = map(lambda x: x.replace(" ", ''), splits)
            splits = list(splits)
            context, en, zh = splits[:-2], splits[-2], splits[-1]
            if len(en) == 0 or len(zh) == 0:
                continue
            # create single_round chat data
            single_round = True
            if single_round:
                data = create_single_round_data(splits)
            for item in data:
                en, zh = item
                context = ""
                if x <= p:
                    list_train.append((context, en, zh))
                    line_count_train += 1
                else:
                    list_dev.append((context, en, zh))
                    line_count_dev += 1
            if line_count > limit:
                break
    shuffle_output(list_train, out_file_train_en, out_file_train_zh, out_file_train_cxt)
    shuffle_output(list_dev, out_file_dev_en, out_file_dev_zh, out_file_dev_cxt)
    print(str(line_count) + "\t" + str(line_count_train) + "\t" + str(line_count_dev))

def create_single_round_data(splits, step=1):
    ret = []
    for ix in range(0, step, len(splits)-1):
        ret.append((splits[ix], splits[ix+1]))
    return ret

def create_single_round_data_pd(splits):
	ret = []
	for ix in range(len(splits)-1):
		if splits[ix][0] == 'p':
            ret.append((splits[ix], splits[ix+1])
        else:
            continue
    return ret

def shuffle_output(list, out_file_name_en, out_file_name_zh, out_file_name_context):
    random.shuffle(list)
    with open(out_file_name_en, "w", encoding="utf-8") as out_f_en:
        with open(out_file_name_zh, "w", encoding="utf-8") as out_f_zh:
            with open(out_file_name_context, 'w', encoding="utf-8") as out_f_cxt:
                for cxt, en, zh in list:
                    out_f_en.write(en)
                    out_f_en.write("\n")
                    out_f_zh.write(zh)
                    out_f_zh.write("\n")
                    out_f_cxt.write("\t".join(cxt))
                    out_f_cxt.write("\n")


if __name__ == "__main__":
    in_file = sys.argv[1]
    out_dir = sys.argv[2]
    out_file_train_en = join(out_dir, "train.en")
    out_file_train_zh = join(out_dir, "train.zh")
    out_file_train_context = join(out_dir, 'train.cxt')
    out_file_dev_en = join(out_dir, "dev.en")
    out_file_dev_zh = join(out_dir, "dev.zh")
    out_file_dev_context = join(out_dir, 'dev.cxt')
    remove_delimiter = int(sys.argv[3]) == 1
    remove_space = int(sys.argv[4]) == 1

    convert(in_file, out_file_train_context, out_file_train_en, out_file_train_zh, out_file_dev_context, out_file_dev_en, out_file_dev_zh, remove_delimiter, remove_space, 0.98)
