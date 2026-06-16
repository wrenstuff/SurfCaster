import os
import joblib

import pandas as pd
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Creating a dataframe from the pandas library
# and importing the test dataset for initial training
df = pd.read_csv('data.csv')

# drops rows with missing values
df.dropna(inplace=True)

# displays first 5 entries of df
print(df.head())
# displays all columns of df
print(df.info())

#define target column
target_column = 'status'
url_column = 'url'

df_train = df.copy()

# converts legitemate and phishing to 0 and 1
df_train[target_column] = df_train[target_column].map({
    'legitimate': 0,
    'phishing': 1
})

#drops the target column from df
x = df_train.drop(columns=[target_column, url_column])
# makes a new dataframe for target column
y = df_train[target_column]

# turns catagorical variables into dummy variabes (True/False) to (1/0)
# cumputers don't like words
# if you have a column which has SO MANY UNIQUE VALUES,
# please make sure you drop if first.
# I just spent hours on this because of the stupid "url" column
# it was making the model extremely big when it wasn't supposed to be...
# thanks for coming to my ted talk
x = pd.get_dummies(x, drop_first=True)

feature_columns = list(x.columns)

input_size = x.shape[1]
print(f"Input size: {input_size}")

# setting up the train/split for the model
X_train, X_test, y_train, y_test = train_test_split(
    x, 
    y, 
    test_size=0.2, 
    random_state=42,
    stratify=y
)

# standardise the data for easier training
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# convert to tensors for pytorch
X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1).to(device)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1).to(device)

# define the model
class Baelin(nn.Module):
    def __init__(self, input_size):
        super(Baelin, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.network(x)

model = Baelin(input_size).to(device)

#loss and optimizer
loss_function = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# training loop
# more epochs = better training but possible overfitting
# less epochs = faster training but possible underfitting
# gotta figure out the sweet spot
epochs = 500

for epoch in range(epochs):
    model.train()

    optimizer.zero_grad()
    
    logits = model(X_train_tensor)
    loss = loss_function(logits, y_train_tensor)

    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')

# model evaluation
model.eval()

threshold = .50

with torch.no_grad():
    test_logits = model(X_test_tensor)
    test_probabilities = torch.sigmoid(test_logits)
    # probability that it accepts the url as legitemate or phishing
    test_predictions = (test_probabilities >= threshold).float()

y_pred = test_predictions.cpu().numpy()
y_true = y_test_tensor.cpu().numpy()

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
matrix = confusion_matrix(y_true, y_pred)

print()
print("Evaluation:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

print()
print(f"Confusion Matrix:\n{matrix}")

#checkpoint
os.makedirs('SurfCaster/models', exist_ok=True)
save_path = 'SurfCaster/models/Baelin_checkpoint.pth'
scaler_path = 'SurfCaster/models/Baelin_scaler.pkl'

checkpoint = {
    "model_state_dict": model.state_dict(),
    "input_size": input_size,
    "feature_columns": feature_columns,
    "threshold": threshold,
    "epochs": epochs,
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1
}

torch.save(checkpoint, save_path)
joblib.dump(scaler, scaler_path)

