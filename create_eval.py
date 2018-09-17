import os
import random

data_dir = raw_input('please input the data dir.\n')
with open(os.path.join(data_dir, 'mydata_enzh_tok_dev.lang1'), 'r') as f:
	lang1 = f.readlines()
with open(os.path.join(data_dir, 'mydata_enzh_tok_dev.lang2'), 'r') as f:
	lang2 = f.readlines()

limit = 15
ret = []
for ix in range(len(lang1)):
	if len(lang1[ix]) < limit:
		continue
	ret.append((lang1[ix].strip(), lang2[ix].strip()))

random.shuffle(ret)

with open(os.path.join(data_dir, 'test.txt'), 'w') as f:
	for item in ret[:2000]:
		f.write("{}\t{}\n".format(item[0], item[1]))

with open(os.path.join(data_dir, 'mydata_enzh_tok_dev_2000.lang1'), 'w') as f:
	for item in ret[:2000]:
		f.write("{}\n".format(item[0]))

with open(os.path.join(data_dir, 'mydata_enzh_tok_dev_2000.lang2'), 'w') as f:
	for item in ret[:2000]:
		f.write("{}\n".format(item[1]))