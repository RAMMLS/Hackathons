import torch
from PIL import Image
import torchvision.transforms as T
from model import ArtifactDetector

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor()
])

model = ArtifactDetector()
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

def predict(img_path):
    img = Image.open(img_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        pred = model(tensor).item()

    if pred > 0.5:
        return "✔ Изображение выглядит естественным"
    else:
        return "⚠ Обнаружены признаки вмешательства ИИ"

print(predict("трал.jpg"))