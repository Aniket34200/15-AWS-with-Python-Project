import zipfile
import os

# 🔁 Put FULL paths here
files_to_zip = [
    r"E:\15 AWS with Python Projects\15. Automate CICD Pipelines using Lambda\pipeline\index.html",
    r"E:\15 AWS with Python Projects\15. Automate CICD Pipelines using Lambda\pipeline\buildspec.yml"
]

# Output zip file (you can also give full path here if you want)
zip_filename = r"E:\15 AWS with Python Projects\15. Automate CICD Pipelines using Lambda\source.zip"

def create_zip():
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            if os.path.exists(file_path):
                
                # This ensures only file name goes inside zip (clean structure)
                file_name = os.path.basename(file_path)
                
                zipf.write(file_path, arcname=file_name)
                print(f"✅ Added: {file_name}")

            else:
                print(f"❌ File not found: {file_path}")

    print(f"\n✅ Zip file created successfully: {zip_filename}")

if __name__ == "__main__":
    create_zip()