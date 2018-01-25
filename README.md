# pest-detection

## Data Clean
make sure the raw data has been cleaned.


## Split data into train and test set
**run**
```
python split_train_valid_data.py --xml_dir=/PATH TO YOUR DATA DIRECTORY/xml \
                                 --output_dir=/PATH TO YOUR DATA DIRECTORY
```
**--example** below command splits all xml files into train and test set, and outputs **train.txt** and **test.txt** in "/Users/liuziyi/private/pest-detection-project/data"
```
python split_train_valid_data.py --xml_dir=/Users/liuziyi/private/pest-detection-project/data/xml 
                                 --output_dir=/Users/liuziyi/private/pest-detection-project/data
```


## Create tensorflow record
**run**
```
python /PATH TO YOUR CODE DIRECTORY/create_tf_record.py --data_dir= /PATH TO YOUR DATA DIRECTORY \
                                                        --images_dir=images \
                                                        --annotations_dir=xml \
                                                        --set=train \
                                                        --labels_map_path=label_map.pbtxt \
                                                        --output_path=train.record
```
**--example** below command generate **train.record**
```
python /pest-detection-project/pest-detection/create_tf_record.py --data_dir=/pest-detection-project/data \
                                                                  --images_dir=images \
                                                                  --annotations_dir=xml \
                                                                  --set=train \
                                                                  --labels_map_path=label_map.pbtxt \
                                                                  --output_path=train.record
```
**--example** below command generate **test.record**
```
python /pest-detection-project/pest-detection/create_tf_record.py --data_dir=/pest-detection-project/data \
                                                                  --images_dir=images \
                                                                  --annotations_dir=xml \
                                                                  --set=test \
                                                                  --labels_map_path=label_map.pbtxt \
                                                                  --output_path=test.record
```
