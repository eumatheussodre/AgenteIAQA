# AgenteIAQA Frontend

Interface web moderna em React para o seu agente de QA.

## Funcionalidades
- Gerar casos de teste com IA
- Gerar massa de dados
- Gerar massa bancária
- Exportar relatório

## Como rodar
1. Instale o Node.js (https://nodejs.org/)
2. No terminal, acesse a pasta `frontend`:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Acesse o endereço mostrado no terminal (geralmente http://localhost:5173)

## Requisitos
- A API FastAPI deve estar rodando em http://localhost:8000
- Endpoints necessários:
  - `/gerar-caso-ia/` (POST)
  - `/gerar-massa-dados/` (POST)
  - `/gerar-massa-bancaria/` (POST)
  - `/exportar-relatorio/` (POST)

## Estrutura
- `src/pages/` – Telas para cada funcionalidade
- `src/App.jsx` – Roteamento entre páginas

---

Sinta-se à vontade para customizar o layout, cores e adicionar novas funcionalidades!
