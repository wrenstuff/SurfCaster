import torch
import torch.nn as nn

state_dict_path = 'SurfCaster/models/Baelin.pth'

state_dict = torch.load(state_dict_path)
for key, value in state_dict.items():
    print(f"{key}: {value.shape}")

class Baelin(nn.Module):
    def __init__(self):
        super(Baelin, self).__init__()
        self.linear = nn.Linear(11515, 1)

    def forward(self, x):
        x = torch.relu(self.linear(x))
        return x
    
model = Baelin()

model.load_state_dict(torch.load('SurfCaster/models/Baelin.pth'))
model.eval()

input_data = torch.randn(1, 11515)
with torch.no_grad():
    prediction = model(input_data)
    print(prediction)