import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
import time
import copy
import json
from pathlib import Path

def train_deep_model():
    print("Training Deep Learning Model (ResNet18) for Pneumonia Detection...")
    
    # Configuration
    data_dir = "chest_xray"
    num_epochs = 5  # Start with 5 epochs
    batch_size = 32
    input_size = 224
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Data Transforms
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize((input_size, input_size)), # X-Rays vary in size
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        # We also need a transform for 'test' since this dataset has a test folder
        'test': transforms.Compose([
            transforms.Resize((input_size, input_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Load Data
    # Note: Kaggle dataset structure is train/test/val
    # We will use 'val' for validation during training if it has enough data, 
    # but 'chest_xray/val' is very small (16 images). 
    # Usually people merge train and val or use 'test' as val. 
    # For simplicity, let's use 'test' as our validation set during training to see progress,
    # or strictly stick to the folders. Let's use 'test' for validation to monitor real performance.
    
    phases = ['train', 'test'] 
    
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x])
                      for x in phases}
    
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=batch_size, shuffle=(x=='train'), num_workers=2)
                   for x in phases}
    
    dataset_sizes = {x: len(image_datasets[x]) for x in phases}
    class_names = image_datasets['train'].classes
    
    print(f"Classes: {class_names}")
    print(f"Dataset sizes: {dataset_sizes}")

    # Initialize Model (ResNet18)
    model_ft = models.resnet18(weights='IMAGENET1K_V1')
    
    # Fine-tune the last layer
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, len(class_names))
    
    model_ft = model_ft.to(device)
    
    # Weighted Loss for Imbalanced Data (Pneumonia >> Normal)
    # Count samples
    class_counts = [len(list((Path(data_dir)/'train'/c).glob('*.jpeg'))) for c in class_names]
    # Simple inverse frequency weights
    weights = torch.tensor([1.0/c for c in class_counts]).to(device)
    weights = weights / weights.sum()
    print(f"Using class weights: {weights}")
    
    criterion = nn.CrossEntropyLoss(weight=weights)
    
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
    exp_lr_scheduler = optim.lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    # Training Loop
    since = time.time()
    best_model_wts = copy.deepcopy(model_ft.state_dict())
    best_acc = 0.0
    
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    for epoch in range(num_epochs):
        print(f'Epoch {epoch}/{num_epochs - 1}')
        print('-' * 10)

        for phase in ['train', 'test']: # Using 'test' as validation
            if phase == 'train':
                model_ft.train()
            else:
                model_ft.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer_ft.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model_ft(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer_ft.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            
            if phase == 'train':
                exp_lr_scheduler.step()

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
            
            # Map 'test' to 'val' in history for consistency
            hist_phase = 'val' if phase == 'test' else 'train'
            history[f'{hist_phase}_loss'].append(epoch_loss)
            history[f'{hist_phase}_acc'].append(epoch_acc.item())

            if phase == 'test' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model_ft.state_dict())

        print()

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    # Save Model
    model_ft.load_state_dict(best_model_wts)
    os.makedirs("models", exist_ok=True)
    torch.save(model_ft.state_dict(), "models/pneumonia_resnet18.pth")
    
    with open("models/training_history.json", "w") as f:
        json.dump(history, f)
        
    print("Model saved to models/pneumonia_resnet18.pth")

if __name__ == "__main__":
    train_deep_model()
