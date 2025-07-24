import io
from PIL import Image
import torch
import torchvision.models as models
import torch.nn as nn
from torchvision import transforms


_model = None  


def get_model(model_path: str, device: str = "cpu"):
    global _model
    if _model is None:
        _model = XRayClassifier(model_path, device)
    return _model


class XRayClassifier:
    def __init__(self, model_path: str, device: str = "cpu"):

        self.device = torch.device(device if torch.cuda.is_available() else "cpu")

        self.model = models.resnet50(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, 1)

        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])


    def predict(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(tensor)
            probability = torch.sigmoid(output).item()

        return "pneumonia" if probability > 0.5 else "normal"