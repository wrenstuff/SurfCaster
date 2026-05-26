import torch
import torch.nn as nn

state_dict_path = 'SurfCaster/models/Baelin.pth'

state_dict = torch.load(state_dict_path)
for key, value in state_dict.items():
    print(f"{key}: {value.shape}")

class Baelin(nn.Module):
    def __init__(self):
        super(Baelin, self).__init__()
        self.linear = nn.Linear(50, 1)

    def forward(self, x):
        return self.linear(x)
    
model = Baelin()

model.load_state_dict(torch.load(state_dict_path))
model.eval()

input_data = torch.randn(1, 50)
with torch.no_grad():
    logits = model(input_data)
    probability = torch.sigmoid(logits).item()