import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(xml_root, output_root):
    os.makedirs(output_root, exist_ok=True)
    class_to_id = {}  # Dictionary to store class name to ID mapping
    current_id = 0    # Start assigning class IDs from 0

    # Iterate over each class folder in the XML root directory
    for class_folder in os.listdir(xml_root):
        class_path = os.path.join(xml_root, class_folder)
        if not os.path.isdir(class_path):
            continue

        # Create a corresponding folder in the output directory for YOLO annotations
        output_class_path = os.path.join(output_root, class_folder)
        os.makedirs(output_class_path, exist_ok=True)

        # Iterate over each file in the class folder (no extension filtering)
        for annotation_file in os.listdir(class_path):
            file_path = os.path.join(class_path, annotation_file)

            # Parse XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Get image dimensions
            size = root.find("size")
            width = int(size.find("width").text)
            height = int(size.find("height").text)

            # Create the corresponding YOLO format TXT file
            txt_path = os.path.join(output_class_path, annotation_file + ".txt")  # Adds .txt to original filename
            with open(txt_path, "w") as f:
                for obj in root.iter("object"):
                    cls = obj.find("name").text

                    # Assign a new ID if the class hasn't been encountered yet
                    if cls not in class_to_id:
                        class_to_id[cls] = current_id
                        current_id += 1

                    cls_id = class_to_id[cls]

                    # Get bounding box coordinates
                    xml_box = obj.find("bndbox")
                    xmin = int(xml_box.find("xmin").text)
                    ymin = int(xml_box.find("ymin").text)
                    xmax = int(xml_box.find("xmax").text)
                    ymax = int(xml_box.find("ymax").text)

                    # Convert to YOLO format
                    x_center = (xmin + xmax) / 2.0 / width
                    y_center = (ymin + ymax) / 2.0 / height
                    bbox_width = (xmax - xmin) / width
                    bbox_height = (ymax - ymin) / height

                    # Write the YOLO formatted data to the file
                    f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

    # Save the class-to-ID mapping for reference
    with open(os.path.join(output_root, "classes.txt"), "w") as f:
        for class_name, class_id in class_to_id.items():
            f.write(f"{class_id}: {class_name}\n")

    print("Conversion from XML to YOLO TXT format completed.")
    print("Class to ID mapping saved in classes.txt")

# Example usage
convert_xml_to_txt(
    xml_root=r"D:\The all of python\animal classification\Dogs_data\Stanford Dogs Dataset_annotations_datasets\Annotation",
    output_root=r"D:\The all of python\animal classification\Dogs_data\Stanford Dogs Dataset_annotations_datasets\YOLO_annotation_DOG"
)
