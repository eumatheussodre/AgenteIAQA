@echo off
echo 🚀 Iniciando o container Docker...
echo Aguarde pequeno Gafanhoto

docker stop agente-testes
docker rm agente-testes
docker build -t agente-testes .
docker run -d -p 8501:8501 --name agente-testes agente-testes

echo ✅ Container iniciado com sucesso!
pause
