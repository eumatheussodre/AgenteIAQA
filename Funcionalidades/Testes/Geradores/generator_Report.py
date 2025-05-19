import pandas as pd
from jinja2 import Template
from weasyprint import HTML

def exportar_relatorio(casos, caminho="relatorio.pdf"):
    df = pd.DataFrame({"Caso de Teste - Agente IA": casos})
    
    df.to_excel("relatorio.xlsx", index=False)
    
    with open("relatorio.md", "w", encoding="utf-8") as f:
        for i, caso in enumerate(casos, 1):
            f.write(f"### {i}. Caso de Teste\n{caso}\n\n")

    html_template = Template("""
    <html><body>
    <h1>Casos de Teste Gerados</h1>
    {% for i, caso in enumerate(casos, 1) %}
        <h3>{{ i }}. Caso de Teste</h3>
        <p>{{ caso.replace('\n', '<br>') }}</p>
    {% endfor %}
    </body></html>
    """)
    html = html_template.render(casos=casos, enumerate=enumerate)
    HTML(string=html).write_pdf(caminho)
