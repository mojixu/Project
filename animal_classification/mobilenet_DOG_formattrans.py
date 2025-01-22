import os
import shutil

# 定义路径
base_dir = r'D:\The all of python\animal classification\YOLO_dataset_DOG'
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')
output_dir = r'D:\The all of python\animal classification\Mobile_ImageFolder_dataset_DOG'

# 创建输出目录结构
for split in ['train', 'val']:
    split_dir = os.path.join(output_dir, split)
    os.makedirs(split_dir, exist_ok=True)

    labels_split_dir = os.path.join(labels_dir, split)
    images_split_dir = os.path.join(images_dir, split)

    for label_file in os.listdir(labels_split_dir):
        if label_file.endswith('.txt'):
            # 读取标签文件，提取类别
            with open(os.path.join(labels_split_dir, label_file), 'r') as f:
                lines = f.readlines()
                class_label = lines[0].split()[0]  # 取第一行的第一个值为类别标签

            # 获取图像文件路径
            image_name = label_file.replace('.txt', '.jpg')  # 假设图像格式为.jpg
            image_path = os.path.join(images_split_dir, image_name)

            # 创建类别文件夹
            class_dir = os.path.join(split_dir, class_label)
            os.makedirs(class_dir, exist_ok=True)

            # 复制图像到对应类别文件夹
            shutil.copy(image_path, class_dir)
