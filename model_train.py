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
df = pd.read_csv('dataset_phishing.csv')

# drops rows with missing values
df.dropna(inplace=True)

# displays first 5 entries of df
print(df.head())
# displays all columns of df
print(df.info())

#define target column
target_column = 'status'

drop_columns = ['nb_hyperlinks', 'ratio_intHyperlinks', 'ratio_extHyperlinks', 'ratio_nullHyperlinks', 'nb_extCSS', 'ratio_intRedirection', 'ratio_extRedirection', 'ratio_intErrors', 'ratio_extErrors', 'login_form', 'external_favicon', 'links_in_tags', 'submit_email', 'ratio_intMedia', 'ratio_extMedia', 'sfh', 'iframe', 'popup_window', 'safe_anchor', 'onmouseover', 'right_clic', 'empty_title', 'domain_in_title', 'domain_with_copyright', 'whois_registered_domain', 'domain_registration_length', 'domain_age', 'web_traffic', 'dns_record', 'google_index', 'page_rank']

df_train = df.copy() #df.drop(columns=['url'])

# drops specified columns
df_train = df_train.drop(columns=drop_columns)

# converts legitemate and phishing to 0 and 1
df_train[target_column] = df_train[target_column].map({
    'legitimate': 0,
    'phishing': 1
})

#drops the target column from df
x = df_train.drop(columns=[target_column])
# makes a new dataframe for target column
y = df_train[target_column]

# turns catagorical variables into dummy variabes (True/False) to (1/0)
# cumputers don't like words
X = pd.get_dummies(x, drop_first=True)

# setting up the train/split for the model
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.30, 
    random_state=42
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
class PhishingDetector(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.linear = nn.Linear(input_size, 1)
    
    def forward(self, x):
        return self.linear(x)

input_size = X_train_tensor.shape[1]
model = PhishingDetector(input_size).to(device)

#loss and optimizer
loss_function = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# training loop
# more epochs = better training but possible overfitting
# less epochs = faster training but possible underfitting
# gotta figure out the sweet spot
epochs = 1000

for epoch in range(epochs):
    model.train()

    logits = model(X_train_tensor.to(device))
    loss = loss_function(logits, y_train_tensor)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')

# model evaluation
model.eval()

with torch.no_grad():
    test_logits = model(X_test_tensor.to(device))
    test_probabilities = torch.sigmoid(test_logits)
    test_predictions = (test_probabilities >= 0.5).float()

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

#save model
torch.save(model.state_dict(), 'Baelin.pth')
print("Model saved as 'Baelin.pth'")