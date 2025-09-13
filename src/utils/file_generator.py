def create_png(content, filename):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))
    plt.text(0.5, 0.5, content, fontsize=12, ha='center', va='center')
    plt.axis('off')
    plt.savefig(filename, format='png')
    plt.close()

def create_pdf(content, filename):
    from weasyprint import HTML

    html_content = f"<html><body><h1>{content}</h1></body></html>"
    HTML(string=html_content).write_pdf(filename)

def generate_file(content, file_type, filename):
    if file_type == 'png':
        create_png(content, filename)
    elif file_type == 'pdf':
        create_pdf(content, filename)
    else:
        raise ValueError("Unsupported file type. Please use 'png' or 'pdf'.")