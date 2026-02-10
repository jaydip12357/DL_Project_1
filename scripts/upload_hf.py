from huggingface_hub import login, upload_folder
import os

def upload_to_hf():
    # Attempt to get token from env var first, otherwise ask for input
    token = os.getenv("HF_TOKEN")
    if not token:
        print("Please enter your Hugging Face Token (write permission required):")
        token = input().strip()
    
    try:
        login(token=token)
        print("Logged in successfully!")
        
        repo_id = "HanfuZhao781/540_Project_1"
        print(f"Uploading current directory to {repo_id}...")
        
        # Exclude hidden files, venv, and the large dataset folder itself
        # chest_xray is excluded via ignore_patterns if we want, but upload_folder respects .gitignore 
        # usually. Let's be explicit to avoid uploading huge data if not needed, 
        # OR if you WANT to upload the dataset, remove the exclusion.
        # Assuming you want to upload code + models (models/ folder has your trained .pth).
        
        upload_folder(
            folder_path=".", 
            repo_id=repo_id, 
            repo_type="model",
            ignore_patterns=["chest_xray/*", "venv/*", ".git/*", "__pycache__/*", "*.DS_Store"]
        )
        print("Upload complete!")
        
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    upload_to_hf()




