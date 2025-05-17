#!/bin/bash

SERVICE_NAME="agenteiaqa-agente-ia-1"

echo "📡 Monitorando mudanças para reiniciar o container $SERVICE_NAME..."

watchmedo shell-command \
  --patterns="*.py;*.toml;*.txt;*.yml;*.yaml" \
  --recursive \
  --command="docker restart $SERVICE_NAME" \
  .
