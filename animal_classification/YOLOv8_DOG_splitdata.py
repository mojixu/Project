

import os
import shutil
import random

def split_dataset(images_root, annotations_root, output_dir, train_ratio=0.8):
    # Define train and val directories
    train_images_dir = r'D:\The all of python\animal classification\YOLO_dataset_DOG\images\train'
    val_images_dir = r'D:\The all of python\animal classification\YOLO_dataset_dog\images\val'
    train_labels_dir = r'D:\The all of python\animal classification\YOLO_dataset_dog\labels\train'
    val_labels_dir = r'D:\The all of python\animal classification\YOLO_dataset_dog\labels\val'

    # Create directories if they don’t exist
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)

    # Iterate over each class folder
    for class_folder in os.listdir(images_root):
        class_images_path = os.path.join(images_root, class_folder)
        class_annotations_path = os.path.join(annotations_root, class_folder)

        # Only process directories (skip files)
        if not os.path.isdir(class_images_path):
            continue

        # List all images in the class folder
        images = [f for f in os.listdir(class_images_path) if f.endswith(".jpg")]
        random.shuffle(images)
        split_index = int(len(images) * train_ratio)

        train_images = images[:split_index]
        val_images = images[split_index:]

        # Move train files
        for img in train_images:
            img_path = os.path.join(class_images_path, img)
            label_path = os.path.join(class_annotations_path, img.replace(".jpg", ".txt"))

            shutil.copy(img_path, train_images_dir)
            shutil.copy(label_path, train_labels_dir)

        # Move val files
        for img in val_images:
            img_path = os.path.join(class_images_path, img)
            label_path = os.path.join(class_annotations_path, img.replace(".jpg", ".txt"))

            shutil.copy(img_path, val_images_dir)
            shutil.copy(label_path, val_labels_dir)

    print("Dataset split completed.")

# Example usage
split_dataset(
    images_root=r'D:\The all of python\animal classification\Dogs_data\Stanford Dogs Dataset_images_datasets\Images',
    annotations_root=r'D:\The all of python\animal classification\Dogs_data\Stanford Dogs Dataset_annotations_datasets\YOLO_annotation_DOG',
    output_dir="Dogs_data\output",
    train_ratio=0.8
)
