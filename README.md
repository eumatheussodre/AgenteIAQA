# 🧪 Agente IA - [QA] - Prototipo - i4Pro v.0.0.3

O **Agente IA - [QA] - Prototipo - i4Pro** é uma aplicação que utiliza Inteligência Artificial para gerar automaticamente **casos de teste** com base em documentos de requisitos (PDF, Excel, imagens). 



---
## 📝 Histórico de Versões

### 📌 **v0.0.1 – [16/05/2025]**
- 📄 **Extração de requisitos de documentos** (PDF, Excel, imagens escaneadas).
- 🤖 **Geração automática de casos de teste** com IA (GPT).
- 📤 **Exportação de relatórios** em PDF, Markdown e Excel.
- 💬 **Interface Web interativa** com Streamlit.


### 📌 **v0.0.2 – [16/05/2025]**
🔹 **Melhoria na geração de massa de dados para QA**  
🔹 **Correção do `enumerate` no Jinja2 para relatórios**  
🔹 **Adição do suporte a exportação de relatórios HTML** 
🔹 **Adição de Menus Laterais**  
🔹 **Criação do módulo `bank_generator.py`** para separar massa de dados bancários  
🔹 **Correção do erro `ModuleNotFoundError: No module named 'faker'` no Docker**  
🔹 **Exportação de massa bancária para CSV**


### 📌 **v0.0.3 – [16/05/2025]**
🔹 **Melhorando a Geração de Casos de Testes**
      - Foi adicionado opções de **Upload do Documento do Desenvolvedor e da Especificação de Funcionalidade**
      ![Descrição do GIF](https://link-do-gif.gif)


🔹 **Foi Melhorando a Geração Fake de Dados Bancarios**
      - A geração agora, permiti no minimo a **Geração de 5 Massas de Dados**
      ![Descrição do GIF](https://link-do-gif.gif)


### 📌 **v0.0.5 – [18/05/2025]**
🔹 **Adição do Test Stress**
      - Agora é possivel gerar Massa de Dados, para realziar Tests de Stress
      ![Descrição do GIF](https://link-do-gif.gif)


🔹 **Adição de Test API**
      - Agora é possivel realizar Testes de API, via Agente IA. 
      ![Descrição do GIF](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJyeXV0MzcxeWJvZm5tOTVoaGNyazM4Mmh6Z3duOTV0em1xMzdsNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/44okQTpfZAlr2ilEgg/giphy.gif)


---

## 📦 Tecnologias Utilizadas

- **Python 3.11+**
- [Streamlit](https://streamlit.io) – Interface Web
- [OpenAI API](https://platform.openai.com) – Geração de casos com IA
- **Tesseract OCR** – Leitura de textos em imagens
- **pdfplumber / openpyxl** – Processamento de arquivos PDF e Excel
- **WeasyPrint** – Exportação de relatórios em PDF
- Docker (opcional)
- Faker

---

## ⚙️ Como Executar Localmente

### Pré-requisitos

- Python 3.11 instalado
- Pip (gerenciador de pacotes)

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

## 📁 Estrutura do Projeto

```
agente_inteligente_testes/
├── app.py
├── bank_generator.py
├── data_generator
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

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
