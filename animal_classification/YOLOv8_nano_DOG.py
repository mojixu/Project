from ultralytics import YOLO
import os
# Disable multi-threading
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
# Load the YOLOv8 Nano model pre-trained weights
model = YOLO('trained_yolov8n_DOG_middle.pt')  # Loads YOLOv8 Nano model

# Train the model on your custom dataset
model.train(data=r'D:\The all of python\animal classification\YOLO_dataset_DOG\data_DOG.yaml',  # Path to the data_CUB.yaml file
            epochs=50,                      # Number of training epochs
            imgsz=640,                       # Input image size
            batch=16,
            workers=0,# Batch size
            name='yolov8n_DOG')           # Name for this training session

# Save the trained model as a .pt file
model.save('trained_yolov8n_DOG_middle.pt')

print("Training complete! The model has been saved as 'trained_yolov8n_DOG_middle.pt'.")
