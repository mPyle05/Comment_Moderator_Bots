import pandas as pd
from transformers import RobertaTokenizer
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaModel
import torch.nn as nn
from torch.optim import AdamW
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Load your dataset
data = pd.read_csv('labeled_data_small.csv')

# Extract the text and weights
texts = data['text'].tolist()
labels = data[['hate_speech', 'offensive_language', 'neither']].values  # Multi-label targets

# Preview the data
print(data[['text', 'hate_speech', 'offensive_language', 'neither']].head())

# Load the RoBERTa tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize the text column
def tokenize_data(texts, max_length=128):
    return tokenizer(texts, padding='max_length', truncation=True, max_length=max_length, return_tensors="pt")

# Apply tokenization
input_encodings = tokenize_data(texts)
input_ids = input_encodings['input_ids']
attention_mask = input_encodings['attention_mask']

class WeightedTextDataset(Dataset):
    def __init__(self, input_ids, attention_mask, labels):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.labels = torch.tensor(labels, dtype=torch.float)  # Convert labels to float for regression

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }

# Convert labels to a tensor
dataset = WeightedTextDataset(input_ids, attention_mask, labels)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

class RobertaForWeightedMultiLabel(nn.Module):
    def __init__(self):
        super(RobertaForWeightedMultiLabel, self).__init__()
        self.roberta = RobertaModel.from_pretrained('roberta-base')
        self.regressor = nn.Linear(self.roberta.config.hidden_size, 3)  # Three output values

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        return self.regressor(pooled_output)

# Instantiate the model
model = RobertaForWeightedMultiLabel()

# Check for GPU and move model to GPU if available
device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Use Mean Squared Error loss for regression
loss_fn = nn.MSELoss()
optimizer = AdamW(model.parameters(), lr=2e-5)

# Training loop
model.train()
for epoch in range(3):  # Adjust the number of epochs as needed
    total_loss = 0
    for batch in data_loader:
        optimizer.zero_grad()

        # Move the batch data to the selected device (GPU or CPU)
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        # Compute loss
        loss = loss_fn(outputs, labels)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(data_loader)
    print(f"Epoch {epoch + 1} completed with average loss: {avg_loss}")

# Save model and tokenizer
model.save_pretrained('hate_speech_roberta_weighted_multilabel')
tokenizer.save_pretrained('hate_speech_roberta_weighted_multilabel')
