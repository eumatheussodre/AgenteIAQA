# 🧪 AgenteIA Engine – TGI

O **AgenteIA Engine – TGI** é uma aplicação que utiliza Inteligência Artificial para gerar automaticamente **casos de teste** com base em documentos de requisitos (PDF, Excel, imagens). 



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
🔹 **Melhorando a Geração de Casos de Testes** <br>
      - Foi adicionado opções de **Upload do Documento do Desenvolvedor e da Especificação de Funcionalidade**


🔹 **Foi Melhorando a Geração Fake de Dados Bancarios** <br>
      - A geração agora, permiti no minimo a **Geração de 5 Massas de Dados**  


### 📌 **v0.0.5 – [18/05/2025]**
🔹 **Adição do Test Stress** <br>
      - Agora é possivel gerar Massa de Dados, para realziar Tests de Stress

🔹 **Adição de Test API** <br>
      - Agora é possivel realizar Testes de API, via Agente IA. 
      ![API](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWJyeXV0MzcxeWJvZm5tOTVoaGNyazM4Mmh6Z3duOTV0em1xMzdsNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/44okQTpfZAlr2ilEgg/giphy.gif)

### 📌 **v0.0.7 – [18/05/2025]**
🔹 **Melhoria na Geração de Dados** <br>
      - Agora é possivel selecionar os dados, que você deseja gerar para seu testes.
      ![GeracaoDeDadosv2](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmZlaXc0Y2p2cnl6ajQxd25jamQ5eGpuNjF1b3F6YnBnZWM0a2NqcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3hoCVPt9QQyE7TG9tB/giphy.gif)

### 📌 **v0.0.8 – [22/05/2025]**
🔹 **Melhoria no Menu Lateral** <br>
      - Menu Lateral, anteriormente, estava gerando confusão e certos Bugs. Então, resolvi realizar a unificação dos Menus.
      ![MenuLateral]()


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
- Entr

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
