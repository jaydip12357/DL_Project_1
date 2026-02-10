"""
Naive Baseline Model Training Script for Pneumonia Detection.

This script implements a Most Frequent Class baseline predictor.

AI Attribution: Code generated with assistance from Claude AI (Anthropic)
via Cursor IDE on February 2026.
"""

import os
import json
from pathlib import Path
from collections import Counter
from sklearn.metrics import accuracy_score, classification_report

def train_naive_model():
    print("Training Naive Baseline Model (Chest X-Ray)...")
    
    # Updated paths for Chest X-Ray dataset
    train_dir = Path("chest_xray/train")
    test_dir = Path("chest_xray/test")
    
    if not train_dir.exists():
        print(f"Error: Data directory '{train_dir}' not found.")
        return

    # 1. Training: Find the most frequent class
    class_counts = Counter()
    classes = [d.name for d in train_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print(f"Found classes: {classes}")
    
    for class_name in classes:
        # Count jpeg files (Chest X-Ray dataset uses .jpeg)
        count = len(list((train_dir / class_name).glob("*.jpeg")))
        class_counts[class_name] = count
    
    if not class_counts:
         print("No data found in training set.")
         return

    most_frequent_class = class_counts.most_common(1)[0][0]
    print(f"Most frequent class (Baseline): {most_frequent_class}")
    print(f"Class distribution: {dict(class_counts)}")

    # 2. Evaluation
    y_true = []
    y_pred = []
    
    print("Evaluating on Test Set...")
    for class_name in classes:
        test_images = list((test_dir / class_name).glob("*.jpeg"))
        y_true.extend([class_name] * len(test_images))
        y_pred.extend([most_frequent_class] * len(test_images))
        
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\nNaive Baseline Accuracy: {accuracy:.4f}")
    
    # Save report
    report = classification_report(y_true, y_pred, zero_division=0, output_dict=True)
    
    os.makedirs("models", exist_ok=True)
    with open("models/naive_baseline_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print("Baseline report saved to models/naive_baseline_report.json")

if __name__ == "__main__":
    train_naive_model()
