"""
Classical Machine Learning Model Training Script (HOG + SVM).

This script extracts HOG features from X-Ray images and trains an SVM classifier.

AI Attribution: Code generated with assistance from Claude AI (Anthropic)
via Cursor IDE on February 2026.
"""

import os
import joblib
import numpy as np
from pathlib import Path
from tqdm import tqdm
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from PIL import Image

def load_data(data_dir, target_size=(128, 128), max_samples=None):
    X = []
    y = []
    
    classes = sorted([d.name for d in data_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    for class_name in classes:
        class_dir = data_dir / class_name
        images = list(class_dir.glob("*.jpeg"))
        
        # Subsample if requested (to speed up SVM training)
        if max_samples and len(images) > max_samples:
            import random
            random.shuffle(images)
            images = images[:max_samples]
            
        for img_path in tqdm(images, desc=f"Loading {class_name}"):
            try:
                # Use PIL to handle grayscale conversion consistently
                with Image.open(img_path) as img:
                    img = img.convert('L') # Convert to grayscale
                    img_resized = img.resize(target_size)
                    img_array = np.array(img_resized)
                
                # Extract HOG features
                features = hog(img_array, orientations=9, pixels_per_cell=(8, 8),
                               cells_per_block=(2, 2), visualize=False)
                
                X.append(features)
                y.append(class_name)
            except Exception as e:
                print(f"Error reading {img_path}: {e}")
                
    return np.array(X), np.array(y), classes

def train_classical_model():
    print("Training Classical ML Model (HOG + SVM) for Pneumonia Detection...")
    
    train_dir = Path("chest_xray/train")
    test_dir = Path("chest_xray/test")
    
    if not train_dir.exists():
        print("Error: Data directory not found.")
        return

    # Load data (Limit training samples for SVM speed if needed, e.g., 1000 per class)
    print("Extracting features from training set...")
    # SVM scales poorly with n_samples > 10k. Here we have ~5k, which is okay but might be slow.
    X_train, y_train, classes = load_data(train_dir, max_samples=1000) 
    
    print("Extracting features from test set...")
    X_test, y_test, _ = load_data(test_dir)
    
    # Encode labels
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc = le.transform(y_test)
    
    # Train SVM
    print(f"Training SVM Classifier on {len(X_train)} samples...")
    clf = SVC(kernel='rbf', C=1.0, verbose=True) # RBF kernel usually better for images than linear
    clf.fit(X_train, y_train_enc)
    
    # Evaluate
    print("Evaluating...")
    y_pred_enc = clf.predict(X_test)
    accuracy = accuracy_score(y_test_enc, y_pred_enc)
    print(f"\nClassical Model Accuracy: {accuracy:.4f}")
    
    y_pred = le.inverse_transform(y_pred_enc)
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/svm_model.pkl")
    joblib.dump(le, "models/label_encoder.pkl")
    print("Model saved to models/svm_model.pkl")

if __name__ == "__main__":
    train_classical_model()
