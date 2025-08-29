import express from "express";
import cors from "cors";
import { gerarMassaDados, gerarMassaBancaria } from "./modules/geradores.js";

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    res.json({ mensagem: "API do AgenteIAQA (Node.js) está ativa!" });
});

app.post("/gerar-massa-dados", (req, res) => {
    const { quantidade, campos } = req.body;
    const massa = gerarMassaDados(Number(quantidade), campos);
    res.json({ massa });
});

app.post("/gerar-massa-bancaria", (req, res) => {
    const { quantidade, permitir_negativo } = req.body;
    const massa = gerarMassaBancaria(Number(quantidade), permitir_negativo);
    res.json({ massa_bancaria: massa });
});

// Endpoints para IA e exportação podem ser adicionados aqui

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
