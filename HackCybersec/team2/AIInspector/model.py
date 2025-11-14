import torch
import torch.nn as nn
import torchvision.transforms as T
from torchvision import models
from PIL import Image


class ArtifactDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.base = models.resnet18(weights=None)
        self.base.fc = nn.Linear(512, 1)

    def forward(self, x):
        return torch.sigmoid(self.base(x))


transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
])


def predict_image(model_path, image_path):
    model = ArtifactDetector()
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        pred = model(tensor).item()

    if pred > 0.5:
        return "⚠️ Возможные признаки вмешательства ИИ"
    else:
        return "✔️ Изображение выглядит естественным"