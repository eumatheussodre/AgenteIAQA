# generator_Report.py

import pandas as pd
from jinja2 import Template
from weasyprint import HTML
from pathlib import Path

# Template HTML movido para uma constante para maior clareza
HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Relatório de Casos de Teste</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; }
        h1 { color: #333; }
        .caso-teste { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
        .caso-teste h3 { margin-top: 0; color: #0056b3; }
        p { white-space: pre-wrap; /* Mantém as quebras de linha do texto original */ }
    </style>
</head>
<body>
    <h1>Relatório de Casos de Teste - Gerado por AgenteIA</h1>
    {% for i, caso in enumerate(casos, 1) %}
        <div class="caso-teste">
            <h3>Caso de Teste #{{ i }}</h3>
            <p>{{ caso }}</p>
        </div>
    {% endfor %}
</body>
</html>
""")


def exportar_relatorio(casos: list[str], nome_base_arquivo: str = "relatorio_de_testes"):
    """
    Exporta uma lista de casos de teste para os formatos .xlsx, .md e .pdf.

    Args:
        casos: Uma lista de strings, onde cada string é um caso de teste.
        nome_base_arquivo: O nome base para os ficheiros gerados (sem extensão).
    """
    caminho_base = Path(nome_base_arquivo)

    try:
        # 1. Exportar para Excel
        df = pd.DataFrame({"Casos de Teste": casos})
        caminho_excel = caminho_base.with_suffix(".xlsx")
        df.to_excel(caminho_excel, index=False, engine='openpyxl')
        print(f"✅ Relatório Excel salvo em: {caminho_excel}")

        # 2. Exportar para Markdown
        caminho_md = caminho_base.with_suffix(".md")
        with caminho_md.open("w", encoding="utf-8") as f:
            f.write("# Relatório de Casos de Teste\n\n")
            for i, caso in enumerate(casos, 1):
                f.write(
                    f"### Caso de Teste {i}\n\n```\n{caso}\n```\n\n---\n\n")
        print(f"✅ Relatório Markdown salvo em: {caminho_md}")

        # 3. Exportar para PDF usando um template HTML
        html_renderizado = HTML_TEMPLATE.render(
            casos=casos, enumerate=enumerate)
        caminho_pdf = caminho_base.with_suffix(".pdf")
        HTML(string=html_renderizado).write_pdf(caminho_pdf)
        print(f"✅ Relatório PDF salvo em: {caminho_pdf}")

    except (IOError, PermissionError) as e:
        print(f"❌ Erro ao escrever o ficheiro de relatório: {e}")
    except Exception as e:
        # Erro genérico para problemas inesperados (ex: com a biblioteca weasyprint)
        print(f"❌ Um erro inesperado ocorreu durante a exportação: {e}")
