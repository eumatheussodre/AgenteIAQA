import express from "express";
import cors from "cors";
import { gerarMassaDados, gerarMassaBancaria } from "./modules/geradores.js";
import pkg from "llama-node";
const { LlamaModel, LlamaContext, LlamaChatSession } = pkg;

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    res.json({ mensagem: "API do AgenteIAQA (Node.js) está ativa!" });
});

app.post("/api/massa-dados", (req, res) => {
    const { quantidade, campos } = req.body;
    const massa = gerarMassaDados(Number(quantidade), campos);
    res.json({ massa });
});

app.post("/api/massa-bancaria", (req, res) => {
    const { quantidade, permitir_negativo } = req.body;
    const massa = gerarMassaBancaria(Number(quantidade), permitir_negativo);
    res.json({ massa_bancaria: massa });
});

const llamaModel = LlamaModel({
    modelPath: "./models/llama-2-7b.Q4_K_M.gguf"
});
let llamaLoaded = false;

app.post("/api/llama", async (req, res) => {
    try {
        if (!llamaLoaded) {
            await llamaModel.load();
            llamaLoaded = true;
        }
        const { prompt } = req.body;
        const context = new LlamaContext({ model: llamaModel });
        const session = new LlamaChatSession({ context });
        const resposta = await session.prompt(prompt);
        res.json({ resposta });
    } catch (err) {
        res.status(500).json({ erro: err.message });
    }
});

// Endpoints para IA e exportação podem ser adicionados aqui

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
