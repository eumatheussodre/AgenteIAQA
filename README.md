# 🧪 AgenteIA Engine – TGI

O **AgenteIA Engine – TGI** é uma ferramenta de automação de testes construída com Streamlit e Python. A aplicação utiliza Inteligência Artificial para gerar casos de teste a partir de documentos de requisitos, além de oferecer um conjunto de utilitários para Quality Assurance (QA), como geração de massa de dados e testes de API.

---

## ✨ Funcionalidades Principais

* **Geração de Casos de Teste por IA:** Faça upload de documentos de especificação e desenvolvimento para gerar casos de teste automaticamente.
* **Gerador de Massa de Dados:** Crie dados fictícios (nomes, CPFs, CNPJs, etc.) para os seus testes.
* **Gerador de Dados Bancários:** Gere dados bancários fictícios para cenários de teste financeiros.
* **Gerador para Testes de Carga:** Crie grandes volumes de dados em formato CSV ou JSON para testes de stress e performance.
* **Testador de API:** Envie requisições (GET, POST, PUT, DELETE) para qualquer endpoint de API diretamente da interface.
* **Exportação de Relatórios:** Exporte os resultados e os dados gerados em formatos como JSON, CSV e TXT.

---

## 📦 Tecnologias Utilizadas

* **Python 3.11+**
* **Streamlit:** Para a interface web interativa.
* **Pandas:** Para manipulação de dados.
* **OpenAI API:** (ou outro modelo de LLM) Para a geração de casos de teste.
* **WeasyPrint:** Para a exportação de relatórios em PDF.
* **Tesseract OCR:** Para a leitura de textos em imagens e PDFs escaneados.

---

## ⚙️ Configuração do Ambiente Local

Antes de executar o projeto, é crucial instalar as dependências de sistema que não são pacotes Python.

### Pré-requisitos de Sistema

1.  **Python 3.11 ou superior:** [Faça o download aqui](https://www.python.org/downloads/).
2.  **GTK3 (para WeasyPrint):** `WeasyPrint` precisa do GTK3 para gerar PDFs.
    * **Instruções:** Siga o guia que forneci anteriormente para [instalar o GTK3 no Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases) e adicioná-lo ao PATH do sistema.
3.  **Tesseract OCR (Opcional):** Necessário se for processar imagens.
    * **Instruções para Windows:** Faça o download e instale a partir [deste link](https://github.com/UB-Mannheim/tesseract/wiki). Durante a instalação, **certifique-se de adicionar o Tesseract ao PATH do sistema.**

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/agente-ia-qa.git](https://github.com/seu-usuario/agente-ia-qa.git)
    cd agente-ia-qa
    ```

2.  **(Recomendado) Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```

A aplicação estará disponível no seu navegador no endereço `http://localhost:8501`.

---

## 📁 Estrutura Sugerida do Projeto

Para que o `app.py` funcione corretamente, a estrutura do seu projeto deve ser semelhante a esta, com os módulos importados dentro de uma pasta `Funcionalidades`: