import express from "express";
import cors from "cors";
import multer from "multer";
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const pdfParse = require('pdf-parse');
import mammoth from "mammoth";
import ExcelJS from "exceljs";
import fs from "fs";
import { gerarMassaDados, gerarMassaBancaria } from "./modules/geradores.js";
// Temporariamente comentado até resolver problema com llama-node
// import { createRequire } from 'module';
// const require = createRequire(import.meta.url);
// const { LlamaModel, LlamaContext, LlamaChatSession } = require('llama-node');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configuração do multer para upload de arquivos
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, './uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname)
    }
});

const upload = multer({ storage: storage });

// Criar pasta uploads se não existir
import path from 'path';
const uploadsDir = './uploads';
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Função para processar conteúdo do arquivo
async function processarArquivo(filePath, mimeType) {
    try {
        if (mimeType === 'application/pdf') {
            const dataBuffer = fs.readFileSync(filePath);
            const data = await pdfParse(dataBuffer);
            return data.text;
        } else if (mimeType.includes('document') || filePath.endsWith('.doc') || filePath.endsWith('.docx')) {
            const result = await mammoth.extractRawText({ path: filePath });
            return result.value;
        }
        return '';
    } catch (error) {
        console.error('Erro ao processar arquivo:', error);
        return '';
    }
}

app.get("/", (req, res) => {
    res.json({ mensagem: "API do AgenteIAQA (Node.js) está ativa!" });
});

app.post("/api/massa-dados", (req, res) => {
    console.log("Iniciando geração de massa de dados...");
    const { quantidade, campos } = req.body;
    console.log(`Quantidade: ${quantidade}, Campos: ${campos}`);

    const startTime = Date.now();
    const massa = gerarMassaDados(Number(quantidade), campos);
    const endTime = Date.now();

    console.log(`Geração concluída em ${endTime - startTime}ms`);
    res.json({ massa });
});

app.post("/api/massa-bancaria", (req, res) => {
    const { quantidade, permitir_negativo } = req.body;
    const massa = gerarMassaBancaria(Number(quantidade), permitir_negativo);
    res.json({ massa_bancaria: massa });
});

// Temporariamente comentado até resolver problema com llama-node
// const llamaModel = LlamaModel({
//     modelPath: "./models/llama-2-7b.Q4_K_M.gguf"
// });
// let llamaLoaded = false;

app.post("/api/llama", async (req, res) => {
    res.status(503).json({ erro: "Serviço Llama temporariamente indisponível" });
    // try {
    //     if (!llamaLoaded) {
    //         await llamaModel.load();
    //         llamaLoaded = true;
    //     }
    //     const { prompt } = req.body;
    //     const context = new LlamaContext({ model: llamaModel });
    //     const session = new LlamaChatSession({ context });
    //     const resposta = await session.prompt(prompt);
    //     res.json({ resposta });
    // } catch (err) {
    //     res.status(500).json({ erro: err.message });
    // }
});

// Novo endpoint para gerar casos de teste com IA
app.post("/api/gerar-caso-ia", upload.single('arquivo'), async (req, res) => {
    try {
        let textoBase = req.body.requisito || '';

        // Se há arquivo, processar o conteúdo
        if (req.file) {
            const conteudoArquivo = await processarArquivo(req.file.path, req.file.mimetype);
            textoBase = conteudoArquivo + (textoBase ? '\n\n' + textoBase : '');

            // Remover arquivo após processamento
            fs.unlinkSync(req.file.path);
        }

        if (!textoBase.trim()) {
            return res.status(400).json({ erro: "Nenhum conteúdo fornecido" });
        }

        // Por enquanto, retornar uma resposta simulada até implementar a IA
        const casoGerado = `📝 SOLICITAÇÃO DO CLIENTE:
${textoBase.substring(0, 200)}...

🔧 SOLUÇÃO ADOTADA PELO DEV:
[Aguardando implementação da integração com IA para análise automática]

CT-001

🔹CENÁRIO DE TESTE:
Validação do comportamento antes da correção

🔸CASO DE TESTE:
Replicar o erro reportado no ambiente

⏳ PRÉ-REQUISITO:
Sistema configurado no estado anterior à correção

📋 FLUXO DE TESTE:
1. Acessar a funcionalidade
2. Executar ação que gera o erro
3. Verificar comportamento inesperado

✅ RESULTADO ESPERADO:
Erro deve ser reproduzido conforme reportado

⚠️ PONTOS DE ATENÇÃO:
Documentar evidências do erro

CT-002

🔹CENÁRIO DE TESTE:
Validação do comportamento após a correção

🔸CASO DE TESTE:
Confirmar que a correção resolve o problema

⏳ PRÉ-REQUISITO:
Sistema atualizado com a correção implementada

📋 FLUXO DE TESTE:
1. Acessar a funcionalidade
2. Executar a mesma ação do CT-001
3. Verificar comportamento correto

✅ RESULTADO ESPERADO:
Funcionalidade deve operar sem erros

⚠️ PONTOS DE ATENÇÃO:
Validar não regressão em outras funcionalidades`;

        res.json({ caso: casoGerado });

    } catch (error) {
        console.error('Erro ao processar requisição:', error);
        res.status(500).json({ erro: "Erro interno do servidor" });
    }
});

// Endpoint para exportar casos de teste para Excel
app.post("/api/exportar-casos-excel", async (req, res) => {
    try {
        const { casos } = req.body;

        if (!casos) {
            return res.status(400).json({ erro: "Nenhum caso de teste fornecido" });
        }

        // Criar workbook do Excel
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('Casos de Teste');

        // Configurar cabeçalhos
        worksheet.columns = [
            { header: 'Seção', key: 'secao', width: 25 },
            { header: 'Conteúdo', key: 'conteudo', width: 80 }
        ];

        // Processar o texto dos casos para extrair seções
        const linhas = casos.split('\n');
        let linhaAtual = '';

        for (const linha of linhas) {
            if (linha.trim()) {
                // Detectar seções com emojis
                if (linha.includes('📝 SOLICITAÇÃO DO CLIENTE:') ||
                    linha.includes('🔧 SOLUÇÃO ADOTADA PELO DEV:') ||
                    linha.includes('🔹CENÁRIO DE TESTE:') ||
                    linha.includes('🔸CASO DE TESTE:') ||
                    linha.includes('⏳ PRÉ-REQUISITO:') ||
                    linha.includes('📋 FLUXO DE TESTE:') ||
                    linha.includes('✅ RESULTADO ESPERADO:') ||
                    linha.includes('⚠️ PONTOS DE ATENÇÃO:') ||
                    linha.startsWith('CT-')) {

                    if (linhaAtual) {
                        worksheet.addRow({ secao: '', conteudo: linhaAtual });
                        linhaAtual = '';
                    }

                    const secao = linha.split(':')[0].trim();
                    const conteudo = linha.includes(':') ? linha.split(':').slice(1).join(':').trim() : linha;

                    worksheet.addRow({ secao, conteudo });
                } else {
                    linhaAtual += linha + '\n';
                }
            } else if (linhaAtual) {
                worksheet.addRow({ secao: '', conteudo: linhaAtual.trim() });
                linhaAtual = '';
            }
        }

        // Adicionar última linha se houver
        if (linhaAtual) {
            worksheet.addRow({ secao: '', conteudo: linhaAtual.trim() });
        }

        // Estilizar o cabeçalho
        worksheet.getRow(1).eachCell((cell) => {
            cell.font = { bold: true };
            cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4472C4' } };
            cell.font.color = { argb: 'FFFFFFFF' };
        });

        // Configurar quebra de linha automática
        worksheet.eachRow((row) => {
            row.eachCell((cell) => {
                cell.alignment = { vertical: 'top', wrapText: true };
            });
        });

        // Gerar buffer do Excel
        const buffer = await workbook.xlsx.writeBuffer();

        // Configurar headers para download
        res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader('Content-Disposition', `attachment; filename="casos_de_teste_${new Date().toISOString().split('T')[0]}.xlsx"`);

        res.send(buffer);

    } catch (error) {
        console.error('Erro ao gerar Excel:', error);
        res.status(500).json({ erro: "Erro ao gerar arquivo Excel" });
    }
});

// Endpoints para IA e exportação podem ser adicionados aqui

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
