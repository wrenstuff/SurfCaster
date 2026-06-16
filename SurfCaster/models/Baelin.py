import torch
import torch.nn as nn
import joblib
import pandas as pd

state_dict_path = 'SurfCaster/models/Baelin_checkpoint.pth'
scaler_path = 'SurfCaster/models/Baelin_scaler.pkl'


class Baelin(nn.Module):
    def __init__(self, input_size):
        super(Baelin, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size,64),
            nn.ReLU(),
            nn.Linear(64,32),
            nn.ReLU(),
            nn.Linear(32,1)
        )

    def forward(self, x):
        return self.network(x)
    
    def predict(self, features, scaler=None, feature_columns=None, threshold=0.5):

        if isinstance(features, dict):
            features = pd.DataFrame([features])

        if isinstance(features, torch.Tensor):
            if features.dim() == 2:
                features = features.detach().cpu().numpy()
            else:
                features = features.detach().cpu().numpy().reshape(1, -1)

        if isinstance(features, pd.DataFrame):
            features = pd.DataFrame(features, columns=feature_columns)
 

        if scaler is not None:
            features = scaler.transform(features)
            
        features = torch.tensor(features, dtype=torch.float32)

        self.eval()

        with torch.no_grad():
            logits = self(features)
            phishing_probability = torch.sigmoid(logits).item()

        if phishing_probability >= threshold:
            result = "phishing"
            confidence = phishing_probability
        else:
            result = "legitimate"
            confidence = 1 - phishing_probability

        return {
            "result": result,
            "phishing_probability": phishing_probability,
            "confidence": confidence
        }
    
checkpoint = torch.load(state_dict_path, map_location="cpu")
scaler = joblib.load(scaler_path)

input_size = checkpoint["input_size"]
feature_columns = checkpoint["feature_columns"]
threshold = checkpoint["threshold"]

model = Baelin(input_size)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()

input_data = torch.randn(1, input_size)

with torch.no_grad():
    logits = model(input_data)
    probability = torch.sigmoid(logits).item()