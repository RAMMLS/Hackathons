import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import os

# ===============================
# 1. Трансформации для обучения
# ===============================
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(5),
    transforms.ColorJitter(brightness=0.3, contrast=0.3),
    transforms.ToTensor(),
])

# ===============================
# 2. Датасет
# ===============================
dataset = datasets.ImageFolder("data", transform=train_transform)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

print(f"Найдено изображений: {len(dataset)}")
print(f"Классы: {dataset.classes}")

# ===============================
# 3. Модель ResNet18
# ===============================
class ArtifactDetector(nn.Module):
    def __init__(self):
        super().__init__()
        # Создаем модель без предобученных весов
        self.base = models.resnet18(weights=None)
        self.base.fc = nn.Linear(512, 1)

    def forward(self, x):
        return torch.sigmoid(self.base(x))

model = ArtifactDetector()

# ===============================
# 4. Загрузка весов из model.pth
# ===============================
model_path = "model.pth"
if os.path.exists(model_path):
    print(f"Загружаем веса из {model_path}")
    try:
        # Загружаем state_dict
        state_dict = torch.load(model_path, map_location="cpu")
        
        # Проверяем, является ли загружаемый state_dict полным или только весами модели
        if "base.fc.weight" in state_dict or "base.fc.bias" in state_dict:
            # Это state_dict нашей модели ArtifactDetector
            model.load_state_dict(state_dict)
            print("✓ Веса успешно загружены")
        else:
            # Это state_dict стандартного ResNet18, нужно адаптировать
            print("Обнаружены веса стандартного ResNet18, адаптируем...")
            # Удаляем последний слой (classifier) из загружаемых весов
            state_dict.pop('fc.weight', None)
            state_dict.pop('fc.bias', None)
            # Загружаем только backbone
            model.base.load_state_dict(state_dict, strict=False)
            print("✓ Backbone ResNet18 загружен, последний слой инициализирован случайно")
            
    except Exception as e:
        print(f"Ошибка при загрузке весов: {e}")
        print("Продолжаем со случайной инициализацией")
else:
    print(f"Файл {model_path} не найден. Начинаем обучение со случайной инициализацией.")

# ===============================
# 5. Функция потерь и оптимизатор
# ===============================
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# ===============================
# 6. Обучение
# ===============================
EPOCHS = 10
print("\nНачинаем обучение...\n")

for epoch in range(EPOCHS):
    total_loss = 0
    correct = 0
    total = 0

    for images, labels in dataloader:
        labels = labels.float().unsqueeze(1)

        optimizer.zero_grad()
        outputs = model(images)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        
        # Вычисляем точность
        predicted = (outputs > 0.5).float()
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    accuracy = 100 * correct / total
    print(f"Эпоха {epoch+1}/{EPOCHS} — Loss: {total_loss:.4f}, Accuracy: {accuracy:.2f}%")

# ===============================
# 7. Сохранение
# ===============================
torch.save(model.state_dict(), "model.pth")
print("\n✔ Модель сохранена как model.pth")
