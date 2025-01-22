import os

# Paths
CUB_ROOT = "./CUB_200_2011"
CLASSES_FILE = os.path.join(CUB_ROOT, 'classes.txt')
YOLO_ROOT = "./YOLO_dataset_CUB"
YAML_FILE = os.path.join(YOLO_ROOT, 'data_CUB.yaml')

# Read class names from classes.txt
class_names = []
with open(CLASSES_FILE, 'r') as f:
    for line in f:
        class_id, class_name = line.strip().split(' ', 1)
        class_names.append(class_name)

# Create YAML content
yaml_content = f"""
# data_CUB.yaml
train: {os.path.join(YOLO_ROOT, 'images/train')}
val: {os.path.join(YOLO_ROOT, 'images/val')}

nc: {len(class_names)}  # Number of classes
names: {class_names}
"""

# Write the content to the YAML file
with open(YAML_FILE, 'w') as yaml_file:
    yaml_file.write(yaml_content)

print(f"'data_CUB.yaml' has been created at: {YAML_FILE}")
