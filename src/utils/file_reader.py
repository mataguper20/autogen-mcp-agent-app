def read_pdf(file_path):
    from PyPDF2 import PdfReader

    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def read_png(file_path):
    from PIL import Image
    import pytesseract

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

def get_file_metadata(file_path):
    import os

    metadata = {
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "file_type": os.path.splitext(file_path)[1],
    }
    return metadata