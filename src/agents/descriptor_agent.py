from PIL import Image

class DescriptorAgent:
    def __init__(self, file_path):
        self.file_path = file_path

    def describe_file(self):
        if self.file_path.endswith('.png'):
            with Image.open(self.file_path) as img:
                return f"Imagen PNG de tamaño {img.size}, modo {img.mode}."
        elif self.file_path.endswith('.pdf'):
            from PyPDF2 import PdfReader
            reader = PdfReader(self.file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return f"PDF con {len(reader.pages)} páginas. Texto extraído: {text[:200]}..."
        else:
            return f"Archivo generado: {self.file_path}"