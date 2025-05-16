from fastapi import FastAPI, UploadFile
from file_processor import processar_arquivo
from test_generator import gerar_casos_de_teste

app = FastAPI()

@app.post("/gerar-testes/")
async def gerar_testes_api(file: UploadFile):
    conteudo = await file.read()
    texto = processar_arquivo(UploadFile(filename=file.filename, file=conteudo))
    casos = gerar_casos_de_teste(texto)
    return {"casos_de_teste": casos}
