from fastapi import Body
from core.ai_model import gerar_caso_teste_ia

# Endpoint para geração de caso de teste via IA
@app.post("/gerar-caso-ia/")
def gerar_caso_ia_api(
    requisito: str = Body(..., embed=True)
):
    caso = gerar_caso_teste_ia(requisito)
    return {"caso": caso}
"""
API FastAPI para o AgentIAQA
Permite acessar as principais funções do agente via HTTP.
"""
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from core import business, utils

app = FastAPI(title="AgenteIAQA API")


@app.post("/gerar-casos-de-teste/")
def gerar_casos_api(
    doc_dev: UploadFile = File(...),
    doc_spec: UploadFile = File(...)
):
    texto_dev = utils.processar_arquivo(doc_dev.file)
    texto_spec = utils.processar_arquivo(doc_spec.file)
    casos = business.gerar_casos_de_teste(texto_dev, texto_spec)
    return {"casos": casos}


@app.post("/gerar-massa-dados/")
def gerar_massa_api(
    quantidade: int = Form(...),
    campos: List[str] = Form(...)
):
    massa = business.gerar_massa_de_dados(quantidade, campos)
    return {"massa": massa}


@app.post("/gerar-massa-bancaria/")
def gerar_massa_bancaria_api(
    quantidade: int = Form(...),
    permitir_negativo: bool = Form(False)
):
    massa = business.gerar_massa_bancaria(quantidade, permitir_negativo)
    return {"massa_bancaria": massa}


@app.post("/exportar-relatorio/")
def exportar_relatorio_api(
    casos: List[str] = Form(...),
    nome_base: str = Form(...)
):
    business.exportar_relatorio(casos, nome_base)
    return {"status": "ok"}


@app.get("/")
def root():
    return {"mensagem": "API do AgenteIAQA está ativa!"}
