# 🧪 Agente Inteligente para Testes de Software

O **Agente Inteligente para Testes** é uma aplicação que utiliza Inteligência Artificial para gerar automaticamente **casos de teste** com base em documentos de requisitos (PDF, Excel, imagens). Além disso, permite o **envio direto para o Azure DevOps Boards**, agilizando o processo de testes e integração com o time de QA.

---

## 🚀 Funcionalidades

- 📄 **Extração de requisitos** de documentos (PDF, Excel, imagens escaneadas).
- 🤖 **Geração automática de casos de teste** com IA (GPT).
- ☁️ **Integração com Azure DevOps Boards** para criação de Test Cases.
- 📤 **Exportação de relatórios** em PDF, Markdown e Excel.
- 💬 **Interface Web interativa** com Streamlit.
- 🔌 **API REST** opcional para automação ou integração com outros sistemas.

---

## 📦 Tecnologias Utilizadas

- **Python 3.11+**
- [Streamlit](https://streamlit.io) – Interface Web
- [OpenAI API](https://platform.openai.com) – Geração de casos com IA
- **Tesseract OCR** – Leitura de textos em imagens
- **pdfplumber / openpyxl** – Processamento de arquivos PDF e Excel
- **WeasyPrint** – Exportação de relatórios em PDF
- **Azure DevOps Python SDK** – Integração com Azure Boards
- Docker (opcional)

---

## ⚙️ Como Executar Localmente

### Pré-requisitos

- Python 3.11 instalado
- Pip (gerenciador de pacotes)
- Tesseract OCR instalado e no PATH
- Conta e token de acesso (PAT) no Azure DevOps

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/agente-inteligente-testes.git
cd agente-inteligente-testes
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o aplicativo

```bash
streamlit run app.py
```

---

## 🐳 Executando com Docker

```bash
docker build -t agente-testes .
docker run -p 8501:8501 agente-testes
```

> Acesse: http://localhost:8501

---

## ☁️ Integração com Azure DevOps

Para enviar casos de teste diretamente ao Azure DevOps Boards:

1. Obtenha seu **Personal Access Token (PAT)** [aqui](https://dev.azure.com).
2. Preencha no formulário da aplicação:
   - URL da organização (ex: `https://dev.azure.com/sua_org`)
   - Nome do projeto
   - Seu token PAT

---

## 🧠 Exemplo de Uso

1. Faça upload de um documento com requisitos.
2. Clique em **"Gerar Casos de Teste"**.
3. Revise os casos gerados.
4. Clique em **"Enviar para Azure DevOps"** ou **"Exportar Relatório"**.

---

## 📁 Estrutura do Projeto

```
agente_inteligente_testes/
├── app.py
├── api.py
├── chatbot.py
├── automation_engine.py
├── file_processor.py
├── report_generator.py
├── test_generator.py
├── integrations/
│   ├── azure_client.py
│   ├── jira_client.py
│   └── github_client.py
├── requirements.txt
└── README.md
```

---

## ☁️ Hospedagem Gratuita com Docker + GitHub + Railway

Você pode hospedar este projeto gratuitamente usando:

- [Railway.app](https://railway.app)
- [Render](https://render.com)

### Exemplo com Railway

1. Crie uma conta em [railway.app](https://railway.app)
2. Clique em **"Deploy from GitHub repo"**
3. Conecte seu repositório com este projeto
4. Railway detectará automaticamente o `Dockerfile`
5. Configure variáveis de ambiente (como `OPENAI_API_KEY`, `AZURE_PAT_TOKEN`, etc.)
6. Acesse a URL pública gerada

---

## 📛 Badges (opcional)

```md
![Build](https://img.shields.io/github/actions/workflow/status/seu-usuario/agente-inteligente-testes/deploy.yml)
![License](https://img.shields.io/github/license/seu-usuario/agente-inteligente-testes)
```

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
