## 项目概述
本项目基于计算机视觉技术，针对农田环境下的各类害虫目标进行实时检测（即定位、识别和计数）。项目基于Tensorflow机器学习框架和卷积神经网络为技术手段，在Tensorflow机器学习框架下进行开发，并可方便移植到Android等移动平台或云端。

## 数据情况

### 害虫类别
项目中所涉及检测种类为69种，涵盖常见稻田、茶园和果园害虫种类。具体细节如表1所示：


### 数据格式
由于本项目是基于Tensorflow机器学习框架进行，因此在构建模型时需要将数据由原始的JPEG格式转换为TF Record格式。具体的格式转换代码为
```
# From /pest-detection-project/pest-detection
python ./create_tf_record_plus_pad_images.py \
--data_dir=../data \
--images_dir=../images \
--annotations_dir=../xml \
--set=train \
--labels_map_path=label_map.pbtxt \
--output_path=train.record
```

## 检测模型

### 模型架构 
项目所采用检测模型为SSD-MobileNet模型，该模型的详细架构以及具体流程可以参见文件。

### 模型保存
保存后的模型包含6个文件，其名称和作用分别为
- checkpoint
- graph.pbtxt
- model.ckpt-44405.data-00000-of-00001
- model.ckpt-44405.index
- model.ckpt-44405.meta

为了能够调用模型，需要将模型保存为单个文件，调用如下命令：
```
# From /pest-detection-project/pest-dete
python export_inference_graph.py \
--input_type image_tensor \
--pipeline_config_path ../data/train/pipeline.config \
--trained_checkpoint_prefix ../data/train/model.ckpt-44405 \
--output_directory ../data/train/
```


# 训练模型
```
python /models/research/object_detection/train.py --logtostderr --train_dir=/pest-detection-project/data/train --pipeline_config_path=/pest-detection-project/data/ssd_mobilenet_v1_coco_2017_11_17/ssd_mobilenet_v1_coco.config
```

# 测试模型
```
python /models/research/object_detection/eval.py --logtostderr --pipeline_config_path=/pest-detection-project/data/train_2/pipeline.config --checkpoint_dir=/pest-detection-project/data/train_2 --eval_dir=/pest-detection-project/data/eval --run_once=True
```

# 应用模型
## freeze model
```
cd /pest-detection-project/pest-detection

python export_inference_graph.py \
--input_type image_tensor \
--pipeline_config_path ../data/train/pipeline.config \
--trained_checkpoint_prefix ../data/train/model.ckpt-44405 \
--output_directory ../data/train/
```

## optimize model
```
cd /pest-detection-project/pest-detection

python optimize_for_inference.py \
--input ../data/train/frozen_inference_graph.pb \
--output ../data/train/opt_graph.pb \
--input_names image_tensor \
--output_names "num_detections,detection_scores,detection_boxes,detection_classes" \
--placeholder_type_enum 4 \
--frozen_graph

python optimize_for_inference.py \
--input ../data/train/frozen_inference_graph.pb \
--output ../data/train/opt_graph.pb \
--input_names image_tensor \
--output_names "num_detections,detection_scores,detection_boxes,detection_classes" \

```

# 构建APP
## bazel方式
```
find . -name ".DS_Store" -delete

bazel build -c opt //tensorflow/examples/android:tensorflow_demo
```

```
adb kill-server
adb devices
adb install -r bazel-bin/tensorflow/examples/android/tensorflow_demo.apk
adb install -r /Users/liuziyi/tools/tensorflow/tensorflow/examples/android/gradleBuild/outputs/apk/debug/android-debug.apk
```

## android studio方式
### 修改app名称
在res/values/base_strings.xml文件中修改
