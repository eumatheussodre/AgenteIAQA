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


app.post("/api/llama", async (req, res) => {
    res.status(503).json({ erro: "Serviço Llama temporariamente indisponível" });
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
${textoBase.substring(0, 200).replace(/\n/g, ' ')}...

🔧 SOLUÇÃO ADOTADA PELO DEV:
Implementação de correção técnica baseada na análise do requisito fornecido, incluindo validações e ajustes necessários no sistema.

CT-001

🔹CENÁRIO DE TESTE:
Validação do comportamento antes da correção - Reprodução do erro

🔸CASO DE TESTE:
Replicar o erro reportado no ambiente anterior à implementação da solução

⏳ PRÉ-REQUISITO:
Sistema configurado no estado anterior à correção, ambiente de testes preparado

📋 FLUXO DE TESTE:
1. Acessar a funcionalidade específica do sistema
2. Executar a ação que gera o comportamento inadequado
3. Verificar se o erro é reproduzido conforme reportado

✅ RESULTADO ESPERADO:
Erro deve ser reproduzido conforme reportado pelo cliente, confirmando a existência do problema

⚠️ PONTOS DE ATENÇÃO:
Documentar evidências do erro, capturar screenshots, validar mensagens de erro exibidas

CT-002

🔹CENÁRIO DE TESTE:
Validação do comportamento após a correção - Confirmação da solução

🔸CASO DE TESTE:
Confirmar que a correção implementada resolve o problema reportado

⏳ PRÉ-REQUISITO:
Sistema atualizado com a correção implementada, ambiente configurado com a nova versão

📋 FLUXO DE TESTE:
1. Acessar a mesma funcionalidade testada no CT-001
2. Executar a mesma sequência de ações do cenário anterior
3. Verificar se o comportamento está correto após a correção

✅ RESULTADO ESPERADO:
Funcionalidade deve operar corretamente sem apresentar o erro anterior

⚠️ PONTOS DE ATENÇÃO:
Validar que não houve regressão em outras funcionalidades, confirmar mensagens de sucesso`;

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
        const worksheet = workbook.addWorksheet('Plano de Testes');

        // Configurar largura das colunas
        worksheet.columns = [
            { key: 'cenario', width: 20 },
            { key: 'id', width: 8 },
            { key: 'caso', width: 25 },
            { key: 'prerequisito', width: 20 },
            { key: 'fluxo', width: 35 },
            { key: 'resultado', width: 25 },
            { key: 'pontos', width: 20 },
            { key: 'integracao', width: 15 },
            { key: 'aceite', width: 15 }
        ];

        // Cabeçalho principal - PLANO DE TESTE I4PRO
        worksheet.mergeCells('B1:I1');
        const headerCell = worksheet.getCell('B1');
        headerCell.value = 'PLANO DE TESTE I4PRO';
        headerCell.font = { bold: true, size: 20, color: { argb: 'FF00B4A6' } };
        headerCell.alignment = { horizontal: 'center', vertical: 'middle' };
        headerCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF0F0F0' } };

        // Logo I4PRO (célula A1)
        const logoCell = worksheet.getCell('A1');
        logoCell.value = 'i4pro';
        logoCell.font = { bold: true, size: 14, color: { argb: 'FFFF6B35' } };
        logoCell.alignment = { horizontal: 'center', vertical: 'middle' };
        logoCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4ECDC4' } };

        // Informações do cabeçalho
        const infoRows = [
            ['Cliente', ''],
            ['Solicitante', ''],
            ['Autor', ''],
            ['Data Criacao', ''],
            ['WEX/Solicitacao', ''],
            ['Ambiente', ''],
            ['Classificacao', ''],
            ['Solicitação da Cliente', ''],
            ['Solução Adotada', '']
        ];

        let currentRow = 2;
        for (const [label, value] of infoRows) {
            const labelCell = worksheet.getCell(`A${currentRow}`);
            labelCell.value = label;
            labelCell.font = { bold: true };
            labelCell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4ECDC4' } };

            worksheet.mergeCells(`B${currentRow}:I${currentRow}`);
            const valueCell = worksheet.getCell(`B${currentRow}`);
            valueCell.value = value;

            currentRow++;
        }

        // Extrair informações dos casos
        const linhas = casos.split('\n');
        let solicitacaoCliente = '';
        let solucaoAdotada = '';

        for (const linha of linhas) {
            if (linha.includes('📝 SOLICITAÇÃO DO CLIENTE:')) {
                solicitacaoCliente = linha.split(':').slice(1).join(':').trim();
            } else if (linha.includes('🔧 SOLUÇÃO ADOTADA PELO DEV:')) {
                solucaoAdotada = linha.split(':').slice(1).join(':').trim();
            }
        }

        // Preencher informações extraídas
        worksheet.getCell('B8').value = solicitacaoCliente;
        worksheet.getCell('B9').value = solucaoAdotada;

        // Cabeçalho "EXECUÇÃO DOS TESTES"
        currentRow = 12;
        worksheet.mergeCells(`A${currentRow}:I${currentRow}`);
        const execucaoHeader = worksheet.getCell(`A${currentRow}`);
        execucaoHeader.value = 'EXECUÇÃO DOS TESTES';
        execucaoHeader.font = { bold: true, size: 14, color: { argb: 'FFFFFFFF' } };
        execucaoHeader.alignment = { horizontal: 'center', vertical: 'middle' };
        execucaoHeader.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4ECDC4' } };

        currentRow++;

        // Cabeçalhos das colunas
        const headers = [
            'CENÁRIO DE TESTE',
            'ID CT',
            'CASO DE TESTE',
            'PRÉ-REQUISITO',
            'FLUXO DE TESTE',
            'RESULTADO ESPERADO',
            'PONTOS DE ATENÇÃO',
            'INTEGRAÇÃO (I4pro)',
            'ACEITE (CLIENTE)'
        ];

        headers.forEach((header, index) => {
            const cell = worksheet.getCell(`${String.fromCharCode(65 + index)}${currentRow}`);
            cell.value = header;
            cell.font = { bold: true, color: { argb: 'FFFFFFFF' } };
            cell.alignment = { horizontal: 'center', vertical: 'middle', wrapText: true };
            cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4ECDC4' } };
        });

        currentRow++;

        // Processar casos de teste CT-001 e CT-002
        const casos_regex = /(CT-\d+)([\s\S]*?)(?=CT-\d+|$)/g;
        let match;
        let casoId = 1;

        while ((match = casos_regex.exec(casos)) !== null) {
            const [, ctId, conteudo] = match;

            let cenario = '';
            let caso = '';
            let prerequisito = '';
            let fluxo = '';
            let resultado = '';
            let pontos = '';

            const linhasConteudo = conteudo.split('\n');
            let currentSection = '';
            let fluxoLines = [];

            for (const linha of linhasConteudo) {
                const linhaTrim = linha.trim();
                if (!linhaTrim) continue;

                if (linhaTrim.includes('🔹CENÁRIO DE TESTE:')) {
                    currentSection = 'cenario';
                    cenario = linhaTrim.split(':').slice(1).join(':').trim();
                } else if (linhaTrim.includes('🔸CASO DE TESTE:')) {
                    currentSection = 'caso';
                    caso = linhaTrim.split(':').slice(1).join(':').trim();
                } else if (linhaTrim.includes('⏳ PRÉ-REQUISITO:')) {
                    currentSection = 'prerequisito';
                    prerequisito = linhaTrim.split(':').slice(1).join(':').trim();
                } else if (linhaTrim.includes('📋 FLUXO DE TESTE:')) {
                    currentSection = 'fluxo';
                    fluxoLines = [];
                } else if (linhaTrim.includes('✅ RESULTADO ESPERADO:')) {
                    currentSection = 'resultado';
                    resultado = linhaTrim.split(':').slice(1).join(':').trim();
                } else if (linhaTrim.includes('⚠️ PONTOS DE ATENÇÃO:')) {
                    currentSection = 'pontos';
                    pontos = linhaTrim.split(':').slice(1).join(':').trim();
                } else if (currentSection === 'fluxo' && !linhaTrim.includes('✅') && !linhaTrim.includes('⚠️')) {
                    if (linhaTrim.match(/^\d+\./) || linhaTrim.includes('Acessar') || linhaTrim.includes('Executar') || linhaTrim.includes('Verificar')) {
                        fluxoLines.push(linhaTrim);
                    }
                }
            }

            fluxo = fluxoLines.join('\n');

            // Adicionar linha do caso de teste
            worksheet.getCell(`A${currentRow}`).value = cenario || `Teste ${ctId}`;
            worksheet.getCell(`B${currentRow}`).value = ctId;
            worksheet.getCell(`C${currentRow}`).value = caso || `Validação do ${ctId}`;
            worksheet.getCell(`D${currentRow}`).value = prerequisito || 'Sistema configurado';
            worksheet.getCell(`E${currentRow}`).value = fluxo || '1. Acessar a funcionalidade\n2. Executar ação\n3. Verificar resultado';
            worksheet.getCell(`F${currentRow}`).value = resultado || 'Comportamento esperado confirmado';
            worksheet.getCell(`G${currentRow}`).value = pontos || 'Validar funcionalidade';
            worksheet.getCell(`H${currentRow}`).value = 'OK';
            worksheet.getCell(`I${currentRow}`).value = `EH${casoId}`;

            // Aplicar cor de fundo alternada
            const bgColor = casoId % 2 === 1 ? 'FFE6E6FA' : 'FFD8BFD8';
            for (let col = 1; col <= 9; col++) {
                const cell = worksheet.getCell(currentRow, col);
                cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bgColor } };
                cell.alignment = { vertical: 'top', wrapText: true };
                cell.border = {
                    top: { style: 'thin' },
                    left: { style: 'thin' },
                    bottom: { style: 'thin' },
                    right: { style: 'thin' }
                };
            }

            currentRow++;
            casoId++;
        }        // Cabeçalho "EVIDÊNCIAS DE TESTE"
        worksheet.mergeCells(`H${currentRow}:I${currentRow}`);
        const evidenciasHeader = worksheet.getCell(`H${currentRow}`);
        evidenciasHeader.value = 'EVIDÊNCIAS DE TESTE';
        evidenciasHeader.font = { bold: true, color: { argb: 'FFFFFFFF' } };
        evidenciasHeader.alignment = { horizontal: 'center', vertical: 'middle' };
        evidenciasHeader.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF4ECDC4' } };

        // Ajustar altura das linhas
        worksheet.eachRow((row) => {
            row.height = 30;
        });

        // Gerar buffer do Excel
        const buffer = await workbook.xlsx.writeBuffer();

        // Configurar headers para download
        res.setHeader('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        res.setHeader('Content-Disposition', `attachment; filename="plano_teste_i4pro_${new Date().toISOString().split('T')[0]}.xlsx"`);

        res.send(buffer);

    } catch (error) {
        console.error('Erro ao gerar Excel:', error);
        res.status(500).json({ erro: "Erro ao gerar arquivo Excel" });
    }
});// Endpoints para IA e exportação podem ser adicionados aqui

const PORT = 8000;
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});
