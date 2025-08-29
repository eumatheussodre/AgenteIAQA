import express from "express";
import { LlamaModel, LlamaContext, LlamaChatSession } from "llama-node";

const app = express();
app.use(express.json());

// Configure o caminho do modelo GGUF baixado
const model = new LlamaModel({
    modelPath: "./models/llama-2-7b.Q4_K_M.gguf", // ajuste para o caminho do seu modelo
});

let loaded = false;

app.post("/llama", async (req, res) => {
    try {
        if (!loaded) {
            await model.load();
            loaded = true;
        }
        const { prompt } = req.body;
        const context = new LlamaContext({ model });
        const session = new LlamaChatSession({ context });
        const resposta = await session.prompt(prompt);
        res.json({ resposta });
    } catch (err) {
        res.status(500).json({ erro: err.message });
    }
});

const PORT = 8001;
app.listen(PORT, () => {
    console.log(`Llama API rodando em http://localhost:${PORT}`);
});
