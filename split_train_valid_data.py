from sklearn.model_selection import train_test_split
import sys, os
import argparse

def get_train_val_set(xml_dir): 
    train_set = []#np.array([]).reshape(-1, 1)
    test_set = []#np.array([]).reshape
    all_sub_dir = os.listdir(xml_dir)
    if '.DS_Store' in all_sub_dir: all_sub_dir.remove('.DS_Store')
    for sub_dir in all_sub_dir:
        file_names = os.listdir(os.path.join(xml_dir, sub_dir))
        if '.DS_Store' in file_names: file_names.remove('.DS_Store')
        for i in range(len(file_names)):
            file_names[i] = sub_dir + '/' + file_names[i].split('.')[0]
        train_names, test_names = train_test_split(file_names, 
        	test_size=0.33, random_state = 1)
        train_set.extend(train_names)
        test_set.extend(test_names)
    return train_set, test_set, len(train_set)+len(test_set)

def write_txt(data, txt_name):
	f = open(txt_name, 'w')
	for line in data:
		f.write(line + '\n')
	f.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Demo')
	parser.add_argument('--xml_dir', required=True)
	parser.add_argument('--output_dir', required=True)

	args = parser.parse_args()

	xml_dir = args.xml_dir
	output_dir = args.output_dir

	train_set, test_set, num_xml = get_train_val_set(xml_dir)
	print(num_xml)
	write_txt(train_set, os.path.join(output_dir, 'train.txt'))
	write_txt(test_set, os.path.join(output_dir, 'test.txt'))

