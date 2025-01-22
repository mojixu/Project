import os


def create_yaml_from_classes(classes_file, output_yaml, dataset_path):
    # Read the classes from classes.txt to maintain consistent order
    class_names = []
    with open(classes_file, "r") as f:
        for line in f:
            class_id, class_name = line.strip().split(": ")
            class_names.append(class_name)

    # Write to .yaml file
    with open(output_yaml, "w") as f:
        f.write(f"path: {dataset_path}\n")
        f.write("train: images_DOG/train\n")
        f.write("val: images_DOG/val\n")
        f.write("\n")
        f.write("names:\n")

        for i, class_name in enumerate(class_names):
            f.write(f"  {i}: {class_name}\n")

    print(f"YAML file '{output_yaml}' created successfully with classes in the correct order.")


# Example usage
create_yaml_from_classes(
    classes_file=r"D:\The all of python\animal classification\Dogs_data\Stanford Dogs Dataset_annotations_datasets\YOLO_annotation_DOG\classes.txt",
    output_yaml=r"D:\The all of python\animal classification\YOLO_dataset_DOG\data_DOG.yaml",
    dataset_path=r"D:\The all of python\animal classification\YOLO_dataset"  # Root directory where images and labels are located
)
