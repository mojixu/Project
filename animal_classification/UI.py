import streamlit as st
import torchvision.transforms as transforms
from PIL import Image, ImageDraw
from ultralytics import YOLO
import torch
import numpy as np
import cv2
from DOG_mapping import DOG_mapping, CUB_mapping

def load_model(model_choice, user_model_file=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = None  # 初始化模型变量

    if user_model_file is not None:
        try:
            if model_choice == "YOLOv8_nano":
                model = YOLO(user_model_file)  # 尝试加载用户上传的 YOLO 模型
                st.sidebar.success("成功加载自定义 YOLO 模型！")
            elif model_choice == "mobilenet":
                model = torch.load(user_model_file, map_location=device)
                model.eval()  # 切换到评估模式
                st.sidebar.success("成功加载自定义 MobileNet 模型！")
        except Exception as e:
            st.sidebar.error(f"加载自定义模型失败：{e}。请确保上传的文件兼容所选模型类型。")
    else:
        # 加载默认模型
        if animal_choice == "鸟类" and model_choice == "YOLOv8_nano":
            model = YOLO('trained_yolov8n_cub200_final.pt')
        elif animal_choice == "鸟类" and model_choice == "mobilenet":
            model = torch.load('mobilenet_v2_cub_final.pt', map_location=device)
            model.eval()  # 切换到评估模式
        elif animal_choice == "狗类" and model_choice == "YOLOv8_nano":
            model = YOLO('trained_yolov8n_DOG_middle.pt')
        elif animal_choice == "狗类" and model_choice == "mobilenet":
            model = torch.load('mobilenet_v2_dogs_final.pt', map_location=device)
            model.eval()  # 切换到评估模式

    if model is not None:
        model.to(device)
    return model, device


def predict(image, model, device, confidence_threshold, iou_threshold):
    if model is None:
        st.error("模型加载失败，请检查您的模型文件或选择其他模型。")
        return None, []

    results, pred_data = None, []

    if isinstance(model, YOLO):
        # YOLO 模型预测
        img = np.array(image)
        results = model(img, conf=confidence_threshold, iou=iou_threshold)
        for box in results[0].boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            confidence = box.conf.item()
            x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
            pred_data.append({
                "Class": class_name,
                "Confidence": confidence,
                "BBox": [x_min, y_min, x_max, y_max]
            })
    else:
        # MobileNet 模型预测
        mobilenet_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        img_tensor = mobilenet_transform(image).unsqueeze(0).to(device)  # 将图像张量移动到同一设备

        if animal_choice =="狗类":
            class_names = DOG_mapping()
            with torch.no_grad():
                outputs = model(img_tensor)
                _, predicted = outputs.max(1)
                class_id = predicted.item()
                class_name = class_names.get(class_id, f"类别 {class_id}")  # 从字典中获取类别名称
                confidence = torch.softmax(outputs, dim=1)[0, class_id].item() * 100  # 计算置信度
                pred_data.append({
                    "Class": class_name,
                    "Confidence": confidence
                })

        elif animal_choice =="鸟类":
            class_names = CUB_mapping()
            with torch.no_grad():
                outputs = model(img_tensor)
                _, predicted = outputs.max(1)
                class_id = predicted.item()
                class_name = class_names.get(class_id, f"类别 {class_id}")  # 从字典中获取类别名称
                confidence = torch.softmax(outputs, dim=1)[0, class_id].item() * 100  # 计算置信度
                pred_data.append({
                    "Class": class_name,
                    "Confidence": confidence
                })

    return results, pred_data



def draw_boxes(image, pred_data):
    draw = ImageDraw.Draw(image)
    for data in pred_data:
        x_min, y_min, x_max, y_max = data["BBox"]
        label = f"{data['Class']} ({data['Confidence']:.2f})"
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
        draw.text((x_min, y_min), label, fill="red")
    return image


st.title("基于轻量模型的动物细粒度识别检测系统")

st.sidebar.header("动物大类设置")
animal_choice = st.sidebar.selectbox("选择动物类型", ("鸟类", "狗类"))
st.sidebar.header("模型设置")
model_choice = st.sidebar.selectbox("选择模型类型", ("YOLOv8_nano", "mobilenet"))

# 用户上传自定义模型
st.sidebar.header("自定义模型")
user_model_file = st.sidebar.file_uploader("上传自定义 .pt 文件", type=["pt"])

confidence_threshold = st.sidebar.slider("置信度阈值", 0.0, 1.0, 0.25, 0.01)
iou_threshold = st.sidebar.slider("IOU阈值", 0.0, 1.0, 0.50, 0.01)

st.sidebar.header("摄像头配置")
camera_choice = st.sidebar.selectbox("选择摄像头", ("未启用摄像头", "启用摄像头1"))

st.sidebar.header("识别项目设置")
file_type = st.sidebar.selectbox("选择文件类型", ("图片文件",))

uploaded_file = st.sidebar.file_uploader("上传图片", type=["jpg", "jpeg", "png"])

st.subheader("显示模式")
display_mode = st.radio("选择显示模式", ("单画面显示", "双画面显示"), index=0)
target_choice = st.selectbox("目标选择", ("全部目标", "单个目标"))

# 根据选择的模型和用户上传的自定义模型文件加载模型
model, device = load_model(model_choice, user_model_file)
if camera_choice != "未启用摄像头":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    stframe1 = st.empty()  # Placeholder for the original frame
    stframe2 = st.empty()  # Placeholder for the boxed frame

    st.write("摄像头实时检测已启动，请对准识别目标")
    stop_button = st.button("停止摄像头", key="stop_camera")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("无法捕获帧，请检查摄像头连接。")
            break

        # Convert frame to PIL image for processing
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Prediction and bounding box generation
        results, pred_data = predict(image, model,device, confidence_threshold, iou_threshold)
        boxed_image = draw_boxes(image.copy(), pred_data)  # Image with bounding boxes

        # Check display mode
        if display_mode == "双画面显示":
            # Show original frame and bounded frame side-by-side
            stframe1.image(image, caption='原始画面', use_column_width=True)
            stframe2.image(boxed_image, caption='识别结果画面', use_column_width=True)
        else:
            # Only show the raw frame
            stframe1.image(image, caption='原始画面', use_column_width=True)

        # Display prediction results
        st.write("识别结果：")
        for i, data in enumerate(pred_data, 1):
            st.write(f"目标 {i}: 类别 - {data['Class']}, 置信度 - {data['Confidence']:.2f}")

        # Stop the loop if the stop button is pressed
        if stop_button:
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    if st.button("开始运行", key="start_run"):
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption='上传的图片', use_column_width=True)
            st.write("正在识别中，请稍候...")
            results, pred_data = predict(image, model, device,confidence_threshold, iou_threshold)
            if target_choice == "单目标识别" and pred_data:
                pred_data = [max(pred_data, key=lambda x: x["Confidence"])]
            st.write("识别完成！")
            if display_mode == "双画面显示":
                boxed_image = image.copy()
                boxed_image = draw_boxes(boxed_image, pred_data)
                st.image(boxed_image, caption='识别结果图像', use_column_width=True)
            st.write("Predicted Results:")
            for i, data in enumerate(pred_data, 1):
                st.write(f"Object {i}: Class - {data['Class']}, Confidence - {data['Confidence']:.2f}")
        else:
            st.warning("请上传图片进行识别！")
