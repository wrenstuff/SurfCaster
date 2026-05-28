import torch
import torch.nn as nn

state_dict_path = 'SurfCaster/models/Baelin.pth'

state_dict = torch.load(state_dict_path)
for key, value in state_dict.items():
    print(f"{key}: {value.shape}")

class Baelin(nn.Module):
    def __init__(self):
        super(Baelin, self).__init__()
        self.linear = nn.Linear(49, 1)

    def forward(self, x):
        return self.linear(x)
    
    def predict(self, features):

        if not isinstance(features, torch.Tensor):
            features = torch.tensor(features, dtype=torch.float32)

        if features.dim() == 1:
            features = features.unsqueeze(0)

        with torch.no_grad():
            logits = self(features)
            return torch.sigmoid(logits).item()
    
model = Baelin()

model.load_state_dict(torch.load(state_dict_path))
model.eval()

input_data = torch.randn(1, 49)

