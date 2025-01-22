import torch
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets
from torch import nn, optim

# 图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 使用ImageNet的均值和方差
])

# 加载训练集和验证集
data_dir = r'D:\The all of python\animal classification\Mobile_ImageFolder_dataset_CUB'
train_data = datasets.ImageFolder(root=f'{data_dir}/train', transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)

val_data = datasets.ImageFolder(root=f'{data_dir}/val', transform=transform)
val_loader = torch.utils.data.DataLoader(val_data, batch_size=32, shuffle=False)

# 加载预训练的MobileNetV2模型
model = torchvision.models.mobilenet_v2(weights=True)

# 替换分类层，设置输出单元为您数据集的类别数
num_classes = len(train_data.classes)
model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)

# # 加载已有的.pth文件
# model.load_state_dict(torch.load('mobilenet_v2_dogs_middle.pth'))

# 使用GPU（如果可用）
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# 设置损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
epochs = 100
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    if epoch == 50:
        # 保存模型
        torch.save(model, f'mobilenet_v2_cub_{epoch}.pt')
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        # 前向传播
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch [{epoch + 1}/{epochs}], Loss: {running_loss / len(train_loader):.4f}")

    # 验证模型
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f"Validation Accuracy: {100 * correct / total:.2f}%")

# 保存模型
torch.save( model, 'mobilenet_v2_cub_final.pt')
