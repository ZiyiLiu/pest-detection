## 项目概述
本项目基于计算机视觉技术，针对农田环境下的各类害虫目标进行实时检测（即定位、识别和计数）。项目开发流程中，具体依赖于[TensorFlow机器学习框架](https://github.com/tensorflow/tensorflow)来构建卷积神经网络模型，模型可方便移植到Android等移动端平台或云端。

## 数据情况
本部分对项目中的建模所涉及的数据情况进行综述。

### 害虫类别
本项目中所涉及害虫检测种类为69种，涵盖常见稻田、茶园和果园害虫种类。具体类别可以参见本项目data文件下的label_map.pbtxt文件。


### 数据格式
由于项目是基于Tensorflow机器学习框架进行开发，因此在构建模型时需要将图像数据由原始的JPEG格式转换为TF Record格式，进而进行模型的训练、验证和应用操作。具体的数据格式转换代码为

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
其中，
- images：存放原始图像数据的文件夹
- xml：存放数据标注文件的文件夹
- set：该参数可以为train, valid或test，分别针对模型的训练、验证和测试过程
- labels_map_path：该文件指定了各类别的名称以及对应的类别id
- output_path：即为输出的新的数据格式的路径

## 检测模型
项目意欲采用两种类型的模型架构，分别在云端和移动端（以离线的方式运行）进行应用，故也采用了两套不同的模型，此处以移动端的模型为例进行说明。移动端采用的模型为SSD-MobileNet模型。具体的模型定义位于文件中，该文件中具体指定了模型的架构，模型的训练参数，以及模型训练过程中所采用的数据路径等等。


### 模型架构 
- 移动端：SSD-MobileNet，该模型相对架构简单，但是能够在对设备的性能要求和检测精度上达到一定的平衡；
- 云端：Faster-RCNN，该模型架构较为复杂，主要关注在检测精度上取得更好的效果；


### 模型训练
以移动端的SSD-MobileNet为例，模型训练的代码如下：
```
# From /pest-detection-project/pest-detection
python object_detection/train.py \
--logtostderr \
--train_dir=../data/train \
--pipeline_config_path=../data/ssd_mobilenet_v1_coco_2017_11_17/ssd_mobilenet_v1_coco.config
```
其中，
- train_dir：训练结果的输出文件夹
- pipeline_config_path：指定模型架构、训练参数和数据路径的文件的路径

保存后的train_dir中将包含6个文件，其名称和作用分别为
- checkpoint
- graph.pbtxt
- model.ckpt-***.data-00000-of-00001
- model.ckpt-***.index
- model.ckpt-***.meta

### 模型应用
为了能够在应用中调用模型，需要将模型保存（freeze）为单个文件，调用如下命令：
```
# From /pest-detection-project/pest-detection
python export_inference_graph.py \
--input_type image_tensor \
--pipeline_config_path ../data/train/pipeline.config \
--trained_checkpoint_prefix ../data/train/model.ckpt-44405 \
--output_directory ../data/train/
```
其中，
- input_type：模型输入模块的名称
- trained_checkpoint_prefix：训练过程中模型保存名称的前缀
- output_directory：输出的单个文件的输出目录

为了能够在应用中缩小模型的尺寸（尤其是在移动端），需要对模型中的部分无用参数进行裁剪，具体命令如下：
```
# From /pest-detection-project/pest-detection
python optimize_for_inference.py \
--input ../data/train/frozen_inference_graph.pb \
--output ../data/train/opt_graph.pb \
--input_names image_tensor \
--output_names "num_detections,detection_scores,detection_boxes,detection_classes" \
--placeholder_type_enum 4 \
--frozen_graph
```
其中，
- input：模型保存后的单个文件
- output：裁剪后的模型的保存路径
- output_names：由模型获得的输出数据，包括定位到的害虫数量num_detections，对每一个害虫目标的判断置信度detection_scores，对每一个害虫目标的定位位置detection_boxes以及其所对应的类别

## APP构建
本部分以Android平台上的构建过程为例进行说明，在获得模型文件后，可以采用两种方式来构建Android APP，下面分别对这两种方式进行说明。在此之前，需安装一些基本依赖：

### 预先准备
克隆Tensorflow的github仓库，将本项目仓库中的Android文件夹存放至上述克隆目录的/tensorflow/example中，替换掉其原有的android文件夹。具体命令如下：
```
git clone https://github.com/tensorflow/tensorflow.git
```

安装Android SDK和NDK工具，其中，NDK的推荐版本为12b以上（本项目中所用到版本为14b），SDK的版本为23。于此同时，在上述克隆的Tensorflow文件夹的根目录中找到WORKSPACE文件，修改其中<PATH_TO_NDK>和<PATH_TO_SDK>为本地路径。

### 构建方式1：Bazel构建
安装[Bazel](https://bazel.build)构建工具和[ADB](https://developer.android.com/studio/command-line/adb.html)工具用于安装Android APK文件。

1. Bazel构建Android项目，具体命令如下：
```
bazel build -c opt //tensorflow/examples/android:tensorflow_demo
```

2. 安装所构建的APK文件（请注意已经在此之前用ADB连接好设备），具体命令如下：
```
adb install -r bazel-bin/tensorflow/examples/android/tensorflow_demo.apk
```

### 构建方式2：Android Studui构建
1. 打开Android Studio，选择Open an existing Android Studio project，由tensorflow/examples/android导入项目（如果要求Gradle Sync, 点击OK即可）。

2. 打开Open the build.gradle文件，查找到nativeBuildSystem
变量，并按如下设置：
```
// set to 'bazel', 'cmake', 'makefile', 'none'
def nativeBuildSystem = 'none'
```

3. 点击Run，即可安装APP。
