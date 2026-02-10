"""
Setup script for Pneumonia Detection project.

This script prepares the project environment:
- Creates necessary directories
- Downloads/prepares data (if needed)
- Runs initial data processing
- Optionally trains baseline models

Usage:
    python setup.py
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create project directory structure."""
    dirs = [
        'data/raw',
        'data/processed/train',
        'data/processed/val',
        'data/processed/test',
        'data/outputs',
        'models',
        'notebooks',
        'scripts',
        'uploads'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✓ Created directory structure")

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import flask
        import torch
        import sklearn
        import PIL
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_data():
    """Check if data exists."""
    data_dir = Path("chest_xray")
    if data_dir.exists():
        print(f"✓ Found dataset at {data_dir}")
        return True
    else:
        print(f"✗ Dataset not found at {data_dir}")
        print("Please download the Chest X-Ray dataset and place it in chest_xray/")
        return False

def main():
    print("=" * 60)
    print("Pneumonia Detection Project Setup")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check data
    data_exists = check_data()
    
    if data_exists:
        choice = input("\nData found. Do you want to run data preprocessing now? (y/n): ")
        if choice.lower() == 'y':
            print("\nRunning data preprocessing...")
            os.system("python scripts/make_dataset.py")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Train models: python main.py --mode train")
    print("  2. Run web app: python main.py --mode app")
    print("  3. Or run both: python main.py --mode all")

if __name__ == "__main__":
    main()

