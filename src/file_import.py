import os

def import_file(uploaded_file):
   
    # Create save directory if not exists
    save_dir = "uploaded_resumes"
    os.makedirs(save_dir, exist_ok=True)

    # Extract file name
    filename = uploaded_file.name
    print(filename)

    # Only accept PDFs
    if not filename.lower().endswith('.pdf'):
        print("File is not a PDF")
        return None

    # Save uploaded file locally
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    print(f"✅ File saved as {file_path}")
    return file_path
