import os
import shutil
import random
from PIL import Image
from pathlib import Path
from tqdm import tqdm

def process_data():
    # Configuration
    # NOTE: Assuming user will put raw data back into data/raw or we need to ask them to restore it.
    # Since I cannot restore deleted files that were not backed up by me, I will assume 
    # the user will re-upload or I need to process what is available.
    # For now, I will write the script assuming data/raw is populated.
    
    raw_data_dir = Path("data/raw")
    processed_data_dir = Path("data/processed")
    target_size = (224, 224)
    split_ratios = {"train": 0.7, "val": 0.15, "test": 0.15}
    
    if not raw_data_dir.exists():
        print(f"Error: {raw_data_dir} does not exist. Please place your 'ayakkabi', 'canta', 'giyim' folders there.")
        return

    # Ensure processed directory exists
    if processed_data_dir.exists():
        shutil.rmtree(processed_data_dir)
    processed_data_dir.mkdir(parents=True)

    # Create split directories
    for split in split_ratios.keys():
        (processed_data_dir / split).mkdir()

    # Get all categories
    categories = [d for d in raw_data_dir.iterdir() if d.is_dir()]
    
    for category_dir in categories:
        classes = [d for d in category_dir.iterdir() if d.is_dir()]
        
        for class_dir in tqdm(classes, desc=f"Processing {category_dir.name}"):
            class_name = class_dir.name
            
            # Create class directories
            for split in split_ratios.keys():
                (processed_data_dir / split / class_name).mkdir(exist_ok=True)

            images = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                images.extend(list(class_dir.glob(ext)))
            
            random.shuffle(images)
            
            n_total = len(images)
            n_train = int(n_total * split_ratios["train"])
            n_val = int(n_total * split_ratios["val"])
            
            splits = {
                "train": images[:n_train],
                "val": images[n_train:n_train + n_val],
                "test": images[n_train + n_val:]
            }

            for split_name, split_images in splits.items():
                for img_path in split_images:
                    try:
                        with Image.open(img_path) as img:
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                            dest_path = processed_data_dir / split_name / class_name / img_path.name
                            img_resized.save(dest_path, quality=90)
                    except Exception as e:
                        print(f"Error processing {img_path}: {e}")

    print("\nData processing complete!")

if __name__ == "__main__":
    random.seed(42)
    process_data()
