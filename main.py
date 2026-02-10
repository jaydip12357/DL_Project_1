"""
Main entry point for the Pneumonia Detection project.

This script provides a unified interface to run various components of the project:
- Data processing
- Model training (Naive, Classical, Deep Learning)
- Web application

Usage:
    python main.py --mode [process|train|app]
"""

import argparse
import sys
import os

def run_data_processing():
    """Run data preprocessing pipeline."""
    print("Running data preprocessing...")
    from scripts.make_dataset import process_data
    process_data()
    print("Data processing complete!")

def run_training(model_type='all'):
    """Run model training."""
    if model_type in ['naive', 'all']:
        print("\n=== Training Naive Baseline ===")
        os.system("python scripts/train_naive.py")
    
    if model_type in ['classical', 'all']:
        print("\n=== Training Classical ML Model ===")
        os.system("python scripts/train_classical.py")
    
    if model_type in ['deep', 'all']:
        print("\n=== Training Deep Learning Model ===")
        os.system("python scripts/train_deep.py")

def run_web_app():
    """Launch the web application."""
    print("Starting web application...")
    print("Open http://localhost:5000 in your browser")
    from app.main import app
    app.run(debug=True, port=5000)

def main():
    parser = argparse.ArgumentParser(description='Pneumonia Detection Project')
    parser.add_argument('--mode', 
                        choices=['process', 'train', 'app', 'all'],
                        default='app',
                        help='Mode to run: process data, train models, run app, or all')
    parser.add_argument('--model',
                        choices=['naive', 'classical', 'deep', 'all'],
                        default='all',
                        help='Which model to train (only used with --mode train)')
    
    args = parser.parse_args()
    
    if args.mode == 'process':
        run_data_processing()
    elif args.mode == 'train':
        run_training(args.model)
    elif args.mode == 'app':
        run_web_app()
    elif args.mode == 'all':
        print("Running full pipeline...")
        run_data_processing()
        run_training('all')
        print("\nSetup complete! Run 'python main.py --mode app' to start the web application.")

if __name__ == "__main__":
    main()

