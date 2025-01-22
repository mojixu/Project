import os
import shutil
from PIL import Image

# Paths to the dataset files
CUB_ROOT = "./CUB_200_2011"
IMAGES_FILE = os.path.join(CUB_ROOT, 'images.txt')
TRAIN_TEST_SPLIT_FILE = os.path.join(CUB_ROOT, 'train_test_split.txt')
BOUNDING_BOXES_FILE = os.path.join(CUB_ROOT, 'bounding_boxes.txt')
IMAGE_CLASS_LABELS_FILE = os.path.join(CUB_ROOT, 'image_class_labels.txt')
IMAGES_DIR = os.path.join(CUB_ROOT, 'images')

# Output directories for YOLO format
YOLO_ROOT = "./YOLO_dataset_CUB"
os.makedirs(f"{YOLO_ROOT}/images/train", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/images/val", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/labels/train", exist_ok=True)
os.makedirs(f"{YOLO_ROOT}/labels/val", exist_ok=True)


# Helper function to convert bounding boxes to YOLO format
def convert_bbox_to_yolo(x, y, width, height, img_width, img_height):
    x_center = (x + width / 2) / img_width
    y_center = (y + height / 2) / img_height
    width /= img_width
    height /= img_height
    return x_center, y_center, width, height


# Read files
with open(IMAGES_FILE, 'r') as f:
    img_id_to_name = {line.split()[0]: line.split()[1] for line in f}

with open(TRAIN_TEST_SPLIT_FILE, 'r') as f:
    img_id_to_split = {line.split()[0]: line.split()[1] for line in f}

with open(BOUNDING_BOXES_FILE, 'r') as f:
    img_id_to_bbox = {line.split()[0]: list(map(float, line.split()[1:])) for line in f}

with open(IMAGE_CLASS_LABELS_FILE, 'r') as f:
    img_id_to_class = {line.split()[0]: str(int(line.split()[1]) - 1) for line in f}  # YOLO classes start at 0

# Process images and bounding boxes
for img_id, img_name in img_id_to_name.items():
    img_split = img_id_to_split[img_id]
    img_class = img_id_to_class[img_id]
    bbox = img_id_to_bbox[img_id]

    # Load image to get dimensions
    img_path = os.path.join(IMAGES_DIR, img_name)
    img = Image.open(img_path)
    img_width, img_height = img.size

    # Convert bounding box to YOLO format
    x_center, y_center, bbox_width, bbox_height = convert_bbox_to_yolo(
        *bbox, img_width, img_height
    )

    # Create annotation line
    yolo_annotation = f"{img_class} {x_center} {y_center} {bbox_width} {bbox_height}\n"

    # Determine if it's a train or validation image
    if img_split == '1':  # Train image
        split = 'train'
    else:  # Validation image
        split = 'val'

    # Save image
    save_img_path = os.path.join(YOLO_ROOT, 'images', split, os.path.basename(img_name))
    shutil.copy(img_path, save_img_path)

    # Save annotation
    label_file_path = os.path.join(YOLO_ROOT, 'labels', split, os.path.splitext(os.path.basename(img_name))[0] + '.txt')
    with open(label_file_path, 'w') as label_file:
        label_file.write(yolo_annotation)
