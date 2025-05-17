#!/bin/bash

# Nome do serviço no docker-compose
SERVICE_NAME="agente-ia"

echo "Monitorando mudanças para reiniciar o container $SERVICE_NAME..."

watchmedo shell-command \
    --patterns="*.py;*.toml;*.txt;*.yml;*.yaml" \
    --recursive \
    --command="docker-compose restart $SERVICE_NAME" \
    .
