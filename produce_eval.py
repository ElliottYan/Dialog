import codecs
import sys
import os
from ndcg import read_in_decoder_output
reload(sys)
sys.setdefaultencoding('utf-8')

eval_dir = './chatbot/yard/hq_med_single/eval'
output_file_path = './chatbot/yard/hq_med_single/decodes.txt'
beam_size = 4

def produce_eval(eval_dir, output_file_path):
	decoder_outputs = read_in_decoder_output(eval_dir)

	with codecs.open(output_file_path, 'wb', encoding='utf-8') as f:
		for ix, item in enumerate(decoder_outputs):
			inputs, decodes, targets = item
			# each beam in decodes
			f.write(str(ix) + '\n')
			for decode in decodes.split('\t'):
				f.write('inputs: {}\n'.format(inputs))
				f.write('decodes: {}\n'.format(decode))
				f.write('targets: {}\n'.format(targets))
				f.write('\n')

def produce_eval_with_cxt(eval_dir, output_file_path, src_dev_dir):
	decoder_outputs = read_in_decoder_output(eval_dir)

	dev_sets = {}
	basename = os.path.join(src_dev_dir, 'dev')
	filenames = {
		basename + '.en',
		basename + '.zh',
		basename + '.cxt'
	}
	tmp = dict()
	for filename in filenames:
		with codecs.open(filename, 'r', encoding='utf-8') as f:
			tmp[filename.split('.')[-1]] = list(map(unicode.strip(), f.readlines()))
	ret = dict()
	for i in range(len(tmp['en'])):
		ret[(tmp['en'][i], tmp['zh'][i])] = tmp['cxt'][i]

	with codecs.open(output_file_path, 'wb', encoding='utf-8') as f:
		for ix, item in enumerate(decoder_outputs):
			inputs, decodes, targets = item
			# each beam in decodes
			f.write(str(ix) + '\n')
			for decode in decodes.split('\t'):
				f.write('context:{}\n').format(ret[(inputs, targets)].replace('\t', ' '))
				f.write('inputs: {}\n'.format(inputs.replace('\t', ' ')))
				f.write('decodes: {}\n'.format(decode.replace('\t', ' ')))
				f.write('targets: {}\n'.format(targets.replace('\t', ' ')))
				f.write('\n')






if __name__ == '__main__':
	eval_dir = sys.argv[1]
	output_file_path = sys.argv[2]
	src_dev_dir = None
	if len(sys.argv) > 3:
		src_dev_dir = sys.argv[3]
	if src_dev_dir:
		produce_eval_with_cxt(eval_dir, output_file_path, src_dev_dir)
	else:
		produce_eval(eval_dir, output_file_path)
