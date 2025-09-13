import matplotlib.pyplot as plt
import re
from weasyprint import HTML
from jinja2 import Template

class GeneratorAgent:
    def __init__(self, language_model):
        self.language_model = language_model

    def generate_content(self, prompt):
        response = self.language_model.generate(prompt)
        return response

    def process_llm_response(self, llm_response):
        match = re.search(r"\[([0-9.,\s]+)\]", llm_response)
        data = []
        if match:
            data_str = match.group(0)
            import ast
            data = ast.literal_eval(data_str)
        text = llm_response.replace(data_str, "").strip() if match else llm_response
        return data, text

    def save_file(self, llm_response, file_type, file_path, user_prompt=None):
        data, text = self.process_llm_response(llm_response)
        imagen_generada = False
        if data:
            self._save_as_png(data, 'output.png', user_prompt)
            imagen_generada = True
        if file_type == 'pdf':
            image_path = 'output.png' if imagen_generada else None
            self._save_as_pdf_with_image(text, image_path, file_path, user_prompt)
        elif file_type == 'png' and imagen_generada:
            self._save_as_png(data, file_path, user_prompt)
        elif file_type == 'png':
            # Si no hay datos, no genera imagen
            pass
        else:
            raise ValueError("Unsupported file type. Use 'pdf' or 'png'.")

    def _save_as_pdf_with_image(self, text, image_path, file_path, user_prompt=None):
        html_template = """
        <html>
        <head>
            <style>
                @page { size: A4; margin: 32px; }
                body { font-family: 'Segoe UI', Arial, sans-serif; background: #f8f9fa; }
                .container { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #ccc; padding: 24px; }
                h1 { color: #2980b9; margin-bottom: 16px; font-size: 16pt; }
                .prompt { background: #eaf6fb; border-left: 4px solid #2980b9; padding: 12px; margin-bottom: 24px; font-style: italic; font-size: 10pt; }
                .texto { font-size: 10pt; margin-bottom: 30px; color: #333; }
                .grafico { text-align: center; margin-top: 30px; }
                .grafico img { max-width: 90%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px #bbb; }
                .footer { margin-top: 40px; font-size: 8pt; color: #888; text-align: right; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{{ titulo }}</h1>
                <div class="prompt"><strong>Prompt del usuario:</strong> {{ prompt }}</div>
                <div class="texto">{{ texto | safe }}</div>
                {% if imagen %}
                <div class="grafico">
                    <img src="{{ imagen }}"/>
                    <div style="font-size:8pt;color:#555;">Gráfico generado automáticamente</div>
                </div>
                {% endif %}
                <div class="footer">Generado por autogen-mcp-agent-app</div>
            </div>
        </body>
        </html>
        """
        from jinja2 import Template
        # Usa el prompt como título si no tienes un título específico
        titulo = user_prompt if user_prompt else "Informe generado"
        template = Template(html_template)
        html_content = template.render(
            texto=text,
            imagen=image_path if image_path else None,
            prompt=user_prompt or "",
            titulo=titulo
        )
        from weasyprint import HTML
        HTML(string=html_content, base_url='.').write_pdf(file_path)

    def _save_as_png(self, data, file_path, user_prompt=None):
        if data:
            plt.figure(figsize=(10, 5))
            # Usa el prompt como título del gráfico
            plt.title(user_prompt if user_prompt else "Gráfico generado", fontsize=16)
            plt.plot(data, marker='o', color='#2980b9')
            plt.xlabel("Índice", fontsize=12)
            plt.ylabel("Valor", fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(file_path, format='png')
            plt.close()
        else:
            plt.figure(figsize=(6, 4))
            plt.text(0.5, 0.5, "No hay datos para graficar", fontsize=14, ha='center', va='center')
            plt.axis('off')
            plt.savefig(file_path, format='png')
            plt.close()